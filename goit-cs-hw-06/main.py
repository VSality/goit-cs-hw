import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
from multiprocessing import Process
import json  # Для работы с JSON

# web Server
class HttpHandler(BaseHTTPRequestHandler):
    
    
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        #print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        #print(data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        #print(data_dict)
        json_data = json.dumps(data_dict)
    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("localhost", 5000))
            sock.sendall(json_data.encode('utf-8'))
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        

    def do_GET(self):
        script_dir = os.path.join(os.path.dirname(__file__))
        
        
        pr_url = urllib.parse.urlparse(self.path)
  
        if pr_url.path == '/':
            file_path = os.path.join(script_dir, 'index.html')
            self.send_html_file(file_path)
        elif pr_url.path == '/message.html':
            file_path = os.path.join(script_dir, 'message.html')
            self.send_html_file(file_path)
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]) != "":
                self.send_static(pr_url.path[1:])
            else:
                file_path = os.path.join(script_dir, 'error.html')
                self.send_html_file(file_path, 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, filename):
     
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        script_dir = os.path.join(os.path.dirname(__file__))
        file_path = os.path.join(script_dir, filename)

        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())
    


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


# Socket Server
import socket
from concurrent import futures as cf

def run_server(ip, port):
    
    def handle(sock: socket.socket, address: str):
        print(f'Connection established {address}')
        while True:
            received = sock.recv(1024)
            if not received:
                break
            data = received.decode()
            print(f'Data received: {data}')
            sock.send(received)
        print(f'Socket connection closed {address}')
        sock.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)
    print(f'Start echo server {server_socket.getsockname()}')
    with cf.ThreadPoolExecutor(10) as client_pool:
        try:
            while True:
                new_sock, address = server_socket.accept()
                client_pool.submit(handle, new_sock, address)
        except KeyboardInterrupt:
            print(f'Destroy server')
        finally:
            server_socket.close()

if __name__ == '__main__':
    host = 'localhost'
    port = 5000

    web_process = Process(target=run)
    socket_process = Process(target=run_server, args=(host, port))

    # Запускаем процессы
    web_process.start()
    socket_process.start()

    # Ждем завершения процессов
    web_process.join()
    socket_process.join()