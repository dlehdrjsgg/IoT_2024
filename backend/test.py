import re
from datetime import datetime

text = "2027.10.21"

only_digits = re.sub(r'\D', '', text)


if len(only_digits) == 8:
    date = datetime.strptime(only_digits, '%Y%m%d').strftime('%Y-%m-%d')
elif len(only_digits) == 6:
    date = datetime.strptime(only_digits, '%y%m%d').strftime('%Y-%m-%d')
elif len(only_digits) == 4:
    date = datetime.strptime(only_digits, '%m%d').strftime('%Y-%m-%d')
else:
    date = only_digits
if (datetime.now() >= datetime.strptime(date, '%Y-%m-%d') or abs(datetime.now() - datetime.strptime(date, '%Y-%m-%d')).days > 730):
    print("Error")
    
print(date)