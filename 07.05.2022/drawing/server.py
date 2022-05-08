import socket
import info
import cv2



sock = socket.socket()
sock.bind((info.HOST, info.PORT))
sock.listen()
c, addr = sock.accept()

image = cv2.cv2.imread(info.PATH)
cv2.namedWindow('Remote', cv2.WINDOW_AUTOSIZE)

while True:
    cv2.imshow('Remote', image)
    key = cv2.waitKey(1)
    if key == info.ESCAPE:
        cv2.destroyAllWindows()
        break
    rec = c.recv(1024)
    if rec:
        for line in rec.decode().split('.'):
            if len(line) == 0: break
            from_x, from_y, to_x, to_y = line.split()
            cv2.line(image, (int(from_x), int(from_y)), (int(to_x), int(to_y)), info.COLOUR, info.THICKNESS)
