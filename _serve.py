"""Local dev server for reply-croquetclaude-site. Run from project root."""
import http.server
import socketserver
import os

PORT = 8765
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
    print(f"Serving {ROOT} at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
