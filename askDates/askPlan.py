
import datetime, os
from askDates import month
from funcs import prints, splice, breakup, num


def askDate(text):
    dayList = []
    while True:
        date = prints.ask(text)
        if '-' in date:####日にちを連続させるプログラムを書かないと
            date1, date2 = splice.splice(date, '-', 'str')
            if date1 == '':
                firstYear, firstMonth, firstDay = True, True, True
            else:
                firstYear, firstMonth, firstDay = checkDate(date1)

            if date2 == '':
                pass
            elif not '/' in date2:
                date2 = f'{firstMonth}/{date2}'
            if not date2 == '':
                lastYear, lastMonth, lastDay = checkDate(date2)
            else:
                lastYear, lastMonth, lastDay = True, True, True
            if num.create(firstYear,firstMonth,firstDay)>num.create(lastYear,lastMonth,lastDay):
                lastYear += 1

            if lastYear == True and firstYear == True:
                pass
            elif not firstYear == False or not lastYear == False:
                dayList = firstYear, firstMonth, firstDay, lastYear, lastMonth, lastDay
                
                return dayList
            
def checkDate(date):
    today = datetime.date.today()
    if not '/' in date:
        return False, False, False
    year, monthAndDate = splice.splice(date, '/', "str")
    monthofPlan, dateofPlan = splice.splice(monthAndDate, "/", "int")#年が書いてある場合のプログラム
    if num.isNum(year) == False:
        return False, False, False
    if dateofPlan == False:#年が書いてない場合のプログラム
        monthofPlan = int(year)
        dateofPlan = int(monthAndDate)
        if num.create(today.year,year,monthAndDate)<num.create(today.year,today.month,today.day):
            year = today.year + 1#年が書いてなくて、日にちがもう過ぎてしまっている場合、予定日が来年に割り振られる。
        else:
            year = today.year#年が書いてなくて、日にちが過ぎていない場合、予定日に今年に割り振られる。
    if monthofPlan > 12:
        return False, False, False
    daysInMonth = month.checkDays(monthofPlan, year)
    if dateofPlan <= daysInMonth:
        return int(year), monthofPlan, dateofPlan
    return False, False, False


def askTime(text):
    while True:
        wasError = False
        numList = [i for i in range(0, 9)]
        planTime = prints.ask(text)
        if planTime == "start":
            return "0:00"
        elif planTime == 'end':
            return '23:59'
        os.system("cls")
        timeHour, timeMinute = breakup.time(planTime)
        if str(timeHour) == 'False':
            print(str(timeHour))
            prints.err('入力形式にエラーがあります')
        elif num.isNum(timeHour) == False or num.isNum(timeMinute) == False:
            prints.err('時間を入力してください')
        elif timeHour >= 24 or timeHour < 0:
            prints.err("入力された時間にエラーがあります")
        elif timeMinute >= 60 or timeMinute < 0:
            prints.err("入力された分数にエラーがあります")
        else:
            break
    if timeMinute < 10:
        timeMinute = '0' + str(timeMinute)
    return(f'{timeHour}:{timeMinute}')
