#!/usr/bin/env python3
"""Local dev server for icom-custom-firmware/docs.

Serves the patcher web UI over HTTP so that ES-module scripts and
Web Workers load without CORS/file-protocol restrictions.

Usage:
    python docs/dev_server.py
    python docs/dev_server.py --port 8765
    python docs/dev_server.py --bind 0.0.0.0
"""

import argparse
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler


HERE = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    """Serve docs/ with CORS headers allowed during development."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="Local dev server for the patcher UI")
    parser.add_argument("--port", "-p", type=int, default=8765, help="Port to listen on (default: 8765)")
    parser.add_argument("--bind", "-b", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    args = parser.parse_args()

    server = HTTPServer((args.bind, args.port), Handler)
    url = f"http://{args.bind if args.bind != '127.0.0.1' else 'localhost'}:{args.port}/"
    print(f"Serving at {url}")
    print("Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.server_close()


if __name__ == "__main__":
    main()
