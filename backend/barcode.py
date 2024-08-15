from lib import *
import pyzbar.pyzbar as pyzbar

def decode_barcode(frame):
    barcodes = pyzbar.decode(frame)
    data = False
    if len(barcodes) > 0:
        barcode = barcodes[0]
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        log.Infolog("BarcodeType " + barcodeType)
        log.Infolog("BarcodeData" + barcodeData)
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, barcodeData, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        data = barcodeData
    return frame, data

def read():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame,data = decode_barcode(frame)
        cv2.imshow('Barcode Scanner', frame)
        
        if cv2.waitKey(1) and data:
            time.sleep(1)
            break
    cap.release()
    cv2.destroyAllWindows()
    
    return data