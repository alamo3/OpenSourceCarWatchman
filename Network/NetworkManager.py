from requests import get
import socket

COMM_PORT = 52345  #seriously, just chose this randomly

class NetworkManager:

    def __init__(self):
        self.ip = get('https://api.ipify.org').content.decode('utf8')
        print("IP Address of this device is: {0}".format(self.ip))



    def get_ip_device(self):
        return self.ip

    def send_message(self, ip, message=None, port=None):

        if message is None:
            message = "Test message from {0}".format(self.ip)

        if port is None:
            port = COMM_PORT

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(message, 'utf-8'), (ip, port))

    def test_connectivity(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes("Test UDP request", 'utf-8'), ("127.0.0.1", 61115))

        sock.close()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("localhost", 18422))
        sock.settimeout(3.0)

        try:
            data = sock.recv(4096)
            print(data.decode('utf-8'))
        except:
            print("No data received, faulty connection?")


        sock.close()



