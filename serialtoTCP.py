import serial
import socket
import threading
import time
HOST = "0.0.0.0"
PORT = 9000
ADDR = (HOST, PORT)
isconn = False


def main():
    global isconn
    sock = socket.socket()
    sock.bind(ADDR)
    sock.listen(1)

    ser = serial.Serial("/dev/ttyUSB0", 115200)
    ser.flushInput()
    while True:
        conn, addr = sock.accept()
        print("cilent ip：", addr)

        t1 = threading.Thread(target=readcilent, args=(conn, ser,))
        t1.setDaemon(True)
        t1.start()
        t2 = threading.Thread(target=writecilent, args=(conn, ser,))
        t2.setDaemon(True)
        t2.start()


def readcilent(conn, serObj):
    while True:
        try:
            data = conn.recv(1024)
        except:
            conn.close()
            break
        if not data:
            conn.close()
            break
        serObj.write(data)


def writecilent(conn, serObj):

    while True:
        count = serObj.inWaiting()
        if count > 0:
            recv = serObj.read(count)
            try:
                conn.send(recv)
            except Exception as e:
                print(e)
                break
            else:
                serObj.flushInput()
        time.sleep(0.05)


if __name__ == '__main__':
    main()
