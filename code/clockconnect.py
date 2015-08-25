import socket
import threading
import display


class Server:
    def __init__(self, connection=('', 46692)):
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.bind(connection)
        self.main_socket.listen(1)

        self.accepting = True
        self.active_conn = None

        self.accept = threading.Thread(target=self.accept_conns)
        self.accept.start()

    def accept_conns(self):
        while self.accepting:
            conn, addr = self.main_socket.accept()
            if self.active_conn and self.active_conn.connected:
                self.active_conn.kill()
            self.active_conn = Cnxn(addr, conn)
            print('connnection accepted')

    def kill(self):
        self.accepting = False
        self.active_conn.kill()


class Cnxn:
    def __init__(self, connection, conn=None):
        self.address = connection
        if conn is None:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(connection)
        else:
            self.conn = conn
        self.connected = True
        self.pending_data = []

        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

    def kill(self, shutdown=True):
        self.connected = False
        if shutdown:
            self.conn.shutdown(socket.SHUT_WR)
        self.conn.close()

    def receive_data(self):
        while self.connected:
            data = ''
            try:
                data = self.conn.recv(512)
            except:
                self.kill(False)

            if data != '':
                display.clear()
                display.set_display_manual({0: (ord(data[0]) << 16) | (ord(data[1]) << 8) | ord(data[2])})
            else:
               self.kill(False)

    def send_data(self, data):
        self.conn.sendall(data)
