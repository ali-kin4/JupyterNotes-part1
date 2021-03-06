import re
import datetime

class Christian:

    def __init__(self, *date):
        # Parse date
        if len(date) == 1:
            date = date[0]
            if isinstance(date, str) == True:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', date)
                if m:
                    [year, month, day] = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
                else:
                    raise Exception("Invalid Input String")
            elif isinstance(date, datetime.date) == True:
                [year, month, day] = [date.year, date.month, date.day]
            elif isinstance(date, tuple) == True:
                year, month, day = date
                year = int(year)
                month = int(month)
                day = int(day)
            else:
                raise Exception("Invalid Input Type")
        elif len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        else:
            raise Exception("Invalid Input")

        # Check the validity of input date
        try:
            datetime.datetime(year, month, day)
        except:
            raise Exception("Invalid Date")

        self.christian_year = year
        self.christian_month = month
        self.christian_day = day

        # Convert date to Jalali
        d_4 = year % 4
        g_a = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        doy_g = g_a[month] + day
        if d_4 == 0 and month > 2:
            doy_g += 1
        d_33 = int(((year - 16) % 132) * .0305)
        a = 286 if (d_33 == 3 or d_33 < (d_4 - 1) or d_4 == 0) else 287
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 10) / 63) == 30:
            a -= 1
            b += 1
        if doy_g > b:
            jy = year - 621
            doy_j = doy_g - b
        else:
            jy = year - 622
            doy_j = doy_g + a
        if doy_j < 187:
            jm = int((doy_j - 1) / 31)
            jd = doy_j - (31 * jm)
            jm += 1
        else:
            jm = int((doy_j - 187) / 30)
            jd = doy_j - 186 - (jm * 30)
            jm += 7
        self.persian_year = jy
        self.persian_month = jm
        self.persian_day = jd

    def persian_tuple(self):
        if (self.persian_month < 10):
            self.persian_month = '0' + str(self.persian_month)
        if (self.persian_day < 10):
            self.persian_day = '0' + str(self.persian_day)
        return self.persian_year, self.persian_month, self.persian_day

    def persian_string(self, date_format="{}-{}-{}"):
        if (self.persian_month < 10):
            self.persian_month = '0' + str(self.persian_month)
        if (self.persian_day < 10):
            self.persian_day = '0' + str(self.persian_day)
        return date_format.format(self.persian_year, str(self.persian_month), str(self.persian_day))

class Persian:

    def __init__(self, *date):
        # Parse date
        if len(date) == 1:
            date = date[0]
            if isinstance(date, str) == True:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', date)
                if m:
                    [year, month, day] = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
                else:
                    raise Exception("Invalid Input String")
            elif isinstance(date, tuple) == True:
                year, month, day = date
                year = int(year)
                month = int(month)
                day = int(day)
            else:
                raise Exception("Invalid Input Type")
        elif len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        else:
            raise Exception("Invalid Input")

        # Check validity of date. TODO better check (leap years)
        if year < 1 or month < 1 or month > 12 or day < 1 or day > 31 or (month > 6 and day == 31):
            raise Exception("Incorrect Date")

        self.persian_year = year
        self.persian_month = month
        self.persian_day = day

        # Convert date
        d_4 = (year + 1) % 4
        if month < 7:
            doy_j = ((month - 1) * 31) + day
        else:
            doy_j = ((month - 7) * 30) + day + 186
        d_33 = int(((year - 55) % 132) * .0305)
        a = 287 if (d_33 != 3 and d_4 <= d_33) else 286
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 19) / 63) == 20:
            a -= 1
            b += 1
        if doy_j <= a:
            gy = year + 621
            gd = doy_j + b
        else:
            gy = year + 622
            gd = doy_j - a
        for gm, v in enumerate([0, 31, 29 if (gy % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
            if gd <= v:
                break
            gd -= v

        self.christian_year = gy
        self.christian_month = gm
        self.christian_day = gd

    def christian_tuple(self):
        if (self.christian_month < 10):
            self.christian_month = '0' + str(self.christian_month)
        if (self.christian_day < 10):
            self.christian_day = '0' + str(self.christian_day)
        return self.christian_year, self.christian_month, self.christian_day

    def christian_string(self, date_format="{}-{}-{}"):
        if (self.christian_month < 10):
            self.christian_month = '0' + str(self.christian_month)
        if (self.christian_day < 10):
            self.christian_day = '0' + str(self.christian_day)
        return date_format.format(self.christian_year, self.christian_month, self.christian_day)

    def christian_string2(self, date_format="{}{}{}"):
        if (self.christian_month < 10):
            self.christian_month = '0' + str(self.christian_month)
        if (self.christian_day < 10):
            self.christian_day = '0' + str(self.christian_day)
        return date_format.format(self.christian_year, self.christian_month, self.christian_day)

    def christian_datetime(self):
        if (self.christian_month < 10):
            self.christian_month = '0' + str(self.christian_month)
        if (self.christian_day < 10):
            self.christian_day = '0' + str(self.christian_day)
        return datetime.date(self.christian_year, self.christian_month, self.christian_day)
