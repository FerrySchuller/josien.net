from datetime import datetime, timedelta
from dateparser import parse

settings = {'TO_TIMEZONE': 'GMT+1'}


print('{} {}'.format(int(datetime(2021, 5, 27, 17, 0).timestamp() * 1000), 'DC Cover Girls — Series 1'))
print('{} {}'.format(int(datetime(2021, 6, 10, 17, 0).timestamp() * 1000), 'Ron English - Cereal Killers - Series 1'))
print('{} {}'.format(int(datetime(2021, 6, 17, 17, 0).timestamp() * 1000), 'Superman — Series 1'))
print('{} {}'.format(int(datetime(2021, 6, 18, 2, 0).timestamp() * 1000), 'Ghostbusters Slimer'))
print('{} {}'.format(int(datetime(2021, 6, 21, 17, 0).timestamp() * 1000), 'Givenchy Beauty — PRIDE'))
print('{} {}'.format(int(datetime(2021, 6, 24, 17, 0).timestamp() * 1000), 'DC Bombshells — Series 2'))
print('{} {}'.format(int(datetime(2021, 7, 1, 17, 0).timestamp() * 1000), 'Frank Kozik Labbit— Series 1'))



l = [ { 'title': 'Frank Kozik Labbit— Series 1', 'dt': 'Thursday, July 1st at 8 am PT'},
      { 'title': 'Back to the Future Part II Hoverboards — Series 1', 'dt': 'Thursday, July 1st at 6 pm PT'} ]

for x in l:
    dt = parse(x['dt'], settings=settings)
    dt = dt + timedelta(hours=1)
    print("{{ x: {}, title: '{}' }}".format(int(dt.timestamp() * 1000), x['title']))
