#!/usr/bin/env python3

import sys, socket, time, argparse

CONNECTION_ERROR = 1
BUFFER_SIZE = 2048

DEBUG = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File Client')
    parser.add_argument('host', metavar='HOSTNAME-OR-IP', type=str, help='file server address')
    parser.add_argument('port', metavar='PORT', type=int, help='listening port')
    parser.add_argument('path', metavar='FILENAME', type=str, help='file save directory')

    args = parser.parse_args()
    host = args.host
    port = args.port
    file_path = args.path

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
    
    try:
        client_socket.connect((host, port))
    except Exception as e:
        sys.stderr.write('ERROR: ' + str(e))
        sys.exit(CONNECTION_ERROR)
    
    DEBUG and time.sleep(11)
    
    src_file = open(file_path, 'rb')
    input_data = src_file.read(BUFFER_SIZE)
    while input_data:
        try:
            client_socket.sendall(input_data)
        except Exception as e:
            sys.stderr.write("ERROR: " + str(e))
            exit(CONNECTION_ERROR)
        if len(input_data) < BUFFER_SIZE:
            break
        input_data = src_file.read(BUFFER_SIZE)
    src_file.close()
    client_socket.close()
