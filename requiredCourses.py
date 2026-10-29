# code: utf-8
import os
import csv
import getpass
from funcs import file, cli
from funcs import prints
import unicodedata
import win32api
import changeCourse, removePastCourse
import time

days = ['月','火','水','木','金','土']

def inputFunc(string):
    os.system('cls')
    print('必修科目入力')
    print()
    print(string + 'は何ですか？')
    return input('>> ')


def createClass(classes):
    perweek = None
    fileofOneClass = []
    while True:
        subject = unicodedata.normalize('NFKC', inputFunc('科目名'))
        if not subject in classes and not subject == '':
            break
        else:
            alreadyExists = getpass.getpass(f'''\033[91m{"もう登録してあります"}\033[0m''')
    while True:
        try:
            perweek = int(inputFunc('週に行う数とクォータ数をかけた数'))
            break
            quarter = None
        except ValueError:
            pass
        finally:
            if perweek == None:
                valerror = getpass.getpass(f'''\033[91m{"入力エラーがあります"}\033[0m''')

    timeperiodAppend = None
    timeperiod = []
    for i in range(perweek):
        while True:
            try:
                timeperiodAppend = unicodedata.normalize('NFKC', inputFunc('一つずつ教えてください。クォーターと時間割'))
                if timeperiodAppend in classes or timeperiodAppend in timeperiod:
                    pass
                elif not timeperiodAppend[0] == 'Q':
                    pass
                elif not int(timeperiodAppend[1]) in range(5) and not int(timeperiodAppend[1]) == 0:
                    pass
                elif not timeperiodAppend[2] in days:
                    pass
                elif int(timeperiodAppend[3]) in range(6) and not int(timeperiodAppend[3]) == 0:
                    timeperiod.append(timeperiodAppend)
                    timeperiodAppend = True
                    break
                timeperiodAppend = None
            except (ValueError, IndexError):
                pass
            finally:
                if not timeperiodAppend == True:
                    valerror = getpass.getpass(f'''\033[91m{'"Q1月1"のように入力してください'}\033[0m''')
                else:
                    timeperiodAppend = None
    fileofOneClass.append(subject)
    for i in timeperiod:
        fileofOneClass.append(i)
    fileofOneClass.append('done')
    return fileofOneClass

def sortTakenClass(classes):
    classdetail = []
    #input(classes)
    for classname, classday in classes.items():
        day = ''
        seperatedDays = []
        for lenofStr, i in enumerate(classday):
            day += i
            if lenofStr+1 == len(classday) or classday[lenofStr+1] == 'Q':
                seperatedDays.append(day)
                day = ''

        for day in seperatedDays:
            classdetail.append(f'{day}{classname}')
    #input(classdetail)

    badlysortedClassdetail = sorted(classdetail)
    wellsortedClassdetail = []
    for quarter in range(1,5):
        for day in days:
            thereIsClass = False
            for dateAndName in badlysortedClassdetail:
                if dateAndName[1] == str(quarter) and dateAndName[2] == day:
                    wellsortedClassdetail.append(dateAndName)
                    thereIsClass = True
            if thereIsClass == False:
                wellsortedClassdetail.append(f'Q{quarter}{day}-')

    
    #input(wellsortedClassdetail)  
    return wellsortedClassdetail
        

def showQuarter(quarters, dictClasses):
    schedule = sortTakenClass(dictClasses)
    daycheck = None
    for quarter in quarters:
        print(f'----------Q{quarter}----------')
        for dates in schedule:
            if not dates[1] == str(quarter):
                pass
            elif not daycheck == dates[2]:
                print()
                dateok = F'{dates[2]}'
            else:
                dateok = '　'

            if dates[1] == str(quarter):
                print(f'{dateok} {dates[3]}限 {dates[4:]}')
            daycheck = dates[2]
    
def fetchClassContent(filecontent):
        classname = None
        content = ""
        classdict = {}
        for i in filecontent:
            if classname == None:
                classname = i
            elif i == "done":
                classdict[classname] = content
                classname = None
                content = ''
            else:
                content += i
        return classdict

                


