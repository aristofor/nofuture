# Examples

These examples are optional and may require extra dependencies.

## Files

- [`base.py`](base.py): MayBe basics (construction, mapping, chaining)
- [`objects.py`](objects.py): MayBe with dataclasses and domain objects
- [`result.py`](result.py): Result pipelines, error handling, serialization
- [`iteration.py`](iteration.py): Iteration, unpacking, and builtin integrations
- [`websocket_app.py`](websocket_app.py): Quart WebSocket server showcasing a full pipeline
- [`websocket_client.py`](websocket_client.py): Simple client for the WebSocket mini-app

## WebSocket mini-app

Dependencies:

- `quart`
- `websockets` (client)

Why Quart:

- Quart is an async reimplementation of Flask with native WebSocket support, providing a production-ready foundation while keeping Flask's familiar API.

Run the server:

```
python3 examples/websocket_app.py
```

Run the client:

```
python3 examples/websocket_client.py
```

Payload schema:

- Request: `{"op": "echo", "payload": {"user": "...", "text": "...", "room": "..."}}`
- Response (ok): `{"ok": true, "data": {...}}`
- Response (err): `{"ok": false, "error": "...", "code": "...", "details": ...}`

Supported ops:

- `echo`: returns the normalized payload
- `upper`: returns the payload with uppercased `text`
- `ping`: returns a `pong` response

Response examples:

```
{"ok": true, "data": {"op": "upper", "user": "alice", "text": "HELLO", "room": "lobby"}}
```

```
{"ok": false, "error": "unknown_op", "code": "OP_ERROR", "details": {"details": "noop", "stage": "handle_message"}}
```
