from pyzbar.pyzbar import decode
from PIL import Image
import os
import numpy as np
import cv2

class QRdecoder:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def reader(self):
        while(True):
            ret, frame = self.cap.read()
            cv2.imshow('frame', frame)
            qr_data = decode(Image.fromarray(frame))

            if len(qr_data) > 0:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                return -1
        self.cap.release()
        cv2.destroyAllWindows()
        return qr_data[0][0].decode('utf-8', 'ignore')

if __name__ == "__main__":
    qr = QRdecoder()
    read_data = qr.reader()
    print(read_data)