import socket
import threading
from threading import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9998))
server.listen()
print("Waiting for connections...")
clients = []
groups = []


# --------------- Sub-class of threads---------#
class ServerThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.is_authenticate = False
        self.connection = None
        self.address = None
        self.user_group = None
        self.group_name = []
        self.users = []
        self.admin_list = []
        self.ban = []
        self.admin_pass_list = []
        self.password = None
        self.username = None

    def read_users(self, arg):
        # ----------------- Read a file of users ---------#
        # users = []
        if arg == 'user':
            self.users.clear()
            with open('users.txt') as textFile:
                for line in textFile:
                    # user temp var this thing will separate strings by empty string
                    user = [items.strip() for items in line.split(' ')]
                    self.users.append(user)

            # print('self.users:', self.users)
            # print(len(self.users))
        elif arg == 'ban':
            with open('ban.txt') as textFile:
                for line in textFile:
                    # user temp var this thing will separate strings by empty string
                    name = [items.strip() for items in line.split(' ')]
                    self.ban.append(name)

            # print('self.ban', self.ban)
            # print(len(self.ban))

    def create_group(self):
        # print('in crete')
        self.send_msg('Server: Enter Your User Name---:')
        user_name = self.rec_msg()
        self.send_msg("Server: Enter Your Password:--- ")
        self.password = self.rec_msg()
        # print(user_name, self.password)
        self.send_msg("Server: Enter Group Name: ")
        group_name = self.rec_msg()
        group_name_list = []

        # ------- Creates a list of Name of Groups in chat room ----------#

        for g in self.users:
            group_name_list.append(g[2])
            print('group name list', group_name_list)

        # ---- Checking if group name already exists or not -----------#

        while True:
            is_true = False
            for i in group_name_list:
                if i == group_name:
                    is_true = True
            if is_true:
                self.send_msg("Server: Group already Exists Try another :")
                self.send_msg("Server: Enter Group Name: ")
                group_name = self.rec_msg()
            else:
                break
        self.add_user(user_name, self.password, group_name, True)

    def add_user(self, user_name, password, group_name, is_admin):
        # ----- Add/write user in users.txt------#
        if is_admin:
            with open('users.txt', 'a') as dest_file:
                dest_file.write(user_name + ' ')
                dest_file.write(password + ' ')
                dest_file.write(group_name + ' ')
                dest_file.write('admin' + '\n')
                dest_file.close()
        else:
            with open('users.txt', 'a') as dest_file:
                dest_file.write(user_name + ' ')
                dest_file.write(password + ' ')
                dest_file.write(group_name + '\n')
                dest_file.close()
                return True

    def drive_menu(self):

        msg = "----Welcome To Chat Room---- \n"
        self.send_msg(msg)
        msg = "Press 1 to create group \n" \
              "Press 2 to Enter into Group"
        self.send_msg(msg)
        rec_msg = self.rec_msg()
        converted_int = int(rec_msg)
        # print(type(converted_int))
        if converted_int == 1:
            # print("In 1")
            self.read_users('user')
            self.create_group()
        elif converted_int == 2:
            return

    def broadcast(self, message, add):
        print("In broadcast function:", add)
        print('Groups of active clients:', groups)
        length = len(groups)
        l = len(clients)
        # ---- Searching for group name of sending client----#
        i = 0
        list_of_matched_groups = []
        name_of_group = None
        while i < length - 1:
            if groups[i] == add:
                name_of_group = groups[i + 1]
                break
            i = i + 1
        print("Group name :", name_of_group)

        # ----Find address of same group member of sending client-----#
        j = 0
        while j < length - 1:
            if name_of_group == groups[j + 1]:
                list_of_matched_groups.append(groups[j])
            j = j + 1
        # print("list of found add:", list_of_matched_groups)

        # -----Send message to only group members-----#

        print('Matched list:', list_of_matched_groups)
        # print('Clients:', clients)
        for val in list_of_matched_groups:
            k = 1
            # print("va:", val)
            while k < l:
                # print("value of k", k)
                # print("outside", val, '== ', clients[k])
                if val == clients[k]:
                    # print("In", val, '== ', clients[k])
                    clients[k - 1].send(bytes(message, 'utf-8'))
                k = k + 2

    def get_authentication(self):
        return self.is_authenticate

    def send_msg(self, msg):
        # print('In send_msg:', self.connection)
        self.connection.send(bytes(msg, 'utf-8'))

    def rec_msg(self):
        # print('In rec_msg:', self.connection)
        received = self.connection.recv(1024).decode()
        return received

    def is_Authenticate(self):
        while True:
            try:
                is_exist = False
                self.connection, self.address = server.accept()
                self.drive_menu()
                while not is_exist:
                    # ----------- Asking for User name--------------#

                    msg = "Enter you user name :"
                    self.send_msg(f'Server: {msg}')
                    self.username = self.rec_msg()
                    print(self.username, 'Trying to connect', self.address)

                    # ------------- Asking for Password---------------#
                    msg = "Enter password :"
                    self.send_msg(f'Server: {msg}')
                    self.password = self.rec_msg()

                    self.read_users('user')
                    users_group_name = []

                    # -------- Checking if username and password is correct----#

                    is_recognize = False
                    for data in self.users:
                        if data[0] == self.username and data[1] == self.password:
                            print("accept")
                            # --- Creating a list of groups in which client is a member----#
                            for user in self.users:
                                if user[0] == self.username and user[1] == self.password:
                                    is_exist = True
                                    users_group_name.append(user[2])

                            # ---Sending client names of group in which he/she is a member----#
                            self.read_users('ban')
                            # print('ban', self.ban)
                            while True:
                                is_banned = False
                                self.send_msg(f'Server: You are member of {users_group_name}\n'
                                              f'Enter Group name Which u want to enter:')
                                group_choice = self.rec_msg()
                                for choice in users_group_name:
                                    if choice == group_choice:
                                        for member in self.ban:
                                            if member[2] == group_choice and member[0] == self.username and member[
                                                1] == self.password:
                                                is_banned = True
                                                self.send_msg('you are banned in this group by admin....')
                                                break
                                        if not is_banned:
                                            self.send_msg("Connected Successfully....")
                                            clients.append(self.connection)
                                            clients.append(self.address)
                                            groups.append(self.address)
                                            # ----- Appending Group Name------#
                                            groups.append(group_choice)
                                            self.user_group = group_choice
                                            self.broadcast(f'{self.username} join the chat !', self.address)
                                            is_recognize = True
                                            break
                                if not is_recognize:
                                    self.send_msg("Server: Group Not Exist: \n")
                                if is_recognize:
                                    # print("Admin list")
                                    # print(data[-1])
                                    # print(type(data[-1]))
                                    if data[-1] == 'admin' and data[2] == group_choice:
                                        self.send_msg('---Congrats----')
                                        self.admin_list.append(self.address)

                                        # self.admin_list.append(data[-1])
                                        # print(self.admin_list)
                                    break
                            if is_recognize:
                                break
                    if not is_exist:
                        self.send_msg('Wrong password or username :')
                # print('outer loop')
                if is_recognize:
                    print("Thread starting")
                    thread_1 = threading.Thread(target=self.handle, args=(self.username, self.connection, self.address))
                    thread_1.start()
                    # print(users_group_name)
            except:
                print('connection:', self.connection)
                self.connection.close()
                break

    def handle(self, username, conn, add):
        # nameOfThread = current_thread().getName()
        while True:
            try:
                receivedMessage = conn.recv(1024).decode()
                print("Address of sending client:", add)
                print(receivedMessage)
                # print('admin list: ', self.admin_list)

                # ----------- Checks if User is admin or not and allowed to kick other users ------------#

                if receivedMessage == 'KICK' or receivedMessage == 'Kick' or receivedMessage == 'kick':
                    is_kicked = True
                    for names in self.admin_list:
                        if names == add:
                            self.kick_user(add, conn)
                            is_kicked = False
                            break
                    if is_kicked:
                        # print('In else of KIck')
                        conn.send(bytes('Server: Only admin is allowed to kick :)', 'utf-8'))
                elif receivedMessage == 'ADD' or receivedMessage == 'add' or receivedMessage == 'Add':
                    self.add_user_by_admin(add, conn)

                # ---- If other than Kick send msg to clients of groups----#
                else:
                    self.broadcast(f'{username}:{receivedMessage}', add)
            except:
                # print('Error occurred:')
                print('Before Closing connection clients', clients)
                index = clients.index(conn)
                conn.close()
                # print('index ', index)
                # clients.remove(clients[index])
                # clients.remove(clients[index])

                del clients[index]
                del clients[index]
                print('After Closing connection clients', clients)

                self.broadcast(f'{username} left the chat !', add)
                print('Before Closing connection:', groups)
                # print(add)

                indexs = groups.index(add)
                # print(indexs)
                # print(groups[indexs])
                del groups[indexs]
                # print(groups[indexs])
                del groups[indexs]

                print('After Closing connection :', groups)
                break

    def clients_group(self, add):
        length = len(groups)
        # ---- Searching for group name of sending client----#
        i = 0
        list_of_matched_groups = []
        while i < length - 1:
            if groups[i] == add:
                self.group_name = groups[i + 1]
                break
            i = i + 1
        print("Group name ---:", self.group_name)
        return self.group_name

    def kick_user(self, add, conn):
        try:
            # print('in else with:', add)
            print('In kick')
            self.group_name = self.clients_group(add)
            # for name in self.admin_list:
            is_banned = False
            ban_flag = False
            is_send_banned_msg = False

            # if name == add:
            # self.send_msg('Server: Enter name of user u want to ban :')

            conn.send(bytes('Server:Enter name of user u want to ban', 'utf-8'))
            msg = conn.recv(1024).decode()

            # print('rec msg:', msg)
            # print('self.username ', self.username)

            # ------------- Check if User is admin he will not ban himself-----------------------#
            # -----------------------------------------------------------------------------------#
            for members in self.users:
                # print('In loop---')
                # print(members[-1], members[0], members[2])
                if members[-1] == 'admin' and members[0] == msg and members[2] == self.group_name:
                    conn.send(bytes('Server: Admin is not allowed to kick himself....', 'utf-8'))
                    return

            # ----------- Check if user is already banned or not------------#
            # print('msg :', msg, ' ', 'username ', self.username)
            # self.read_users('ban')

            for member in self.ban:
                if member[0] == msg and member[2] == self.group_name:
                    conn.send(bytes(f'{member[0]} is already banned...', 'utf-8'))
                    # self.send_msg(f'{member[0]} is already banned...')
                    ban_flag = True
                    break

            # ---------Check in user list that entered user exist or not IF  exist then kick------------#
            if not ban_flag:
                self.read_users('user')
                for user in self.users:
                    # print(user[2])
                    # print(self.user_group)

                    if user[0] == msg and user[2] == self.group_name:
                        # print('users:', user[0], user[2])
                        with open('ban.txt', 'a') as ban_file:
                            ban_file.write(user[0] + ' ')
                            ban_file.write(user[1] + ' ')
                            ban_file.write(user[2] + '\n')
                            ban_file.close()
                            conn.send(bytes(f'{user[0]} banned successfully....', 'utf-8'))
                            # self.send_msg(f'{user[0]} banned successfully....')
                            is_banned = True
                            is_send_banned_msg = False
                        break
                # ****** if user does not found in list******#
                if not is_banned:
                    conn.send(bytes('User does not exist...', 'utf-8'))
                    # self.send_msg('User does not exist...')
        except:
            print('Error in kick')

    def add_user_by_admin(self, add, conn):

        self.read_users('user')
        list = []
        length = len(groups)
        # ---- Searching for group name of sending client----#
        i = 0
        list_of_matched_groups = []
        while i < length - 1:
            if groups[i] == add:
                self.group_name = groups[i + 1]
                break
            i = i + 1
        print("Group name ---:", self.group_name)

        for name in self.admin_list:
            if name == add:
                for users in self.users:
                    list.append(users[0])
                    list.append(users[2])
                # print(self.user_group)
                # print('users', self.users)
                #
                # print('names:', list)
                # ----------------$#
                # print(len(list))

                while True:
                    # print('In infinite loop ')
                    # print('self.address', self.address)
                    # print('add', add)
                    flag = False
                    i = 0
                    conn.send(bytes('Enter user name u want to add: ', 'utf-8'))

                    # conn.send((bytes('Enter user name you want to add :', 'utf-8'))
                    msg_rec = conn.recv(1024).decode()
                    print('msg_rec:', msg_rec)
                    while i <= len(list) - 1:
                        print('list', [i], ':', list[i])
                        # -----Need to improve con by adding AND --#
                        if msg_rec == list[i] and self.group_name == list[i + 1]:
                            flag = True
                            break

                        i = i + 2

                    if flag:
                        # self.send_msg('Username already exist try another one....')
                        conn.send(bytes('Username already exist try another one....', 'utf-8'))
                    else:
                        break

                # self.send_msg('Enter password for user:')
                conn.send(bytes('Enter password for user:', 'utf-8'))
                pass_msg = conn.recv(1024).decode()
                if self.add_user(msg_rec, pass_msg, self.group_name, False):
                    # self.send_msg("Successfully added")
                    conn.send(bytes('Successfully added', 'utf-8'))
                else:
                    # self.send_msg('Not Successfully added')
                    conn.send(bytes('Not Successfully added', 'utf-8'))


# --- i have to create a list of admins---#


# ------------ Here start main Thread/Main -----------#


# ------------------------------------------------------#


# ------------ Check if user is authenticating then start threads--------#


S = ServerThread()
S.is_Authenticate()
# S.join()
