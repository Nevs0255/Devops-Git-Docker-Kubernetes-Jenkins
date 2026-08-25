from http.server import BaseHTTPRequestHandler, HTTPServer
from app import moyenne

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(f'{{"moyenne": {moyenne():.1f}}}'.encode())

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
