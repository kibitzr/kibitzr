import os
import time
import socket
from six.moves import BaseHTTPServer
from six.moves.SimpleHTTPServer import SimpleHTTPRequestHandler
from multiprocessing import Process, Event


def start_server():
    port = free_port()
    server_address = ('127.0.0.1', port)
    root = os.path.join(os.path.dirname(__file__), 'www')
    initialized = Event()
    process = Process(
        target=run_server,
        args=(root, server_address, initialized),
    )
    process.start()
    initialized.wait()
    time.sleep(0.1)
    return process, server_address


def stop_server(process):
    process.terminate()


def run_server(root, server_address, initialized):
    os.chdir(root)
    SimpleHTTPRequestHandler.protocol_version = "HTTP/1.0"
    httpd = BaseHTTPServer.HTTPServer(server_address, SimpleHTTPRequestHandler)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on {0} port {1}...".format(sa[0], sa[1]))
    initialized.set()
    httpd.serve_forever()


def free_port():
    ports_to_check = [17261, 0]
    for port in ports_to_check:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('', port))
        except (OSError, socket.error):
            # Address already in use
            continue
        addr = s.getsockname()
        s.close()
        return addr[1]
