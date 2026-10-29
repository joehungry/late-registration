from funcs import file, compare, opdict, cli, prints, num
from datetime import datetime
import requiredCourses, win32api, time, os, removePastCourse
from askDates import askPlan

def changeQuarters(month):
    if month < 4:
        month += 12
    q1 = compare.isSandwitchNum(month, 4, 5)
    q2 = compare.isSandwitchNum(month, 6, 8)
    q3 = compare.isSandwitchNum(month, 9, 11)
    q4 = compare.isSandwitchNum(month, 11, 15)
    return [q1, q2, q3, q4]

def chooseVagueQuarter(quarterList):
    quarterEndDay = [None, None, 19, None]
    justdoit = int(quarterEndDay[int(quarterList[0])-1])
    if nowDate.day > justdoit:
        return quarterList[1]
    return str([quarterList[0]])

def chooseAbsentClass(indivisualClass, indClass):
    dayClassnow = indClass[indivisualClass]
    actualDayClass = file.fetchList(classAndDayDict[dayList[indivisualClass]], ',')
    activeClasses = []
    for i in actualDayClass:
        activeClasses.append(int(i[0]))
    activeClassesBool = []
    for ilen,i in enumerate(dayClassnow):
        if ilen+1 in activeClasses:
            activeClassesBool.append(True)
        else:
            activeClassesBool.append(False)
    newCount = 1
    oldCount = 0
    addCount = int(fsetting.fetch()[indivisualClass])
    while True:
        if newCount > oldCount:
            os.system('cls')
            fsetting.delete('*file*')
            for i in days.values():
                fsetting.save(i)
            for i in indClass.values():
                fsetting.saveList(i)
            for ilen, i in enumerate(actualDayClass):
                print(f'{i[0]}限{i[1:]} : {int(dayClassnow[int(i[0])-1])+addCount}回')
                
            time.sleep(0.3)

            oldCount = newCount

        one = win32api.GetKeyState(0x31)
        if one < 0 and activeClassesBool[0] == True:
            dayClassnow[0] = int(dayClassnow[0])
            dayClassnow[0] += 1
            newCount += 1
        
        two = win32api.GetKeyState(0x32)
        if two < 0 and activeClassesBool[1] == True:
            dayClassnow[1] = int(dayClassnow[1])
            dayClassnow[1] += 1
            newCount += 1

        three = win32api.GetKeyState(0x33)
        if three < 0 and activeClassesBool[2] == True:
            dayClassnow[2] = int(dayClassnow[2])
            dayClassnow[2] += 1
            newCount += 1
        elif three < 0:
            input('i')
        
        four = win32api.GetKeyState(0x34)
        if four < 0 and activeClassesBool[3] == True:
            dayClassnow[3] = int(dayClassnow[3])
            dayClassnow[3] += 1
            newCount += 1

        five = win32api.GetKeyState(0x35)
        if five < 0 and activeClassesBool[4] == True:
            dayClassnow[4] = int(dayClassnow[4])
            dayClassnow[4] += 1
            newCount += 1

        oneByOne = win32api.GetKeyState(0xA2) #ctrl key
        if oneByOne < 0:
            indClass[indivisualClass] = dayClassnow
            return indClass

def saveQuarterDate(quarterNum):
    while True:
        rawDate = prints.ask(f'Q{quarterNum}の最終日を設定してください')
        saveYear, saveMonth, saveDay = askPlan.checkDate(rawDate)
        if not saveYear == False:
            return f'{saveYear}/{saveMonth}/{saveDay}'
        os.system('cls')

def findKeyNum(hexNumStart, listName, element):
    if not element in listName:
        return 0
    else:
        return (hexNumStart+int(listName.index(element)))
    

