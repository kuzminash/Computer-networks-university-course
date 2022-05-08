import socket
import cv2

import info

sock = socket.socket()
sock.connect((info.HOST, info.PORT))

class DrawLineWidget(object):
    def __init__(self):
        self.image = cv2.cv2.imread(info.PATH)
        cv2.namedWindow('Local', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('Local', self.extract_coordinates)
        self.coordinates = []
        self.click = False

    def extract_coordinates(self, event, x, y, flags, userdata):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.coordinates = (x, y)
            self.click = True

        elif event == cv2.EVENT_LBUTTONUP:
            self.click = False

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.click:
                cv2.line(self.image, self.coordinates, (x, y), info.COLOUR, info.THICKNESS)
                cv2.imshow("Local", self.image)
                sock.send(f'{self.coordinates[0]} {self.coordinates[1]} {x} {y}.'.encode())

                self.coordinates = (x, y)


draw_line_widget = DrawLineWidget()
while True:
        cv2.imshow('Local', draw_line_widget.image)
        key = cv2.waitKey(1)
        if key == info.ESCAPE:
            cv2.destroyAllWindows()
            break
