# High Level Design

## Server Program

The server program consists of 2 main parts.

* Main loop for accepting incoming connections
  
    Waits for client connections infinitely until SIGKILL or SIGTERM signal.

    Once a connection has arrived it makes a thread for handling data stream.

* Data stream handler
  
    Read data from the client and write to

## Client Program

The client program is a simple flow.

Connects to the server with a given host and port.

Use a buffer to send data to the server.

# Problems and Issues

* handling SIGNTERM, SIGKILL signals
  
  I referenced the following StackOverflow article to solve this issue.

  https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
  
* Argument parsing

  I referenced the following python manual to parse arguments.

  https://docs.python.org/3/library/argparse.html

# Additional Modules

* argparse
* signal
* threading
