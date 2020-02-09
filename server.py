#!/usr/bin/env python3

import sys, argparse, socket, time, signal
from threading import Thread

HOST = '127.0.0.1'
PORT_BINDING_ERROR = 1
BUFFER_SIZE = 2048
DEBUG = False

connection_count = 0
kill_now = False

def setKill(sig_num, stack_frame):
    global kill_now
    time.sleep(1)
    exit(0)

def handle_connection(connection, ip, port, connection_id, save_dir):
    
    DEBUG and print('handling connection: ', ip, port, connection_id, save_dir)    
    
    dest_file_path = f"{save_dir}/{connection_id}.file"
    f_dest = open(dest_file_path, 'wb')
    
    DEBUG and print('dest file path: ', f_dest)
    connection.settimeout(10)
    input_data = None
    try:
        input_data = connection.recv(BUFFER_SIZE)
    except Exception as e:
        DEBUG and print('recv exception: ', str(e))
        f_dest.write(b'ERROR')
    
    connection.settimeout(1)
    while input_data:
        f_dest.write(input_data)
        input_data = connection.recv(BUFFER_SIZE)
    
    f_dest.close()
    connection.close()
    
    DEBUG and print('closing connection handler')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File Server')
    parser.add_argument('port', metavar='PORT', type=int, help='listening port')
    parser.add_argument('path', metavar='FILE-DIR', type=str, help='file save directory')
    args = parser.parse_args()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = args.port
    save_path = args.path

    signal.signal(signal.SIGINT, setKill)
    signal.signal(signal.SIGTERM, setKill)

    try:
        server_socket.bind((HOST, port))
    except Exception as e:
        sys.stderr.write("ERROR: " + str(e))
        sys.exit(PORT_BINDING_ERROR)

    server_socket.listen(5)
    
    sys.stdout.write("Waiting for connections\n")
    while not kill_now:
        connection, address = server_socket.accept()
        ip, port = str(address[0]), str(address[1])
        DEBUG and print(f'connection from {ip}:{port}')
        connection_count = connection_count + 1
        try:
            Thread(target=handle_connection, args=(connection, ip, port, connection_count, save_path)).start()
        except Exception as e:
            sys.stderr.write("ERROR: " + str(e))
            DEBUG and print('exception in creating thread: ', str(e))
    soc.close()
