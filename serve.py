import http.server
import socketserver
import urllib.parse

PORT = 8082

class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.appcache': 'text/cache-manifest',
        '.bin': 'application/octet-stream',
        '.js': 'application/javascript',
    }

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/favicon.ico':
            return

        if path.endswith('.appcache'):
            print(f"\n📄 [MANIFEST CHECK] PS4 is checking cache.appcache...")
        elif path in ['/jb.html', '/index.html']:
            print(f"\n🌐 [PAGE LOAD] {path}")
        elif path.endswith('.js') or path.endswith('.bin') or path.endswith('.png'):
            print(f"📥 [DOWNLOAD] Fetching {path}")

        super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8', 'replace')
        params = urllib.parse.parse_qs(body)
        tag = params.get('tag', [''])[0]
        detail = params.get('detail', [''])[0]
        if tag != "REAP":
            print(f"  [{tag}] {detail}")

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', '2')
        self.end_headers()
        self.wfile.write(b'ok')

def main():
    print("=" * 60)
    print(f"  PS4 JB server running (Port {PORT})")
    print("=" * 60)
    print(f"  http://10.34.193.98:{PORT}/jb.html")
    print("=" * 60 + "\n")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), H) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    main()