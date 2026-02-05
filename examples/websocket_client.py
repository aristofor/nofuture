# Example WS client for websocket_app.py
# Optional deps:
#   pip install websockets

import asyncio
import json

import websockets


async def main():
    uri = "ws://127.0.0.1:5000/ws"
    async with websockets.connect(uri) as ws:
        # Valid payload (echo)
        await ws.send(
            json.dumps(
                {
                    "op": "echo",
                    "payload": {"user": "alice", "text": "  Hello  ", "room": "Main"},
                }
            )
        )
        print("server:", await ws.recv())

        # Uppercase
        await ws.send(
            json.dumps(
                {
                    "op": "upper",
                    "payload": {"user": "alice", "text": "  whisper  ", "room": "Main"},
                }
            )
        )
        print("server:", await ws.recv())

        # Ping
        await ws.send(json.dumps({"op": "ping", "payload": {"user": "alice", "text": "x"}}))
        print("server:", await ws.recv())

        # Unknown op
        await ws.send(json.dumps({"op": "noop", "payload": {"user": "alice", "text": "x"}}))
        print("server:", await ws.recv())

        # Missing payload fields
        await ws.send(json.dumps({"op": "echo", "payload": {"user": "bob"}}))
        print("server:", await ws.recv())

        # Invalid payload type
        await ws.send(json.dumps({"op": "echo", "payload": "not-an-object"}))
        print("server:", await ws.recv())

        # Invalid JSON
        await ws.send("{not-json}")
        print("server:", await ws.recv())


if __name__ == "__main__":
    asyncio.run(main())
