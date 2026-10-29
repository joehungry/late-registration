import win32api

days = ['月','火','水','木','金','土']

class changeCourse:
    def __init__(self, classSchedule) -> None:
        self.classSc = classSchedule
        self.quarter = None
        self.quarterCourse = []
        self.day = None
        self.dayCourses = {}
    def chooseQuarter(self):
        print('変更のあるクォーターを選んでください：')
        for i in range(4):
            print(f'{i+1}. Q{i+1}')
        print()
        while True:
            one = win32api.GetKeyState(0x31)
            if one < 0:
                self.quarter = 1
                return None
            two = win32api.GetKeyState(0x32)
            if two < 0:
                self.quarter = 2
                return None
            three = win32api.GetKeyState(0x33)
            if three < 0:
                self.quarter = 3
                return None
            four = win32api.GetKeyState(0x34)
            if four < 0:
                self.quarter = 4
                return None
            back = win32api.GetKeyState(0x08)
            if back < 0:
                return 'back'
            
    def chooseDay(self):
        daysWithCourse = []
        dayBool = []
        input(self.classSc)
        for i in self.classSc:
            if i[3] == '-':
                pass
            elif not i[1] == str(self.quarter):
                pass
            elif i[2] in daysWithCourse:
                self.dayCourses[i[2:4]] = i[4:]
            else:
                self.dayCourses[i[2:4]] = i[4:]
                daysWithCourse.append(i[2])
                
        #input(self.dayCourses)
                
        #input(self.dayCourses)
        print('変更のある日にちを選んでください：')
        for ilen,i in enumerate(days):
            if i in daysWithCourse:
                print(f'{ilen+1}. {i}')
        testDay = None
        while True:
            one = win32api.GetKeyState(0x31)
            if one < 0:
                testDay = 0
            two = win32api.GetKeyState(0x32)
            if two < 0:
                testDay = 1   
            three = win32api.GetKeyState(0x33)
            if three < 0:
                testDay = 2
            four = win32api.GetKeyState(0x34)
            if four < 0:
                testDay = 3
            five = win32api.GetKeyState(0x35)
            if five < 0:
                testDay = 4
            six = win32api.GetKeyState(0x36)
            if six < 0:
                testDay = 5
            back = win32api.GetKeyState(0x08)
            if back < 0:
                return 'back'
            
            if testDay == None:
                pass
            elif testDay < len(daysWithCourse):
                self.day = days.index(daysWithCourse[testDay])
                return None
            else:
                testDay = None
            
        print()

