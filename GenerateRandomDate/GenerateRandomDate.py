import random
from datetime import datetime, timedelta, date

"""
生产随机的日期
"""


def get_months(years=1):
    """
    从当前时间开始遍历日期到 years年前
    :param years:
    :return:
    """
    # 获取当前时间
    current_time = datetime.now()

    # 设置一年前的日期
    one_year_ago = current_time - timedelta(days=365 * years)

    # 遍历月份
    current_month = current_time.replace(day=1)  # 将日期设置为当前月份的第一天

    dates = []
    while current_month > one_year_ago:
        # print(current_month.strftime("%Y-%m"))  # 打印格式为YYYY-MM的日期
        dates.append((current_month.year, current_month.month))
        # 减去一个月
        current_month = (current_month - timedelta(days=1)).replace(day=1)

    return dates


def get_random_dates(year, month, days, flag=False):
    """
    生产随机日期，年为year 月为month days 该月生产days天
    :param year:
    :param month:
    :param days:
    :return:
    """
    if month in (1, 3, 5, 7, 8, 10, 12):
        MAXDAY = 31
    elif month in (4, 6, 9, 11):
        MAXDAY = 30
    else:
        MAXDAY = 29

    dates = random.sample(range(1, MAXDAY), days)
    dates.sort()

    for day in dates:
        da = date(year=year, month=month, day=day)
        h = f"{random.randint(0, 23)}".rjust(2, "0")
        m = f"{random.randint(0, 59)}".rjust(2, "0")
        s = f"{random.randint(0, 59)}".rjust(2, "0")
        times = f"{h}:{m}:{s}"
        if flag:
            print(da, times)
        else:
            print(da)


def main():
    months = get_months(1)
    for month in months:
        # print(month)
        get_random_dates(month[0], month[1], 5, True)


if __name__ == '__main__':
    main()
