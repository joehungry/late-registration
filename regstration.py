# code: utf-8
import os
import csv
import glob
import getpass
import unicodedata, removePastCourse
from funcs import file, splice, num
from datetime import datetime

def opencourse(file):
    ilist = []
    with open(file, 'r', encoding='utf-8') as o:
        file_lines = o.readlines()
        return file_lines
    ilist = [i.strip() for i in file_lines]
    return file_lines

def stripList(list1):
    iliststrip = []
    add = ""
    for i in list1:
        if i == '\n' or i == '\t':
            iliststrip.append(add)
            add = ''
        elif i == '\u3000':
            pass
        else:
            add += i
    iliststrip.append(add)
    return iliststrip

def isitdate(date):
    format = "%Y/%m/%d"
    if date == '未決':
        return 'three'

    try:
        date = datetime.strptime(date, format)
        return True
    except ValueError:
        return False
    
def DELUnopenClass(courses):
    deleteIndex = None
    deleteIndex = []
    for ilen, i in enumerate(courses):
        if i == '不開講':
            deleteIndex.append(ilen-1)
    deletedElement = 0
    for i in deleteIndex:
        IndexToDelete = i - deletedElement
        for i in range(7):
            del courses[IndexToDelete]
            deletedElement += 1
    return courses

def courseorganize(inputList):
    starti = 0
    courseDict = {}
    days = ['月','火','水','木','金','土']
    while True:
        oneCourse = []
        if starti >= len(inputList)-1:
            break
        listwithrange = inputList[starti:]
        countdownNum = None
        for ilen,i in enumerate(listwithrange):
            dateBool = isitdate(i)
            if countdownNum == None:
                pass
            elif countdownNum == 0:
                starti += ilen + 1
                break
            else:
                countdownNum -= 1

            if dateBool == False:
                oneCourse.append(i)
            elif dateBool == 'three':
                countdownNum = 1
            else:
                starti += ilen + 1
                break
        dictKey = oneCourse[2]
        del oneCourse[2]
        del oneCourse[0]
        del oneCourse[0]
        
        for iLen, i in enumerate(oneCourse):
            for day in days:
                if day in i and 'Q' in i:
                    classLoc = iLen + 1
        for i in range(classLoc, len(oneCourse)):
            del oneCourse[classLoc]
        courseDict[dictKey] = (oneCourse)
    return courseDict

def isNum(number):
    try:
        int(number)
        return True
    except:
        return False
    
def delfromElement(thingToDeleteFrom, whichelement):
    listToDelete = list(thingToDeleteFrom)
    if whichelement == '*int*':
        boolthing = True
    elif whichelement == '*str*':
        boolthing = False
    
    for i in thingToDeleteFrom:
        if isNum(i) == boolthing:
            listToDelete.remove(i)
    addlist = ''
    for i in listToDelete:
        addlist += i
    return addlist

def compareCourses(pastCourses, coursesToselect, requiredCourses):
    allUnableDays = []
    allUnableDaysWithoutNum = []
    for selectedcoursekey, selectedcoursevalue in requiredCourses.items(): #this would get the courses days of the courses i took
        for i in selectedcoursekey:
            if isNum(i) == True:
                if '<国際科目群>' in selectedcoursekey:
                    selectedcoursekey = selectedcoursekey[:len(selectedcoursekey)-7]
                allUnableDaysWithoutNum.append(delfromElement(selectedcoursekey, '*int*'))
        for i in selectedcoursevalue: #this would deconstruct the courses and append it to a list
            allUnableDays.append(i) #couldnt use list comprehension because if i do that it includes the [] thing
    coursesYouDidntSelectYet = {}
    coursesYouDidSelect = []
    #input(allUnableDaysWithoutNum)
    for courseUnavaliable in allUnableDaysWithoutNum:
        for coursename1, coursedays1 in coursesToselect.items():
            if '<国際科目群>' in coursename1:
                compareCourse = coursename1[:len(coursename1)-7]
                compareCourses = delfromElement(compareCourse, '*int*')
            else:
                compareCourses = delfromElement(coursename1, '*int*')
            if compareCourses == courseUnavaliable:
                coursesYouDidSelect.append(coursename1)
    for coursename2, coursedays2 in coursesToselect.items():
        if not coursename2 in coursesYouDidSelect:
            coursesYouDidntSelectYet[coursename2] = coursedays2

        
    classesUnableToDo = []
    for coursename, coursedays in coursesYouDidntSelectYet.items(): #this is a very heavily nested code, so its hard to read,
        #input(coursename)
        for selectcourseday in coursedays: #but this would see the days in the course to selsect one by one
            for unavailabledays in allUnableDays: #and this would see the days already taken by other courses one by one
                if unavailabledays == selectcourseday: #this code finally checks if those two course dates do collide and if so,
                    if not coursename in classesUnableToDo: #would check if the class is already in the list or not,
                        classesUnableToDo.append(coursename) #then append it if not in the list. 
    for i in classesUnableToDo:#it would then check the unavailable courses, then delete them from the courses to select.
        del coursesYouDidntSelectYet[i]#it is done this way because its easier to find and append unavailable list rather than to do it for lists available, 
    return coursesYouDidntSelectYet #because even if you append the course once for being available, you dont know if the next date for the course is unavailable or not, so it would be a more complicated code, and i dont have time for that shit

