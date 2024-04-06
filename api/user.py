 
from http.server import BaseHTTPRequestHandler
from os.path import dirname, abspath, join
dir = dirname(abspath(__file__))
 
class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        with open(join(dir, '..', 'data', 'user.json'), 'r') as file:
          for line in file:
            self.wfile.write(line.encode())
        return