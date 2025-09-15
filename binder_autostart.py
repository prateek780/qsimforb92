# binder_autostart.py  — non-blocking autostart with private logs
import os, sys, subprocess, time, urllib.request, atexit, pathlib, threading, shlex

# allow turning off autostart entirely if needed
if os.environ.get("QSIM_DISABLE_AUTOSTART") == "1":
    raise SystemExit

PORT = int(os.environ.get("SIM_PORT", "5174"))
HOST = "127.0.0.1"
HOME = os.path.expanduser("~")
LOG  = os.path.join(HOME, ".qsim_backend.log")

def _probe(timeout=0.7):
    try:
        with urllib.request.urlopen(f"http://{HOST}:{PORT}", timeout=timeout) as r:
            return r.status in (200, 301, 302, 404)
    except Exception:
        return False

def _launch_and_watch():
    env = os.environ.copy()
    env.setdefault("QSIM_MODE", "notebook")
    env.setdefault("USE_REDIS", "0")

    # candidate commands: prefer start.py; fall back to uvicorn with common app paths
    cmds = []
    if pathlib.Path("start.py").exists():
        cmds.append([sys.executable, "start.py", "--host", "0.0.0.0", "--port", str(PORT)])

    # change the first one to your real ASGI app if you know it
    for app in [env.get("ASGI_APP", "server.main:app"), "api.app:app", "main:app"]:
        cmds.append([sys.executable, "-m", "uvicorn", app, "--host", "0.0.0.0", "--port", str(PORT)])

    for cmd in cmds:
        try:
            with open(LOG, "ab") as f:
                f.write(f"\n=== launching: {shlex.join(cmd)} ===\n".encode())
            proc = subprocess.Popen(cmd, stdout=open(LOG, "ab"), stderr=subprocess.STDOUT, env=env)
            atexit.register(lambda: proc.terminate())
        except Exception as e:
            with open(LOG, "ab") as f:
                f.write(f"launch failed: {e}\n".encode())
            continue

        # probe in the background; DON'T block kernel startup
        for _ in range(120):
            if _probe():
                with open(LOG, "ab") as f:
                    f.write(b"backend ready ✅\n")
                return
            time.sleep(1)

        with open(LOG, "ab") as f:
            f.write(b"boot attempt timed out; trying next candidate…\n")

# If nothing is listening yet, start a background thread and return immediately
if not _probe():
    threading.Thread(target=_launch_and_watch, daemon=True).start()

# Write the proxied URL for convenience
base = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")
try:
    with open(os.path.join(HOME, ".qsim_proxy_url"), "w", encoding="utf-8") as f:
        f.write(f"{base}proxy/{PORT}/")
except Exception:
    pass
