#!/usr/bin/env python3
#
# The *hello server* is an HTTP server that responds to a GET request by
# sending back a friendly greeting.  Run this program in your terminal and
# access the server at http://localhost:8000 in your browser.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

messageMemory = []

sampleHtmlForm = '''
            <!DOCTYPE html>
            <title>Message Board</title>
            <form method="POST" action="http://localhost:8000/">
                <textarea name="message"></textarea>
                <br>
                <button type="submit">Post it!</button>
            </form>
            <pre>
                {}
            </pre>
        '''


class HelloHandler(BaseHTTPRequestHandler):

    def processGetResponse(self):
        # Now, write the response body.
        self.wfile.write(self.path[1:].encode())
    
    def showForm(self):
        # Now, write the response body.
        # self.wfile.write(sampleHtmlForm.encode())
        # Send the form with the messages in it.
        mesg = sampleHtmlForm.format("\n".join(messageMemory))
        self.wfile.write(mesg.encode())

    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        if self.path != '/':
            HelloHandler.processGetResponse(self)
        else:
            HelloHandler.showForm(self)

    def do_POST(self):
         #Read the value of content-length
         length = int(self.headers.get('content-length', 0))
         data = self.rfile.read(length).decode()

         parsed_data = parse_qs(data)

         magic = parsed_data['message'][0]

         messageMemory.append(magic)

         # First, send a 200 OK response.
         self.send_response(303)
        
         # new_path = '%s'%('/', self.path)
         self.send_header('Location', '/')

         # Then send headers.
         # self.send_header('Content-type', 'text/plain; charset=utf-8')
         self.end_headers()

         # # # Now, write the response body.
         # self.wfile.write(magic.encode())

if __name__ == '__main__':
    server_address = ('', 8000)  # Serve on all addresses, port 8000.
    httpd = HTTPServer(server_address, HelloHandler)
    httpd.serve_forever()
