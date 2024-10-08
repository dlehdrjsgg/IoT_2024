from lib import *
import xml.etree.ElementTree as ET

def getItem(barcode):
    with open('API_TOKEN', 'r') as f:
        API_TOKEN = f.read().strip()
    url = f"http://openapi.foodsafetykorea.go.kr/api/{API_TOKEN}/C005/xml/1/5/BAR_CD=" + str(barcode)
    print(url)
    response = requests.get(url).text
    print(response)
    root = ET.fromstring(response)
    prdlst_nm_list = [row.find('PRDLST_NM').text for row in root.findall('.//row')]
    if len(prdlst_nm_list) == 0:
        return "상품명을 찾을 수 없습니다."
    print(prdlst_nm_list[0])
    return prdlst_nm_list[0]

if __name__ == "__main__":
    getItem(8801121190197)