if __name__ == '__main__':
    dayList = ['月', '火', '水', '木', '金', '土']
    days = {'月': 0,'火': 0,'水': 0,'木': 0,'金': 0,'土': 0}
    nowDate = datetime.today()
    fsetting = file.content('setting', 'settings.txt')
    fqtrsetting = file.content('setting', 'quarterSettings.txt')
    fpastCourse = file.content('requiredCourse','CourseData.txt')
    fpastCourse.fetch()
    settings = fsetting.fetch()

    removePastCourse.remove()

    quarterBool = changeQuarters(nowDate.month)
    #del settings[0]
    #input(settings)
    nowquarterList = []
    for ilen, i in enumerate(quarterBool):
        if i == True:
            nowquarterList.append(str(ilen+1))
    if len(nowquarterList) > 1:
        nowquarterList = chooseVagueQuarter(nowquarterList)
    
    fCoursData = file.content('AllCourses/requiredCourse', 'CourseData.txt')
    fileOfclasses = fCoursData.fetch()
    dictclasses = requiredCourses.fetchClassContent(fileOfclasses)
    sortedClass = requiredCourses.sortTakenClass(dictclasses)

    quarterClass = []
    for i in sortedClass:
        if not i[1] == str(nowquarterList[0]):
            pass
        else:
            quarterClass.append(i)

    fetchedstuff = fsetting.fetch()
    try:
        for ilen,i in enumerate(days.keys()):
            days[i] = int(fetchedstuff[ilen])
    except:
        pass
    
    indClass = {0: [0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0], 4: [0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0]}
    
    try:

        for i in range(5):
                indClass[i] = file.fetchList(fetchedstuff[len(days)+i], ',')
    except:
        pass

    dictkey = []
    dictvalue = []
    checkClassHasDay = []
    for i in quarterClass:
        dictkey.append(i[2:3])
        dictvalue.append(f'{i[3:]}')
        if i[3] == '-':
            checkClassHasDay = False
        else:
            checkClassHasDay = True
    classAndDayDict = opdict.create(dictkey, dictvalue)

    dictkeyCheck = []
    dictvalueCheck = []
    for i in quarterClass:
        dictkeyCheck.append(dayList.index(i[2:3]))
    
        dictvalueCheck.append(i[3])
    classAndDayCheck = opdict.create(dictkeyCheck, dictvalueCheck)
        

    #for idate, iabsentCount in indClass.items():#wtf is this shit
    #    resetAbsence = []
    #    for ilen, absence in enumerate(iabsentCount):
    #        if absence == '0':
    #            resetAbsence.append(int(absence))
    #        elif not str(ilen+1) in file.fetchList(classAndDayCheck[idate], ','):
    #            resetAbsence.append(0)
    #        else:
    #            resetAbsence.append(int(absence))
    #    indClass[idate] = resetAbsence


    for ikey, ivalue in classAndDayDict.items():
        if ivalue == '-':
            dayList.remove(ikey)

    newCount = 1
    oldCount = 0
    optionDict = {'休んだ日を見る': 0, '休んだ日設定': 1}
    while True:
        os.system('cls')
        rawOption = cli.chooseScreen(optionDict)
        rawOption = input('>> ')
        choosedOption = cli.choosing(rawOption, optionDict)
 
        if choosedOption == 0:
            classAbsentDict = {}
            dictkey = []
            dictvalue = []
            os.system('cls')
            for i in quarterClass:
                dictkey.append(i[4:])
                dictvalue.append(days[i[2:3]])

            for i in quarterClass:
                try:
                    dictvalue.append(indClass[dayList.index(i[2])][int(i[3])-1])
                except:
                    dictvalue.append(0)
                finally:
                    dictkey.append(i[4:])

            classCountDict = opdict.create(dictkey, dictvalue)

            addedValue = []
            for i in classCountDict.values():
                listr = file.fetchList(i, ',')
                addedStuff = 0
                for listvalue in listr:
                    addedStuff += int(listvalue)
                addedValue.append(str(addedStuff))

            classCountAddDict = opdict.create(classCountDict.keys(),addedValue)
            for ikey, ivalue in classCountAddDict.items():
                if not ikey == '':
                    print(f'{ikey}: 総合{ivalue}回')
                    print()
            input()

        if choosedOption == 1:
            while True:
                if newCount > oldCount:
                    os.system('cls')
                    fsetting.delete('*file*')
                    for i in days.values():
                        fsetting.save(i)
                    for i in indClass.values():
                        fsetting.saveList(i)
                    
                    classPeriod = 0
                    realLen = 0
                    for ilen, i in enumerate(days.items()):
                        addAll = 0
                        for classAbsent in indClass[ilen]:
                            addAll += int(classAbsent)
                        absentTimes = i[1]+(addAll/len(file.fetchList(classAndDayDict[i[0]], ',')))
                        #if absentTimes - int(absentTimes) == 0.0:
                        #    absentTimes = int(absentTimes)
                        if i[0] in dayList:
                            realLen += 1
                            print(f'{realLen}. {i[0]} : {round(absentTimes, 1)}回')
                    time.sleep(0.3)

                    oldCount = newCount

                oneByOne = win32api.GetKeyState(0x0D)
                if oneByOne < 0:
                    buffer = input()
                    os.system('cls')
                    time.sleep(0.0263)
                    breakone = 0
                    while True:
                        try:
                            for ilen, i in enumerate(dayList):
                                print(f'{ilen+1}. {i}')
                            print(f'{ilen+2}. 戻る')
                            print()
                            selectDay = int(input(">> "))-1
                            if selectDay == ilen+1:
                                breakone = 1
                                break
                            else:
                                dayList[selectDay]
                                break
                        except:
                            os.system('cls')
                    if breakone == 0:
                        indClass = chooseAbsentClass(selectDay, indClass)
                    time.sleep(0.15)
                    newCount += 1

                monday = win32api.GetKeyState(findKeyNum(49, dayList, '月'))
                if not '月' in dayList:
                    pass
                elif monday < 0:
                    days['月'] += 1
                    newCount += 1
                

                tuesday = win32api.GetKeyState(findKeyNum(49, dayList, '火'))
                if not '火' in dayList:
                    pass
                elif tuesday < 0:
                    days['火'] += 1
                    newCount += 1

                wednesday = win32api.GetKeyState(findKeyNum(49, dayList, '水'))
                if not '水' in dayList:
                    pass
                elif wednesday < 0:
                    days['水'] += 1
                    newCount += 1
                
                thursday = win32api.GetKeyState(findKeyNum(49, dayList, '木'))
                if not '木' in dayList:
                    pass
                elif thursday < 0:
                    days['木'] += 1
                    newCount += 1

                friday = win32api.GetKeyState(findKeyNum(49, dayList, '金'))
                if not '金' in dayList:
                    pass
                elif friday < 0:
                    days['金'] += 1
                    newCount += 1

                saturday = win32api.GetKeyState(findKeyNum(49, dayList, '土'))
                if not '土' in dayList:
                    pass
                elif saturday < 0:
                    days['土'] += 1
                    newCount += 1
        
        if choosedOption == 2:
            quarterSettng = fqtrsetting.fetch()
            if quarterSettng == []:
                pass