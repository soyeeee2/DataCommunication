import os
import socket
import random

FLAGS = _ = None
DEBUG = False

file_size = 0

def sendInfoData(sock, client, filename):
    global file_size
    with open(filename, "rb") as f:
        content = f.read()
        file_size = len(content)
        print(str(file_size))
        return str(file_size)
        

def sendDownloadData(sock, client, filename):
    global file_size
    with open(filename, "rb") as f:
        content = f.read()
        offset = 0
        chunk_size = 1460

        while offset < file_size:
            chunk = content[offset:offset+chunk_size]
            sock.sendto(chunk, client)
            offset += chunk_size



def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.address, FLAGS.port))
    print(f'Listening on {sock}')


    while True:
        data, client = sock.recvfrom(2**16)
        data = data.decode('utf-8')

        if data.startswith("INFO") or data.startswith("DOWNLOAD"):
            state, filename = data.strip().split(maxsplit=1)
            print(f'state {state} - filename {filename}')

            if not os.path.exists(filename):
                sock.sendto(b"404 Not Found", client)
                print(f"File not found: {filename}")
                return
            
            if state == 'INFO':
                response = sendInfoData(sock, client, filename)
            elif state == 'DOWNLOAD':
                response = sendDownloadData(sock, client, filename)
        

        
        print(f'Received {data} from {client}')
        sock.sendto(response.encode('utf-8'), client)
        print(f'Send {response} to {client}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='127.0.0.1',
                        help='The address to serve service')
    parser.add_argument('--port', type=int, default=3034,
                        help='The port to serve service')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()


 