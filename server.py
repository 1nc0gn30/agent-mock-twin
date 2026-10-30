#!/usr/bin/env python3
"""
server.py: Standalone production HTTP daemon for Agent Mock Twin.
Runs on 127.0.0.1:8097 serving REST API, SSE telemetry feed, and static sovereign dashboard.
Zero external pip dependencies.
"""

import argparse
import os
import signal
import sys

# Ensure src/ is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from agent_mock_twin.mock_server import MockServer


def main():
    parser = argparse.ArgumentParser(description="Agent Mock Twin Production Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8097, help="Port to listen on (default: 8097)")
    parser.add_argument("--db", default=os.path.join(BASE_DIR, "agent_mock.db"), help="Path to SQLite database")
    args = parser.parse_args()

    public_dir = os.path.join(BASE_DIR, "public")
    server = MockServer(
        host=args.host,
        port=args.port,
        db_path=args.db,
        public_dir=public_dir
    )

    def handle_signal(sig, frame):
        print("\nShutting down Agent Mock Twin gracefully...")
        server.shutdown_cleanly()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    print(f"✦ Agent Mock Twin listening on http://{args.host}:{args.port}")
    print(f"  Health Check: http://{args.host}:{args.port}/health")
    print(f"  API Routes:   http://{args.host}:{args.port}/api/routes")
    print(f"  Telemetry:    http://{args.host}:{args.port}/api/stats")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        handle_signal(None, None)


if __name__ == "__main__":
    main()
