#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
REPORT_DIR = ROOT / "private-staging" / "qa"
REPORT_PATH = REPORT_DIR / "viewport-report.json"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]

TARGETS = [
    {
        "name": "desktop-dashboard",
        "url": "http://127.0.0.1:8765/#/dashboard",
        "window": "1440,1000",
    },
    {
        "name": "mobile-dashboard",
        "url": "http://127.0.0.1:8765/#/dashboard",
        "window": "390,844",
        "mobile": True,
    },
    {
        "name": "desktop-note",
        "url": "http://127.0.0.1:8765/#/projects/interface-design-direction",
        "window": "1440,1000",
    },
    {
        "name": "desktop-scrolled-note",
        "url": "http://127.0.0.1:8765/#/projects/interface-design-direction#related",
        "window": "1440,1000",
    },
    {
        "name": "mobile-note",
        "url": "http://127.0.0.1:8765/#/projects/interface-design-direction",
        "window": "390,844",
        "mobile": True,
    },
]

NODE_MOBILE_CAPTURE = r"""
const fs = require("node:fs");

async function main() {
  const cdpPort = process.env.CDP_PORT;
  const width = Number(process.env.VIEWPORT_WIDTH);
  const height = Number(process.env.VIEWPORT_HEIGHT);
  const url = process.env.TARGET_URL;
  const output = process.env.SCREENSHOT_PATH;
  const targets = await fetch(`http://127.0.0.1:${cdpPort}/json/list`).then((response) => response.json());
  const target = targets.find((item) => item.type === "page");
  if (!target) throw new Error("No Chrome page target was available.");

  const socket = new WebSocket(target.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.id && pending.has(data.id)) {
      pending.get(data.id)(data);
      pending.delete(data.id);
    }
  };
  await new Promise((resolve) => { socket.onopen = resolve; });
  function send(method, params = {}) {
    const callId = ++id;
    socket.send(JSON.stringify({ id: callId, method, params }));
    return new Promise((resolve) => pending.set(callId, resolve));
  }

  await send("Page.enable");
  await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", {
    width,
    height,
    deviceScaleFactor: 1,
    mobile: true,
  });
  await send("Page.navigate", { url });
  await new Promise((resolve) => setTimeout(resolve, 6000));
  const screenshot = await send("Page.captureScreenshot", {
    format: "png",
    captureBeyondViewport: false,
  });
  fs.writeFileSync(output, Buffer.from(screenshot.result.data, "base64"));
  socket.close();
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
"""


def chrome_path():
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chrome")


def run(command, timeout=25):
    return subprocess.run(command, text=True, capture_output=True, timeout=timeout)


def capture_mobile_target(chrome, target, screenshot):
    node = shutil.which("node")
    if not node:
        return None

    width, height = target["window"].split(",", 1)
    cdp_port = "9333"
    chrome_process = subprocess.Popen(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--remote-debugging-port={cdp_port}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1.2)
        result = subprocess.run(
            [node, "-e", NODE_MOBILE_CAPTURE],
            text=True,
            capture_output=True,
            timeout=18,
            env={
                **os.environ,
                "CDP_PORT": cdp_port,
                "VIEWPORT_WIDTH": width,
                "VIEWPORT_HEIGHT": height,
                "TARGET_URL": target["url"],
                "SCREENSHOT_PATH": str(screenshot),
            },
        )
    finally:
        chrome_process.terminate()
        try:
            chrome_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            chrome_process.kill()

    return result


def capture_target(chrome, target):
    screenshot = REPORT_DIR / f"{target['name']}.png"
    if target.get("mobile"):
        mobile_result = capture_mobile_target(chrome, target, screenshot)
        if mobile_result is not None:
            return {
                "name": target["name"],
                "url": target["url"],
                "window": target["window"],
                "returncode": mobile_result.returncode,
                "screenshot": str(screenshot.relative_to(ROOT)),
                "stderr": mobile_result.stderr.strip(),
                "capture_mode": "cdp-mobile",
            }

    command = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--force-device-scale-factor=1",
        "--virtual-time-budget=6000",
        f"--window-size={target['window']}",
        f"--screenshot={screenshot}",
        target["url"],
    ]
    result = run(command)
    return {
        "name": target["name"],
        "url": target["url"],
        "window": target["window"],
        "returncode": result.returncode,
        "screenshot": str(screenshot.relative_to(ROOT)),
        "stderr": result.stderr.strip(),
    }


def smoke_dom(chrome):
    result = run([
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--force-device-scale-factor=1",
        "--virtual-time-budget=6000",
        "--dump-dom",
        "http://127.0.0.1:8765/#/dashboard",
    ])
    dom = result.stdout
    checks = {
        "has_app_shell": "app-shell" in dom,
        "has_command_palette": "command-palette" in dom,
        "has_dashboard": "acac.sh" in dom,
        "has_search": "Search notes" in dom or "노트 검색" in dom,
    }
    return {
        "returncode": result.returncode,
        "checks": checks,
        "passed": result.returncode == 0 and all(checks.values()),
        "stderr": result.stderr.strip(),
    }


def main():
    chrome = chrome_path()
    if not chrome:
        raise SystemExit("Chrome or Chromium was not found. Install one to run viewport QA.")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    server = subprocess.Popen(
        ["python3", "-m", "http.server", "8765", "--directory", str(SITE_DIR)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1.2)
        captures = [capture_target(chrome, target) for target in TARGETS]
        dom = smoke_dom(chrome)
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "chrome": chrome,
        "captures": captures,
        "dom_smoke": dom,
    }
    REPORT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
    failures = [item for item in captures if item["returncode"] != 0]
    if failures or not dom["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
