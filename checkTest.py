from funcs import file, prints
from askDates import askPlan
import requiredCourses, removePastCourse, calendar, os

removePastCourse.remove()
weekdays = ['月', '火', '水', '木', '金', '土']


if __name__ == '__main__':
    fCoursData = file.content('AllCourses/requiredCourse', 'CourseData.txt')
    fileOfclasses = fCoursData.fetch()
    dictclasses = requiredCourses.fetchClassContent(fileOfclasses)
    sortedClass = requiredCourses.sortTakenClass(dictclasses)

    fQuarterData = file.content('setting', 'quarterSettings.txt')
    quarterData = fQuarterData.fetch()
    quarterNow = str(quarterData[0])

    classesNow = []
    for i in sortedClass:
        if i[3] == '-':
            pass
        elif not i[1] == quarterNow:
            pass
        else:
            classesNow.append(i)

    for ilen, i in enumerate(classesNow):
        print(f'{ilen+1}. {i[4:]} ({i[2]})')
    classNum = int(input('>> '))-1
    classweekday = classesNow[classNum][3]
    classweekdayNum = classweekday.index(classweekday)
    classplanNum = prints.ask('何回目の授業ですか')

    print(calendar.monthcalendar(2024, 10))
    input()

    calendar.calendar
    
