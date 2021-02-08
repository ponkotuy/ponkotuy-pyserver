import textwrap
from http.server import BaseHTTPRequestHandler, HTTPServer


class HtmlRequestHandler(BaseHTTPRequestHandler):
    Page = textwrap.dedent('''\
            <html>
            <body>
            <p>Hellow, web!</p>
            </body>
            </html>''').encode("utf-8")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()
        self.wfile.write(self.Page)


if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, HtmlRequestHandler)
    server.serve_forever()
