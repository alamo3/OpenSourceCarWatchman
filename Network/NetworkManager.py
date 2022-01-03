from requests import get
import socket

COMM_PORT = 52345  #seriously, just chose this randomly

class NetworkManager:

    def __init__(self):
        self.ip = get('https://api.ipify.org').content.decode('utf8')
        print("IP Address of this network is: {0}".format(self.ip))

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        self.device_ip = s.getsockname()[0]
        print("Local IP Address of this device is: {0}".format(self.device_ip))
        s.close()



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

        sock.bind((self.device_ip, COMM_PORT))
        sock.settimeout(3.0)
        try:
            data, address = sock.recvfrom(4096)
            print(data.decode('utf-8'))

            sock.sendto(bytes("Hello client"), address)

        except:
            print("No data received, faulty connection?")


        sock.close()



