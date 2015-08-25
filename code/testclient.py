import socket
import threading


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
                print "GOT DATA"
            else:
               self.kill(False)

    def send_data(self, data):
        self.conn.sendall(data)


c = Cnxn(('192.168.1.21', 46692))
data = '\x00'*12
data += '\xff\x00\x00'*4
c.send_data(data)
