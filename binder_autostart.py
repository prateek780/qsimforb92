# binder_autostart.py
# Auto-start your simulator backend when the IPython kernel starts (Binder-friendly).
# Runs silently and is safe if the backend is already up.

import os, sys, subprocess, time, urllib.request, atexit, pathlib

PORT = int(os.environ.get("SIM_PORT", "5174"))
HOST = "127.0.0.1"

def _probe(port=PORT, timeout=0.7):
    try:
        urllib.request.urlopen(f"http://{HOST}:{port}", timeout=timeout)
        return True
    except Exception:
        return False

def _start_backend():
    # Ensure notebook-safe mode
    env = os.environ.copy()
    env.setdefault("QSIM_MODE", "notebook")
    env.setdefault("USE_REDIS", "0")

    # Choose ONE command that matches your project:
    if pathlib.Path("start.py").exists():
        cmd = [sys.executable, "start.py", "--host", "0.0.0.0", "--port", str(PORT)]
    else:
        # Fallback: uvicorn with your FastAPI app
        # >>> change 'server.main:app' to your app import path if you use uvicorn <<<
        app = env.get("ASGI_APP", "server.main:app")
        cmd = [sys.executable, "-m", "uvicorn", app, "--host", "0.0.0.0", "--port", str(PORT)]

    # Launch quietly
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        env=env
    )

    # Stop it when the kernel exits
    def _stop():
        try:
            proc.terminate()
        except Exception:
            pass
    atexit.register(_stop)

    # Wait briefly for readiness
    for _ in range(120):
        if _probe():
            break
        time.sleep(1)

try:
    if not _probe():
        _start_backend()

    # Compute and stash the proxied URL (useful for any viewer code)
    base = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")
    proxied = f"{base}proxy/{PORT}/"
    # Write a hint file (optional)
    try:
        with open(os.path.expanduser("~/.qsim_proxy_url"), "w") as f:
            f.write(proxied)
    except Exception:
        pass

except Exception:
    # Never block kernel if the backend can't start
    pass
