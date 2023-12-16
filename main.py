from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import time
import hashlib
import hmac
import base64
import uuid
import requests
import uvicorn

if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()

@app.get("/")
async def root():
    token = '067c85c4d399d297516db3445e4b85b9d2f9bb8b468b608163426b0790cf2070484dc6f06918ce8fbcf0588f29074f97'
    secret = '5beb4f11d01e8b6a4f298fe76a51cbea'

    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    api_header = {
        "Authorization": token,
        "Content-Type": "application/json",
        "charset": "utf8",
        "t": str(t),
        "sign": str(sign, 'utf-8'),
        "nonce": str(nonce)
    }

    api_request = requests.get("https://api.switch-bot.com/v1.1/devices/C4857BE2A04B/status", headers=api_header)
    meter_one = api_request.json()["body"]

    api_request = requests.get("https://api.switch-bot.com/v1.1/devices/D2870B269D6B/status", headers=api_header)
    meter_two = api_request.json()["body"]

    api_request = requests.get("https://api.switch-bot.com/v1.1/devices/D84D3FBF0DA4/status", headers=api_header)
    hub = api_request.json()["body"]

    html = f"""
        <html>
            <head>
                <title>Switch Bot</title>
                <link rel='stylesheet' href='https://w3schools.com/w3css/4/w3.css'>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body>
                <div class='w3-container w3-blue w3-xxlarge'>Humidity and Temperature of <b>The Palace</b></div>
                <div class='w3-container'>
                    <h3>Outside:</h3>
                    <p>
                        Temperature is {meter_one['temperature']} C <br>
                        Humidity is {meter_one['humidity']}%
                    </p>
                    <h3>Master Bedroom:</h3>
                    <p>
                        Temperature is {meter_two['temperature']} C <br>
                        Humidity is {meter_two['humidity']}%
                    </p>
                    <h3>Max's Room:</h3>
                    <p>
                        Temperature is {hub['temperature']} C <br>
                        Humidity is {hub['humidity']}%
                    </p>
                </div>
            </body>
    """

    return HTMLResponse(content=html, status_code=200)