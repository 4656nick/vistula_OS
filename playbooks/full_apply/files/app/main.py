from fastapi import FastAPI, Request
import socket
import subprocess

app = FastAPI(title="Server Info API")


def get_hostname() -> str:
    return socket.gethostname()


def get_kernel() -> str:
    return subprocess.check_output(["uname", "-r"]).decode().strip()


def get_ip() -> str:
    # Берём IP по умолчанию для выхода в интернет
    # (ip route get 1.1.1.1 -> ... src X.X.X.X ...)
    # try:
    #     output = subprocess.check_output(
    #         ["ip", "route", "get", "1.1.1.1"], text=True
    #     )
    #     for part in output.split():
    #         if part == "src":
    #             return output.split()[output.split().index("src") + 1]
    # except Exception:
    #     pass

    # fallback
    output = subprocess.check_output(["hostname", "-I"], text=True).strip()
    return output.split()[0] if output else "unknown"


@app.get("/hostname")
def api_hostname():
    return {"hostname": get_hostname()}


@app.get("/ip")
def api_ip():
    return {"ip": get_ip()}


@app.get("/kernel")
def api_kernel():
    return {"kernel": get_kernel()}


@app.get("/myip")
async def api_myip(request: Request):
    # Если запрос идёт через nginx, смотрим X-Forwarded-For
    xff = request.headers.get("x-forwarded-for")
    if xff:
        client_ip = xff.split(",")[0].strip()
    else:
        client_ip = request.client.host
    return {"myip": client_ip}
