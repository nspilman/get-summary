# app.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from twisted.internet import reactor

from pipeline import run_application
from dotenv import load_dotenv

load_dotenv() 

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"We out here")
        run_application()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd server on port 8080")
    httpd.serve_forever()

if __name__ == "__main__":
    reactor_thread = threading.Thread(target=reactor.run, daemon=True)
    reactor_thread.start()
    run()
