import http.server
import socketserver
import urllib.parse
import socket
import sys


PORT = 7000


def local_ips():
    """Return every non-loopback IPv4 address this machine has."""
    ips = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if ip and not ip.startswith("127.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass
    # Fallback: ask the OS which interface would reach the internet.
    if not ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
            s.close()
        except Exception:
            pass
    return ips


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
        print(f"[GET ] {self.path}", flush=True)
        super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8', 'replace')
        params = urllib.parse.parse_qs(body)
        tag = params.get('tag', [''])[0]
        detail = params.get('detail', [''])[0]
        print(f"[{tag}] {detail}", flush=True)

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', '2')
        self.end_headers()
        self.wfile.write(b'ok')


def main():
    ips = local_ips()
    print("=" * 60)
    print("  PS4 JB server running")
    print("=" * 60)
    print(f"  Port: {PORT}")
    print()
    if ips:
        print("  Open this on the PS4 browser:")
        for ip in ips:
            print(f"      http://{ip}:{PORT}/jb.html")
        print()
        print("  (If one of them doesn't load, try another — your")
        print("   laptop may have several network interfaces.)")
    else:
        print("  No local IP detected. Are you connected to Wi-Fi?")
    print()
    print("  Both the PS4 and this computer must be on the same")
    print("  Wi-Fi network. PS4 does NOT need internet access.")
    print("=" * 60)
    print()

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), H) as httpd:
            httpd.serve_forever()
    except OSError as e:
        print(f"Could not bind port {PORT}: {e}")
        print("Is something else already using it?")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nshutting down")


if __name__ == "__main__":
    main()