def writeAndPrint(path, string):
    string = str(string)
    if string == '\n':
        print()
    else:
        print(string)
    with open(path, 'a', encoding= "utf_8") as o:
        if not string == '\n':
            o.writelines(string)
        o.writelines('\n')

                    
            

if __name__ == '__main__':
    removePastCourse.remove()
    fileNames = glob.glob('AllCourses/*.txt')
    takenCourses = glob.glob('AllCourses/requiredCourse/*.txt')
    fpastCourse = file.content('AllCourses/requiredCourse', 'allCourses.txt')
    rawPastCourseList = fpastCourse.fetch()
    pastCourseList = []
    for i in rawPastCourseList:
        lastWord = len(i)-1
        lastWordBool = False
        while lastWordBool == False:
            if num.isNum(i[lastWord]) == False:
                lastWordBool = True

            else:
                lastWord -= 1
        for elementLen,element in enumerate(i):
            if element == '[' or element == '＜' or element == '<':
                lastWord = elementLen
        lastWord += 1
        pastCourseList.append(i[:lastWord])


    courseList = []
    for i in fileNames:
        fileContent = opencourse(i)
        fileContent[len(fileContent)-1] = fileContent[len(fileContent)-1] + '\n'
        courseList = fileContent + courseList
    listedList = []
    for i in courseList:
        appendVar = list(i)
        for i  in appendVar:
            listedList.append(unicodedata.normalize('NFKC', i))
    strippedCourseList = stripList(listedList)
    courseOpen = DELUnopenClass(strippedCourseList)
    coursesWithOtherFaculty = courseorganize(courseOpen)
    coursesANDfaculty = {}
    coursesEVERYONEcanTAKE = {}
    for ikey, ivalue in coursesWithOtherFaculty.items():
        if '[' in ikey:
            uselessStr, facultyTemp = splice.splice(ikey, '[', 'str')
            facultyStr, uselessStr = splice.splice(facultyTemp, ']', 'str')
            facultyList = splice.toList(facultyStr, '・', 'str')
            coursesANDfaculty[ikey] = facultyList
        elif '<' in ikey:
            uselessStr, facultyTemp = splice.splice(ikey, '<', 'str')
            facultyStr, uselessStr = splice.splice(facultyTemp, '>', 'str')
            facultyList = splice.toList(facultyStr, '・', 'str')
            coursesANDfaculty[ikey] = facultyList
        else:
            coursesEVERYONEcanTAKE[ikey] = ivalue

    coursesWithMyFalulty = []
    for ikey, ivalue in coursesANDfaculty.items():
        if 'H' in ivalue or 'HP' in ivalue or '全' in ivalue or '仮登録用' in ivalue:
            coursesWithMyFalulty.append(ikey)

    coursesiCANtakePLUSstuffItook = {}
    for ikey, ivalue in coursesWithOtherFaculty.items():
        if ikey in coursesWithMyFalulty:
            coursesiCANtakePLUSstuffItook[ikey] = ivalue
    for ikey, ivalue in coursesEVERYONEcanTAKE.items():
            coursesiCANtakePLUSstuffItook[ikey] = ivalue

    coursesiCANtake = {}
    for ikey, ivalue in coursesiCANtakePLUSstuffItook.items():
        lastWord = len(ikey)-1
        lastWordBool = False
        while lastWordBool == False:
            if num.isNum(ikey[lastWord]) == False:
                lastWordBool = True
            else:
                lastWord -= 1
        for elementLen,element in enumerate(ikey):
            if element == '[':
                lastWord = elementLen
        lastWord += 1
        compareI = ikey[:lastWord]
        if not compareI in pastCourseList:
            coursesiCANtake[ikey] = ivalue


    fCourseData = file.content('AllCourses/requiredCourse', 'CourseData.txt')
    fileToCompareList = fCourseData.fetch()

    fileToCompare = {}
    dictContent = []
    courseName = None
    for i in fileToCompareList:
        if courseName == None:
            courseName = i
        elif i == 'done':
            fileToCompare[courseName] = dictContent
            courseName = None
            dictContent = []
        else:
            dictContent.append(i)

    attendableCorses = compareCourses(None ,coursesiCANtake, fileToCompare)

    attendableCorsesFinal = {}
    sortedAttendableCorses = sorted(attendableCorses.items(), key=lambda kv:(kv[1], kv[0]))
    for i in range(len(sortedAttendableCorses)):
        attendableCorsesFinal[sortedAttendableCorses[i][0]] = sortedAttendableCorses[i][1]

    if os.path.exists('履修登録可能な科目.txt'):
            os.remove('履修登録可能な科目.txt')
    print('履修登録可能な科目：')
    quarter = None
    for course, date in attendableCorsesFinal.items():
        if quarter == date[0][0:2]:
            pass
        elif quarter == None:
            print()
        else:
            writeAndPrint('履修登録可能な科目.txt', '\n')
            
        if not quarter == date[0][0:2]:
            quarter = date[0][0:2]
            writeAndPrint('履修登録可能な科目.txt', quarter)
            writeAndPrint('履修登録可能な科目.txt', '\n')
        writeAndPrint('履修登録可能な科目.txt', f'{course} {date}')
    input()
    os.popen('cd C:/Users/zoosl/OneDrive/デスクトップ/履修登録')
    os.popen('start 履修登録可能な科目.txt')
    while True:
        abc = getpass.getpass('')