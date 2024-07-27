# SPDX-FileCopyrightText: 2001-2021 Python Software Foundation.All rights reserved.
# SPDX-FileCopyrightText: 2000 BeOpen.com. All rights reserved.
# SPDX-FileCopyrightText: 1995-2001 Corporation for National Research Initiatives.
#                         All rights reserved.
# SPDX-FileCopyrightText: 1995-2001 Corporation for National Research Initiatives.
#                         All rights reserved.
# SPDX-FileCopyrightText: 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
# SPDX-FileCopyrightText: 2021 Brent Rubell for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: Python-2.0

# Example of working with a `datetime` object
# from https://docs.python.org/3/library/datetime.html#examples-of-usage-datetime
from adafruit_datetime import datetime, date, time

# Using datetime.combine()
d = date(2005, 7, 14)
print(d)
t = time(12, 30)
print(datetime.combine(d, t))

# Using datetime.now()
print("Current time (GMT +1):", datetime.now())

# Using datetime.timetuple() to get tuple of all attributes
dt = datetime(2006, 11, 21, 16, 30)
tt = dt.timetuple()
for it in tt:
    print(it)

print("Today is: ", dt.ctime())

iso_date_string = "2020-04-05T05:04:45.752301"
print("Creating new datetime from ISO Date:", iso_date_string)
isodate = datetime.fromisoformat(iso_date_string)
print("Formatted back out as ISO Date: ", isodate.isoformat())
