import socket
import os
    
# port number
port = 2222
client_socket = socket.socket()

# get IP Address
ipAddress = input("Enter a host name (URL) or IP address for the FTP server: ")

try:
    client_socket.connect((ipAddress, int(port)))
    # print welcome message
    print("Welcome to GCC FTP client!")
    print()

    # takes first command
    command = input("Command>> ")
    cmd = command.split(" ")

    while cmd[0].lower().strip() != 'quit':

        # LIST command
        if cmd[0].lower().strip() == 'list':
            # send command
            client_socket.send(bytes(command,'utf-8'))
            # get data
            data = client_socket.recv(1024).decode()
            # print data
            print(" FS: " + data)

        # RETR command
        if cmd[0].lower().strip() == 'retr':
            # send command
            client_socket.send(bytes(command,'utf-8'))
            # save filename
            filename = cmd[1]
            # check to see if the file exists
            response = client_socket.recv(1024).decode()
            # if file exists
            if (response == "True"):
                file = open(filename,'wb')
                while True:
                    try:
                        client_socket.settimeout(3.0)
                        data = client_socket.recv(1024)
                    except:
                        client_socket.settimeout(None)
                        break
                    file.write(data)
                file.close()
                print(" FS: " + filename + " retrieved")
            # if the file doesn't exist
            else:
                print(" FS: " + filename + " does not exist")

        # STOR command
        if cmd[0].lower().strip() == 'stor':
            # send command
            client_socket.send(bytes(command,'utf-8'))
            try:
                filename = cmd[1]
                file = open(filename,"rb")
                client_socket.send("True".encode('utf-8'))
                data = file.read(1024)
                client_socket.send(data)
                while data:
                    data = file.read(1024)
                    client_socket.send(data)
                file.close()
                response = client_socket.recv(1024).decode()
                if (response == "True"):
                    print(" FS: " + filename + " stored")
            except:
                client_socket.send("False".encode('utf-8'))
                print(" FS: " + filename + " does not exist")

        # SIZE command
        if cmd[0].lower().strip() == 'size':
            # send command
            client_socket.send(bytes(command,'utf-8'))
            # get data
            data = client_socket.recv(1024).decode()
            # print data
            print(" FS: " + data)

        # get next command
        command = input("Command>> ")
        cmd = command.split(" ")

    # close the connection
    client_socket.send(bytes(command,'utf-8'))
    client_socket.close()
    print('Connection terminated')


except:
    # failed to connect
    print("Failed to connect")
