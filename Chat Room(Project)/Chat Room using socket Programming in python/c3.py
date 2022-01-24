import socket
from threading import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host=socket.gethostname()
IP=socket.gethostbyname(host)
print(IP)
client.connect(('192.168.9.163', 9998))
print("Client is connected...")


# ---------------- Sub-class of Thread used for multi-threading ---------#
class ClientThrading(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.connection = conn

    def send_msg(self, msg):
        self.connection.send(bytes(msg, 'utf-8'))

    def rec_msg(self):
        received = self.connection.recv(1024).decode()
        return received

    def getauthenticate(self):
        return self.is_authenticate

    def run(self):
        nameOfThread = current_thread().getName()
        while True:
            if nameOfThread == 'Send':
                message = input()
                self.connection.send(bytes(message, 'utf-8'))
            elif nameOfThread == 'Receive':

                receivedMessage = self.connection.recv(1024).decode()
                print('Server :', receivedMessage)
                if receivedMessage == "Enter you user name :":
                    username = self.rec_msg()
                    print(username)
                    msg = input()
                    self.send_msg(msg)

                    password = self.rec_msg()
                    print(password)
                    msg = input()
                    self.send_msg(msg)

                    msg = self.rec_msg()
                    if msg == "Not found":
                        self.is_authenticate = True





# --------------Class for Acknowldgement that if user is right ------------------#


# ---------- Object of Authentication class-------------#
# print("Enter into Authenticate:")
# auth = Client_authen(client)
# auth.Authenticate()
#
# # ---------- Check if user is successfully recognized or not ------------#
# if auth.getauthenticate():
send = ClientThrading(client)
send.setName('Send')

receive = ClientThrading(client)
receive.setName('Receive')

send.start()
receive.start()
