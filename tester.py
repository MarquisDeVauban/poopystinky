import datetime

from requests import NullHandler

dt = datetime.datetime.today()

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

month = 'null'

for thingy in months:
    if dt.month == 1 + months.index(thingy):
        month = months[months.index(thingy)]

print(f'{month}')
