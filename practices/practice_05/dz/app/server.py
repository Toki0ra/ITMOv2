"""HTTP layer for the Word Frequency Explorer."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from app.wordstats import AnalysisError, analyze

STATIC_DIR = Path(__file__).resolve().parent / "static"
MAX_BODY_BYTES = 1_000_000


def error_payload(code, message):
    return {"error": {"code": code, "message": message}}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_html(self, status, html):
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self.send_html(200, (STATIC_DIR / "index.html").read_text(encoding="utf-8"))
            return
        if self.path == "/api/analyze":
            self.send_json(405, error_payload("method_not_allowed", "Используйте POST"))
            return
        self.send_json(404, error_payload("not_found", "Ресурс не найден"))

    def do_POST(self):
        if self.path != "/api/analyze":
            self.send_json(404, error_payload("not_found", "Ресурс не найден"))
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            size = -1
        if size < 0 or size > MAX_BODY_BYTES:
            self.send_json(400, error_payload("invalid_body", "Некорректная длина тела запроса"))
            return
        raw = self.rfile.read(size) if size else b""
        try:
            body = json.loads(raw.decode("utf-8")) if raw else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_json(400, error_payload("invalid_body", "Тело запроса должно быть JSON"))
            return
        if not isinstance(body, dict):
            self.send_json(400, error_payload("invalid_body", "Тело запроса должно быть JSON-объектом"))
            return
        try:
            result = analyze(body.get("text"), body.get("limit", 3))
        except AnalysisError as exc:
            self.send_json(exc.status, error_payload(exc.code, str(exc)))
            return
        except Exception:
            self.send_json(500, error_payload("internal_error", "Внутренняя ошибка сервера"))
            return
        self.send_json(200, result)

    def log_message(self, format, *args):
        pass


def create_server(host="127.0.0.1", port=0):
    return ThreadingHTTPServer((host, port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8067)
    args = parser.parse_args()
    server = create_server(args.host, args.port)
    server.daemon_threads = True
    print(f"Word Frequency Explorer: http://{args.host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
