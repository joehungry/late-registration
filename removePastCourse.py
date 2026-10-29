import os, glob
from datetime import datetime
from funcs import file, num, prints
from askDates import askPlan

def saveQuarterDate(quarterNum):
    while True:
        rawDate = prints.ask(f'Q{quarterNum}の最終日を設定してください')
        saveYear, saveMonth, saveDay = askPlan.checkDate(rawDate)
        if not saveYear == False:
            print(f'{saveYear}/{saveMonth}/{saveDay}')
            return f'{saveYear}/{saveMonth}/{saveDay}'
        os.system('cls')

def remove():
    nowDate = datetime.today()
    fsetting = file.content('setting', 'settings.txt')
    fqtrsetting = file.content('setting', 'quarterSettings.txt')
    fpastCourse = file.content('AllCourses/requiredCourse','CourseData.txt')
    fpastCourse.fetch()
    settings = fsetting.fetch()
    #deleteTextFiles = (glob.glob('AllCourses/*.txt'))

    quarterSetting = fqtrsetting.fetch()
    nowNum = num.numify(f'{nowDate.year} {nowDate.month} {nowDate.day}')
    q4Num = None
    quarterNow = 0
    actualNum = 0
    if not len(quarterSetting) == 0:
        quarterNow = int(quarterSetting[0])
        q4Num = num.numify(quarterSetting[len(quarterSetting)-1])

    change = False
    if quarterSetting == [] or nowNum >= q4Num:
        fpastCourse.delete('*file*')
        quarterSetting = fqtrsetting.fetch()
        q1 = saveQuarterDate(1)
        q2 = saveQuarterDate(2)
        q3 = saveQuarterDate(3)
        q4 = saveQuarterDate(4)
        fqtrsetting.delete('*file*')
        fqtrsetting.save(f'{actualNum}\n{q1}\n{q2}\n{q3}\n{q4}')
    quarterSetting = fqtrsetting.fetch()
    for ilen,i in enumerate(quarterSetting):
        qNum = num.numify(i)
        if qNum >= nowNum:
            actualNum = ilen
            break

    if not quarterNow == actualNum:
        change = True
        fsetting.delete('*file*')
        #for i in deleteTextFiles:
        #    os.remove(i)
        
    if change == True:
        quarters = fqtrsetting.fetch()

        fqtrsetting.delete('*file*')
        fqtrsetting.save(f'{actualNum}\n{quarters[1]}\n{quarters[2]}\n{quarters[3]}\n{quarters[4]}')

if __name__ == '__main__':
    pass