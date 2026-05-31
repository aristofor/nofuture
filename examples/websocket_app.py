# Example: WebSocket mini-app with a Result/MayBe chain
# Optional deps:
#   pip install quart
# Note: Quart is an async reimplementation of Flask with native WebSocket support.

import asyncio
import json

from quart import Quart, websocket
from nofuture import MayBe, Result

app = Quart(__name__)


def maybe(value):
    return MayBe.just(value) if value is not None else MayBe.nothing()


def parse_json(raw_text):
    try:
        return Result.ok(json.loads(raw_text))
    except Exception as exc:
        return Result.err("invalid_json", code="PARSE_ERROR", details=str(exc))


def require_fields(envelope):
    missing = [key for key in ("op", "payload") if key not in envelope]
    if missing:
        return Result.err("missing_fields", code="VALIDATION_ERROR", details=missing)
    return Result.ok(envelope)


def normalize_payload(envelope):
    payload = envelope["payload"]
    if not isinstance(payload, dict):
        return Result.err("payload_not_object", code="VALIDATION_ERROR")

    missing = [key for key in ("user", "text") if key not in payload]
    if missing:
        return Result.err("missing_payload_fields", code="VALIDATION_ERROR", details=missing)

    text = str(payload["text"]).strip()
    if not text:
        return Result.err("empty_text", code="VALIDATION_ERROR")

    updated_payload = dict(payload)
    updated_payload["text"] = text
    updated = dict(envelope)
    updated["payload"] = updated_payload
    return Result.ok(updated)


def enrich(envelope):
    payload = envelope["payload"]
    room = maybe(payload.get("room")) >> (lambda r: MayBe.just(str(r).strip().lower()))
    updated = {
        "op": envelope["op"],
        "user": payload["user"],
        "text": payload["text"],
        "room": room.or_else("lobby"),
    }
    return Result.ok(updated)


def handle_message(raw_text):
    # Parse -> validate envelope -> normalize payload -> enrich data; then annotate errors.
    result = Result.ok(raw_text) >> parse_json >> require_fields >> normalize_payload >> enrich
    return result.map_err(lambda msg, code, details: (msg, code, {"details": details, "stage": "handle_message"}))


def route_op(data):
    # Route by op and return a Result for each operation.
    op = str(data.get("op", "")).lower()
    if op == "echo":
        return Result.ok(data)
    if op == "upper":
        updated = dict(data)
        updated["text"] = str(data["text"]).upper()
        return Result.ok(updated)
    if op == "ping":
        return Result.ok({"op": "pong", "user": data.get("user"), "text": "pong", "room": data.get("room")})
    return Result.err("unknown_op", code="OP_ERROR", details=op)


@app.get("/health")
async def health():
    await asyncio.sleep(0)
    return {"ok": True}


@app.websocket("/ws")
async def ws_handler():
    while True:
        raw = await websocket.receive()
        if raw is None:
            break

        result = handle_message(raw) >> route_op
        payload = result.match(
            ok=lambda data: {"ok": True, "data": data},
            err=lambda msg, code, details: {
                "ok": False,
                "error": msg,
                "code": code,
                "details": details,
            },
        )
        await websocket.send(json.dumps(payload))


if __name__ == "__main__":
    # Run: python3 examples/websocket_app.py
    # Test: python3 examples/websocket_client.py
    app.run(host="127.0.0.1", port=5000, debug=True)
