from lib import *
import barcode
import ocr
import api

if __name__ == "__main__":
    while True:    
        with open('items.json', 'r', encoding="utf-8") as f:
            prev_data = json.load(f)
        barcodedata = barcode.read()
        deadline = ocr.main()
        timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        productName = api.getItem(barcodedata)
        
        if productName == "상품명을 찾을 수 없습니다.":
            log.Errorlog("상품명을 찾을 수 없습니다.")
            continue
        
        prev_data["items"].append({
            "barcode": barcodedata,
            "deadline": deadline,
            "productName": productName,
            "time": timenow
            })
        with open('items.json', 'w', encoding="utf-8") as f:
            json.dump(prev_data, f,ensure_ascii = False ,indent = 4)