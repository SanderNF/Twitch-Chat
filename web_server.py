import argparse
import json
import threading
import time
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

"""
web_server.py

Basic HTTP server that repeatedly (every 100ms by default) reloads a JSON file into memory
and serves it at /Chat.json. Also serves index.html and style.css from the same directory
(if present) or falls back to a small built-in page.
"""


# Shared state
CACHE_LOCK = threading.Lock()
CACHED_TEXT = b'{}'  # bytes
LAST_ERROR = None






try:
    with open('log.json', 'r',  encoding='utf-8') as f:
        json.load(f)
except FileNotFoundError:
    with open('log.json', 'w',  encoding='utf-8') as f:
        json.dump(["log's are saved here"], f, ensure_ascii=False, indent=4)


def loader_loop(path: str, interval: float):
    global CACHED_TEXT, LAST_ERROR
    while True:
        try:
            with open(path, "rb") as f:
                raw = f.read()
            # Validate JSON (work on text)
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = raw.decode("utf-8", errors="replace")
            json.loads(text)  # validation
            with CACHE_LOCK:
                CACHED_TEXT = text.encode("utf-8")
                LAST_ERROR = None
        except Exception as e:
            with CACHE_LOCK:
                LAST_ERROR = str(e)
        time.sleep(interval)


def _guess_content_type(path: str) -> str:
    path = path.lower()
    if path.endswith(".html") or path.endswith(".htm"):
        return "text/html; charset=utf-8"
    if path.endswith(".css"):
        return "text/css; charset=utf-8"
    if path.endswith(".json"):
        return "application/json; charset=utf-8"
    if path.endswith(".js"):
        return "application/javascript; charset=utf-8"
    return "application/octet-stream"


class JSONRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        # strip query params
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "/index.html":
            self._serve_index()
        elif path == "/style.css":
            self._serve_static("style.css")
        elif path == "/Chat.json":
            self._serve_data()
        else:
            # try to serve from current dir for any other file
            local = path.lstrip("/")
            if local and os.path.isfile(local):
                self._serve_static(local)
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"Not Found")

    def _serve_index(self):
        # prefer local index.html if present
        if os.path.isfile("index.html"):
            try:
                with open("index.html", "rb") as f:
                    data = f.read()
                ctype = _guess_content_type("index.html")
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            except Exception:
                pass

        # fallback built-in page which fetches /Chat.json and loads style from /style.css
        html = (
            "<!doctype html><html><head><meta charset='utf-8'><title>JSON Server</title>"
            "<link rel='stylesheet' href='/style.css'>"
            "</head>"
            "<body><h1>JSON Server</h1>"
            "<pre id='out'>loading...</pre>"
            "<script>async function poll(){let r=await fetch('/Chat.json'); if(r.ok){let t=await r.text(); document.getElementById('out').textContent=t;} else {let t=await r.text(); document.getElementById('out').textContent='ERROR '+r.status+'\\n'+t;}} setInterval(poll,500); poll();</script>"
            "</body></html>"
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def _serve_static(self, filename: str):
        try:
            with open(filename, "rb") as f:
                data = f.read()
            ctype = _guess_content_type(filename)
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Not Found")
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(("Server error: " + str(e)).encode("utf-8"))

    def _serve_data(self):
        with CACHE_LOCK:
            data = CACHED_TEXT
            err = LAST_ERROR
        if err is not None and (not data or data == b''):
            # no valid data yet, return 503 with error
            body = ("{\"error\": " + json.dumps(err) + "}").encode("utf-8")
            self.send_response(503)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # serve cached JSON
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        # keep logs minimal
        log_status = ''
        log_type = ''
        write_log = False
        if args[1] == '200':
            log_status = '\x1b[1;30m'
            log_type = 'success'
        elif args[1] == '404':
            log_status = '\x1b[1;33m'
            log_type = 'warning'
            write_log = True
        else:
            log_status = '\x1b[1;31m]'
            log_type = 'error'
            write_log = True
        log_message = ("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))
        print(log_status, log_message, '\x1b[1;30m')
        if write_log:
            print(f'saving {log_type} to file')
            with open('log.json', 'r',  encoding='utf-8') as f:
                b = json.load(f)
            #print(b)
            b.append([log_type, log_message])
            try:
                with open('log.json', 'w',  encoding='utf-8') as f:
                    json.dump(b, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f'Log save failed with error: {e} \n {Exception}')


def main():
    parser = argparse.ArgumentParser(description="Simple JSON-reloading HTTP server")
    parser.add_argument("--file", "-f", default="Chat.json", help="Path to JSON file to reload (default Chat.json)")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to listen on")
    parser.add_argument("--interval", "-i", type=float, default=0.1, help="Reload interval in seconds (default 0.1)")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Warning: file '{args.file}' not found. Server will keep trying to load it.")

    t = threading.Thread(target=loader_loop, args=(args.file, args.interval), daemon=True)
    t.start()

    server_address = ("", args.port)
    httpd = ThreadingHTTPServer(server_address, JSONRequestHandler)
    print(f"Serving on http://0.0.0.0:{args.port}  (reloading '{args.file}' every {args.interval}s)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.server_close()


if __name__ == "__main__":
    main()