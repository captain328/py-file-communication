#!/usr/bin/env python3

import sys, argparse, socket, time
from threading import Thread

HOST = '127.0.0.1'
PORT_BINDING_ERROR = 1
BUFFER_SIZE = 2048

connection_count = 0

def handle_connection(connection, ip, port, connection_id, save_dir):
    dest_file_path = f"{save_dir}/{connection_id}.file"
    f_dest = open(dest_file_path, 'wb')
    connection.settimeout(10)
    try:
        input_data = connection.recv(BUFFER_SIZE)
    except Exception as e:
        f_dest.write(b'ERROR')
    while input_data:
        f_dest.write(input_data)
        if len(input_data) < BUFFER_SIZE:
            break
        input_data = connection.recv(BUFFER_SIZE)
    f_dest.close()
    connection.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File Server')
    parser.add_argument('port', type=int, help='listening port')
    parser.add_argument('path', type=str, help='file save directory')
    args = parser.parse_args()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = args.port
    save_path = args.path
    
    try:
        server_socket.bind((HOST, port))
    except Exception as e:
        sys.stderr.write("ERROR: " + str(e))
        sys.exit(PORT_BINDING_ERROR)

    server_socket.listen(5)
    
    while True:
        sys.stdout.write("Waiting for connections\n")
        connection, address = server_socket.accept()
        ip, port = str(address[0]), str(address[1])
        connection_count = connection_count + 1
        try:
            Thread(target=handle_connection, args=(connection, ip, port)).start()
        except Exception as e:
            sys.stderr.write("ERROR: " + str(e))
    soc.close()
