#!/usr/bin/env python3
"""Tiny zero-dependency server for the YC application tracker.

Serves the tracker page and persists applied/notes state to tracker_data.json
on disk, so progress survives restarts and is readable for the next batch.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "yc_applications.html")
DATA = os.path.join(HERE, "tracker_data.json")
PORT = 8765


def load_data():
    if os.path.exists(DATA):
        try:
            with open(DATA) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_data(d):
    with open(DATA, "w") as f:
        json.dump(d, f, indent=2)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if isinstance(body, str):
            body = body.encode()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html", "/yc_applications.html"):
            with open(PAGE, "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        elif self.path == "/api/state":
            self._send(200, json.dumps(load_data()))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path == "/api/state":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                incoming = json.loads(raw)
            except Exception:
                self._send(400, json.dumps({"error": "bad json"}))
                return
            save_data(incoming)
            self._send(200, json.dumps({"ok": True, "saved": len(incoming)}))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def log_message(self, *args):
        pass  # quiet


if __name__ == "__main__":
    print(f"Tracker running at http://localhost:{PORT}/")
    print(f"State persists to {DATA}")
    HTTPServer(("", PORT), Handler).serve_forever()
