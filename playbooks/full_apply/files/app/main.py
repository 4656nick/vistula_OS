from fastapi import FastAPI, Request
import socket
import subprocess

app = FastAPI(title="Server Info API")


@app.get("/hostname")
def api_hostname():
    output = socket.gethostname()
    return {"hostname": output}


@app.get("/ip")
def api_ip():
    output = subprocess.run(["/usr/bin/hostname", "-I"], capture_output=True, text=True)
    return {"ip": output.stdout.split()[0] if output else "unknown"}


@app.get("/kernel")
def api_kernel():
    output = subprocess.run(["/usr/bin/uname", "-r"], capture_output=True, text=True)
    return {"kernel": output.stdout}


@app.get("/myip")
async def api_myip(request: Request):
    xff = request.headers.get("x-forwarded-for")
    if xff:
        client_ip = xff.split(",")[0].strip()
    else:
        client_ip = request.client.host
    return {"myip": client_ip}
