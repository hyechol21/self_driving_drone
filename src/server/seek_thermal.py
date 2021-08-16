import socket
import threading
import numpy as np
import cv2
from time import time


class SeekThermalServer:
    def __init__(self):
        self.host_name = 'Seek-Thermal Camera Socket Server'
        self.host = '141.223.122.51'
        self.port = 8487
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.isRun = False

    def run(self):
        t = threading.Thread(target=self.thread)
        t.daemon = True
        self.isRun = True
        t.start()

    def thread(self):
        print("-------- {}".format(self.host_name))
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)
        conn, addr = self.sock.accept()

        while self.isRun:
            try:
                print("Start Receiving Frame")
                # st = time.time()
                # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
                length = self.recvall(conn, 8)                      # Receive packet length
                stringData = self.recvall(conn, int(length))        # receive real data
                data = np.fromstring(stringData, dtype='uint8')     # convert to numpy array

                frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
                # cv2.imshow('Frame', frame)

                # TODO: Add Image Processor

                # TODO: Send to Data Queue

            except Exception as e:
                self.isRun = False
                print(e)
                print("-------- Close {}".format(self.host_name))

    def recvall(self, sock, count):
        # 바이트 문자열
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

