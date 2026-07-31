from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import hashlib
import json


app = FastAPI()

EMAIL = "22f2000403@ds.study.iitm.ac.in"


@app.post("/")
async def mcp_endpoint(request: Request):

    body = await request.json()

    method = body.get("method")


    # MCP initialize handshake
    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "challenge-server",
                    "version": "1.0.0"
                }
            }
        })


    # initialized notification
    if method == "notifications/initialized":
        return JSONResponse({})


    # tools/list
    if method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "tools": [
                    {
                        "name": "solve_challenge",
                        "description": "Solve exam challenge",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ]
            }
        })


    # tools/call
    if method == "tools/call":

        headers = request.headers

        challenge = headers.get("x-exam-challenge")


        if not challenge:
            return JSONResponse({
                "error": "Missing challenge header"
            })


        value = f"{challenge}:{EMAIL.strip().lower()}"

        result = hashlib.sha256(
            value.encode()
        ).hexdigest()[:16]


        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }
        })


    return JSONResponse({
        "error": "Unknown method"
    })