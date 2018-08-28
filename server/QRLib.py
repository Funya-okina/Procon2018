from pyzbar.pyzbar import decode
import qrcode
from PIL import Image
import os
import numpy as np
import cv2

class decodeQR:
    def __init__(self, camera_id):
        self.cap = cv2.VideoCapture(camera_id)

    def decoder(self):
        while(True):
            ret, frame = self.cap.read()
            cv2.imshow('frame', frame)
            qr_data = decode(Image.fromarray(frame))

            if len(qr_data) > 0:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                return None
        self.cap.release()
        cv2.destroyAllWindows()
        return qr_data[0][0].decode('utf-8', 'ignore')


class encodeQR:
    def __init__(self):
        self.qr = qrcode.QRCode()

    def encoder(self, data, path, file_name):
        self.qr.add_data(data)
        self.qr.make()
        img = self.qr.make_image()
        img.save(r"{}/{}".format(path, file_name))



if __name__ == "__main__":
    qr = decodeQR(0)
    read_data = qr.decoder()
    print(read_data)