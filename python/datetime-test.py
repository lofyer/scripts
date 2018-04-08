#!/usr/local/bin/python3
a = '11:00 AM'
b = datetime.strptime(a, '%I:%M %p')
b.strftime('%H:%M')
