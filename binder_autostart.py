# binder_autostart.py
# Auto-start your simulator on kernel start (Binder-friendly).
# Writes logs to ~/.qsim_backend.log so you can debug privately.

import os, sys, subprocess, time, urllib.request, atexit, pathlib, shlex

PORT = int(os.environ.get("SIM_PORT", "5174"))
HOST = "127.0.0.1"
HOME = os.path.expanduser("~")
LOG  = os.path.join(HOME, ".qsim_backend.log")

def _probe(url, timeout=0.7):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status in (200, 301, 302, 404)
    except Exception:
        return False

def _probe_local():
    return _probe(f"http://{HOST}:{PORT}")

def _start_backend():
    env = os.environ.copy()
    env.setdefault("QSIM_MODE", "notebook")
    env.setdefault("USE_REDIS", "0")

    # Candidate commands (tries start.py first, then common ASGI paths)
    cmds = []
    if pathlib.Path("start.py").exists():
        cmds.append([sys.executable, "start.py", "--host", "0.0.0.0", "--port", str(PORT)])

    # Change these candidates to match your repo if you know the exact app path
    asgi_candidates = [
        "server.main:app",
        "api.app:app",
        "app.main:app",
        "backend.app:app",
        "main:app",
    ]
    for app in asgi_candidates:
        cmds.append([sys.executable, "-m", "uvicorn", app, "--host", "0.0.0.0", "--port", str(PORT)])

    # Try commands until one boots
    for cmd in cmds:
        try:
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(f"\n=== launching: {shlex.join(cmd)} ===\n")
            proc = subprocess.Popen(cmd, stdout=open(LOG, "ab"), stderr=subprocess.STDOUT, env=env)
        except Exception as e:
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(f"launch failed: {e}\n")
            continue

        # ensure we clean up when kernel exits
        def _stop():
            try: proc.terminate()
            except Exception: pass
        atexit.register(_stop)

        # wait up to ~2 min for readiness
        for _ in range(120):
            if _probe_local():
                with open(LOG, "a", encoding="utf-8") as f:
                    f.write("backend ready ✅\n")
                return True
            time.sleep(1)

        with open(LOG, "a", encoding="utf-8") as f:
            f.write("boot attempt timed out; trying next candidate…\n")

    # all attempts failed
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("❌ all backend start attempts failed\n")
    return False

try:
    # avoid double-start if already running
    if not _probe_local():
        _start_backend()

    # stash the proxied URL for convenience
    base = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")
    proxied = f"{base}proxy/{PORT}/"
    try:
        with open(os.path.join(HOME, ".qsim_proxy_url"), "w", encoding="utf-8") as f:
            f.write(proxied)
    except Exception:
        pass
except Exception:
    # never block kernel startup
    pass
