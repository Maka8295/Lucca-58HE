# SPDX-FileCopyrightText: 2001-2021 Python Software Foundation.All rights reserved.
# SPDX-FileCopyrightText: 2000 BeOpen.com. All rights reserved.
# SPDX-FileCopyrightText: 1995-2001 Corporation for National Research Initiatives.
#                         All rights reserved.
# SPDX-FileCopyrightText: 1995-2001 Corporation for National Research Initiatives.
#                         All rights reserved.
# SPDX-FileCopyrightText: 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
# SPDX-FileCopyrightText: 2021 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: Python-2.0

# Example of working with a `timedelta` object
# from https://docs.python.org/3/library/datetime.html#examples-of-usage-timedelta
from adafruit_datetime import timedelta

# Example of normalization
year = timedelta(days=365)
another_year = timedelta(weeks=40, days=84, hours=23, minutes=50, seconds=600)
print("Total seconds in the year: ", year.total_seconds())

# Example of timedelta arithmetic
year = timedelta(days=365)
ten_years = 10 * year
print("Days in ten years:", ten_years)

nine_years = ten_years - year
print("Days in nine years:", nine_years)

three_years = nine_years // 3
print("Days in three years:", three_years, three_years.days // 365)