if __name__ == '__main__':
    while True:
        removePastCourse.remove()
        file.content('AllCourses')
        fpastCourse = file.content('AllCourses/requiredCourse', 'allCourses.txt')
        fCoursData = file.content('AllCourses/requiredCourse', 'CourseData.txt')
        fpastCourse.fetch()
        while True:
            fileOfclasses = []
            fileOfclasses = fCoursData.fetch()
            if fileOfclasses == None:
                fileOfclasses = []
            print("行いたいことを選択してください：")
            print("1.履修確定")
            print("2.履修確認")
            print("3.履修変更")
            todo = input(">> ")

            if todo == "1":
                while True:
                    fileOfclasses = fileOfclasses + createClass(fileOfclasses)
                    fCoursData.delete('*file*')
                    elementEQLdone =len(fileOfclasses)-2
                    itIsDone = False
                    while itIsDone == False:
                        elementEQLdone -= 1
                        if elementEQLdone == 0:
                            elementEQLdone -= 1
                            itIsDone = True
                        elif fileOfclasses[elementEQLdone] == 'done':
                            itIsDone = True
                    fpastCourse.save(fileOfclasses[elementEQLdone + 1])
                    for i in fileOfclasses:
                        fCoursData.save(i)
                    endOfInput = getpass.getpass('終わりです')
                    fileOfclasses = fCoursData.fetch()
                    if endOfInput == "end":
                        break

            elif todo == "2":
                dictClasses = fetchClassContent(fileOfclasses)
                print()
                print("何クォータの予定が見たいですか？")
                quarters = []
                try:
                    quarters.append(input(">> "))
                    int(quarters[len(quarters)-1])
                except ValueError:
                    quarters = [quarter for quarter in range(1,5)]
                
                os.system('cls')
                showQuarter(quarters, dictClasses)
                input()
                    
            elif todo == "3":
                quarterToChange = None
                periodToChange = None
                while True:
                    os.system('cls')
                    dictClasses = fetchClassContent(fileOfclasses)
                    tempSchedule = sortTakenClass(dictClasses)
                    #ass = changeCourse.changeCourse(tempSchedule)
                    #ass.chooseQuarter()
                    #time.sleep(0.065)
                    #ass.chooseDay()
                    #input('end..')
                    print('変更のあるクォーターを選んでください：')
                    for i in range(4):
                        print(f'{i+1}. Q{i+1}')
                    print('backspace. 戻る')
                    print()
                    while quarterToChange == None:
                        one = win32api.GetKeyState(0x31)
                        if one < 0:
                            quarterToChange = 1
                            break
                        
                        two = win32api.GetKeyState(0x32)
                        if two < 0:
                            quarterToChange = 2
                            break

                        three = win32api.GetKeyState(0x33)
                        if three < 0:
                            quarterToChange = 3
                            break
                        
                        four = win32api.GetKeyState(0x34)
                        if four < 0:
                            quarterToChange = 4
                            break

                        back = win32api.GetKeyState(0x08)
                        if back < 0:
                            quarterToChange = False
                            break

                    if quarterToChange == False:
                        break
                    time.sleep(0.12)
                    #input(tempSchedule)
                    sat = 0
                    compareSchedule = tempSchedule
                    pastnewone = []
                    for i1 in tempSchedule:
                        if not i1[3] == '-':
                            pastnewone.append(i1)
                        for i2 in compareSchedule:
                            if i1[4:] == i2[4:] and not i1 == i2 and not i1[3] == '-':
                                pastnewone.append(i2)
                                tempSchedule.remove(i2)
                    
                    newone = []
                    for i in pastnewone:
                        if int(i[1]) == quarterToChange:
                            newone.append(i)

                    weekdaysWithClass = []
                    for i in newone:
                        if i[3] == '-':
                            pass
                        elif not i[2] in weekdaysWithClass:
                            weekdaysWithClass.append(i[2])

                    os.system('cls')
                    weekdaysToChange = None
                    print(f'Q{quarterToChange}で変更のある曜日を選んでください：')
                    sortedWeekdaysWithClass = []
                    for i in days:
                        if i in weekdaysWithClass:
                            sortedWeekdaysWithClass.append(i)

                    dayNum = 0
                    for i in sortedWeekdaysWithClass:
                        dayNum += 1
                        print(f'{dayNum}. {i}')
                    if dayNum == 0:
                        input("登録された授業はありません")
                        weekdaysToChange = True
                        quarterToChange = None
                        periodToChange = False

                    while weekdaysToChange == None:
                        one = win32api.GetKeyState(0x31)
                        if not len(sortedWeekdaysWithClass) >= 0:
                            pass
                        elif one < 0:
                            weekdaysToChange = sortedWeekdaysWithClass[0]
                            break
                        
                        two = win32api.GetKeyState(0x32)
                        if not len(sortedWeekdaysWithClass) >= 0:
                            pass
                        elif two < 0:
                            weekdaysToChange = sortedWeekdaysWithClass[1]
                            break

                        three = win32api.GetKeyState(0x33)
                        if not len(sortedWeekdaysWithClass) >= 0:
                            pass
                        elif three < 0:
                            weekdaysToChange = sortedWeekdaysWithClass[2]
                            break
                        
                        four = win32api.GetKeyState(0x34)
                        if not len(sortedWeekdaysWithClass) >= 0:
                            pass
                        elif four < 0:
                            weekdaysToChange = sortedWeekdaysWithClass[3]
                            break

                        five = win32api.GetKeyState(0x34)
                        if not len(sortedWeekdaysWithClass) >= 0:
                            pass
                        elif five < 0:
                            weekdaysToChange = sortedWeekdaysWithClass[5]
                            break

                        six = win32api.GetKeyState(0x34)
                        if not len(sortedWeekdaysWithClass) >= 0:
                            pass
                        elif six < 0:
                            weekdaysToChange = sortedWeekdaysWithClass[6]
                            break
                        
                        back = win32api.GetKeyState(0x08)
                        if back < 0:
                            weekdaysToChange = True
                            quarterToChange = None
                            periodToChange = False
                            break
                    
                    
                    time.sleep(0.12)
                    print(True)
                    lastI = 'dowatisay'
                    listthing = {}
                    onestring = ''
                    for i in newone:
                        if not i[2] == weekdaysToChange:
                            pass
                        else:
                            listthing[int(i[3])] = i[4:]
                    
                    os.system('cls')
                    if periodToChange == None:
                        print('変更する授業をえらでください')
                        print()
                        for period, classname in listthing.items():
                                print(f'{period}限. {classname}')
                        while periodToChange == None:
                            
                            one = win32api.GetKeyState(0x31)
                            if not 1 in listthing.keys():
                                pass
                            elif one < 0:
                                periodToChange = 1
                                break
                            
                            two = win32api.GetKeyState(0x32)
                            if not 2 in listthing.keys():
                                pass
                            elif two < 0:
                                periodToChange = 2
                                break

                            three = win32api.GetKeyState(0x33)
                            if not 3 in listthing.keys():
                                pass
                            elif three < 0:
                                periodToChange = 3
                                break
                                
                            four = win32api.GetKeyState(0x34)
                            if not 4 in listthing.keys():
                                pass
                            elif four < 0:
                                periodToChange = 4
                                break

                            five = win32api.GetKeyState(0x34)
                            if not 5 in listthing.keys():
                                pass
                            elif five < 0:
                                periodToChange = 5
                                break

                            back = win32api.GetKeyState(0x08)
                            if back < 0:
                                weekdaysToChange = True
                                quarterToChange = None
                                periodToChange = False
                                whatToChange = 'false'
                                break
                        
                        thingsToChange = {'削除': 0}
                        time.sleep(0.12)
                        os.system('cls')
                        if not periodToChange == False:
                            print(f'{listthing[periodToChange]}にて、変更する項目を選んでください')
                            print()
                            cli.chooseScreen(thingsToChange)
                            whatToChange = None
                        while whatToChange == None:                            
                            one = win32api.GetKeyState(0x31)
                            if one < 0:
                                whatToChange = 1
                                break
                        if whatToChange == 'false':
                            chosenChange = 'false'
                        else:
                            chosenChange = cli.choosing(whatToChange, thingsToChange)
                        if chosenChange == 0:
                            startDelLen = None
                            courseData = fCoursData.fetch()
                            pastCourse = fpastCourse.fetch()
                            for ilen, i in enumerate(pastCourse):
                                print(i, listthing[periodToChange])
                                if i == listthing[periodToChange]:
                                    fpastCourse.delete(ilen)
                                    print(f'deleted {i}')
                                    input()

                            newCourseData = []
                            for ilen,i in enumerate(courseData):
                                if i == listthing[periodToChange]:
                                    startDelLen = ilen

                                if startDelLen == None:
                                    newCourseData.append(i)
                                elif i == 'done':
                                    startDelLen = None
                            saveChange = ''
                            for i in newCourseData:
                                saveChange += f'{i}\n'
                            fCoursData.save(saveChange, '*overwrite*', '*sameLN*')
                        if not chosenChange == 'false':
                            endOfInput = getpass.getpass('press ENTER')
                            dictClasses = fetchClassContent(fileOfclasses)
                            tempSchedule = sortTakenClass(dictClasses)                    
                    else:
                        periodToChange = None

            os.system('cls')