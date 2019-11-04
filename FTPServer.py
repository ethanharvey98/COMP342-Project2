import socket, threading
import os

# print welcome message
print("Welcome to GCC FTP service!")
print("Waiting for client commands..")
# ipaddress
ipAddress = "10.23.102.47"
# port number
port = 2222
server = socket.socket()
server.bind((ipAddress, port))

while True:
    server.listen(1)
    client_socket, clientAddress = server.accept()

    cmd = ''
    while True:
        cmd = ''
        command = client_socket.recv(1024).decode()
        # breaks command into array of strings
        cmd = command.split(' ')

        if (len(command)>0):

            # LIST command
            if(cmd[0]=='list'):
                files = os.listdir(os.curdir)
                smg = ""
                for f in files:
                    smg = smg + "\n " + f
                client_socket.send(smg.encode('utf-8'))

            # RETR command
            elif(cmd[0]=='retr'):
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
                except:
                    client_socket.send("False".encode('utf-8'))

                    
            # STOR command
            elif(cmd[0]=='stor'):
                filename = cmd[1]
                # make sure file exists
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
                    client_socket.send("True".encode('utf-8'))
                    file.close()
                

            # SIZE command
            elif(cmd[0]=='size'):
                reqFile = cmd[1]
                statinfo = os.stat(reqFile)
                size = str(statinfo.st_size) + " bytes"
                client_socket.send(size.encode('utf-8'))

            # QUIT command
            elif (cmd[0]=="quit"):
                client_socket.close()
                break

    # if client quits
    print("Connection terminated by client...")
