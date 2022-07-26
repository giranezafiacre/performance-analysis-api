from asyncio.windows_events import NULL
from math import isnan, nan
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import statistics

from app.models import BackgroundStudy, Course, CourseGroup, Registration, Student, Teacher

# from app.models import TemporaryCourses


def summaryize(dataset):
    return dataset.describe()


def correlationRes(filePath, course1, course2):
    dataset = pd.read_csv(filePath)
    x = pd.Series(dataset[course1])
    y = pd.Series(dataset[course2])
    return x.corr(y)


def histogram(filePath):
    dataset = pd.read_csv(filePath)
    degree_counts = dataset.columns.value_counts()
    dictionary = {}
    for i, key in enumerate(degree_counts):
        dictionary[degree_counts.keys()[i]] = statistics.mean(
            dataset[degree_counts.keys()[i]])
    print(dictionary)
    for i, key in enumerate(dictionary):
        plt.bar(i, dictionary[key])
        plt.xticks(numpy.arange(len(dictionary)),  dictionary.keys())
    return plt


def fileDetails(filepath):
    dataset = pd.read_csv(filepath)
    degree_counts = dataset.columns.value_counts()
    dictionary = {}
    for i, key in enumerate(degree_counts):
        if degree_counts.keys()[i] != 'Id':
            dictionary[degree_counts.keys()[i]] = statistics.mean(
                dataset[degree_counts.keys()[i]])
    print(dictionary)
    return dictionary


def normal_correlation(file, course, factor):
    ids = []
    teachers = []
    background = []
    disability = []
    gender = []
    program = []
    dataset = pd.read_csv(file)
    ids = list(dataset['Id'])
    marksArray = []

    if(factor == '0'):  # teachers choice
        courseId = Course.objects.filter(name=course)[0]
        print('courseId:', courseId)
        groups = CourseGroup.objects.filter(
            course=courseId.id)
        print('groups:', groups)
        teacherDict = {}
        TeacherArr = []
        for group in groups:
            print('group teacher:', group.teacher)
            print("_____________")
            groupArr = []
            successteacher = 0
            failedTeacher = 0
            for i in ids:
                courseId = Course.objects.filter(name=course)[0]
                if(Registration.objects.filter(student=Student.objects.get(id=i), courseGroup=group.id)):
                    teachers.append(group.teacher.id)
                    groupArr.append(list(dataset[course])[ids.index(i)])
                    print(i, ':et', group.teacher)
                    if(list(dataset[course])[ids.index(i)] >= 10):
                        successteacher = successteacher+1
                    else:
                        failedTeacher = failedTeacher + 1

            if(groupArr):
                teacherDict[f'{group.teacher}'] = statistics.mean(groupArr)
                teacherData = {}
                teacherData['name'] = f'{group.teacher}'
                teacherData['succeeded'] = successteacher
                teacherData['failed'] = failedTeacher
                print('teacherName:__', teacherData)
                TeacherArr.append(teacherData)
                print('teacherarr:__', TeacherArr)

        print('x:', list(dataset[course]))
        print('y:', teachers)
        x = pd.Series(list(dataset[course]))
        y = pd.Series(teachers)
        correlation = x.corr(y)
        if(isnan(correlation)):
            correlation = -2
        print('corr:', correlation)

        return {
            'correlation_result': correlation,
            'marks_factors': teacherDict,
            'data': TeacherArr
        }

    if(factor == '1'):  # backgrounds choice
        backgrounds = BackgroundStudy.objects.all()
        backDict = {}
        backgroundArr = []
        backgArr = []
        for background in backgrounds:
            backArr = []
            successBack = 0
            failedBack = 0
            for i in ids:
                student = Student.objects.get(id=i)
                backId = student.backId
                if(backId.id == background.id):
                    backArr.append(list(dataset[course])[ids.index(i)])
                    if(list(dataset[course])[ids.index(i)] >= 10):
                        successBack = successBack+1
                    else:
                        failedBack = failedBack + 1
            if(backArr):
                backDict[f'{background.major} {background.school}'] = statistics.mean(
                    backArr)
                backgData = {}
                backgData['name'] = f'{background.major} {background.school}'
                backgData['succeeded'] = successBack
                backgData['failed'] = failedBack
                backgArr.append(backgData)
                #
            backgroundArr.append(background.id)
        marksArray.append(backDict)

        x = pd.Series(list(dataset[course]))
        y = pd.Series(backgroundArr)
        print('backgArr:', backgArr)
        return {
            'correlation_result': x.corr(y),
            'marks_factors': backDict,
            'data': backgArr
        }

    if(factor == '2'):  # disability choice
        disDict = {}
        normalArr = []
        chronicArr = []
        disArr = []
        disabSuccess = 0
        disabFailed = 0
        normalSuccess = 0
        normalFailed = 0
        chronicSuccess = 0
        chronicFailed = 0
        normalDict = {}
        chronicDict = {}
        disabDict = {}
        for i in ids:
            student = Student.objects.get(id=i)
            disability.append(int(student.healthStatus))
            status = ''
            print(int(student.healthStatus))
            if(int(student.healthStatus) == 1):
                status = 'normal'
                normalArr.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] < 10):
                    normalFailed += 1
                else:
                    normalSuccess += 1
            if (int(student.healthStatus) == 2):
                status = 'chronic_disease'
                chronicArr.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] < 10):
                    chronicFailed += 1
                else:
                    chronicSuccess += 1
            if(int(student.healthStatus) == 3):
                status = 'disability'
                disArr.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] < 10):
                    disabFailed += 1
                else:
                    disabSuccess += 1

            marksArray.append(disDict)
        normalDict['name'] = 'normal'
        normalDict['succeeded'] = normalSuccess
        normalDict['failed'] = normalFailed

        chronicDict['name'] = 'chronic'
        chronicDict['succeeded'] = chronicSuccess
        chronicDict['failed'] = chronicFailed

        disabDict['name'] = 'disabled'
        disabDict['succeeded'] = disabSuccess
        disabDict['failed'] = disabFailed

        healthArr = [normalDict, chronicDict, disabDict]
        disDict['normal'] = statistics.mean(normalArr)
        disDict['chronic_disease'] = statistics.mean(chronicArr)
        disDict['disability'] = statistics.mean(disArr)
        x = pd.Series(list(dataset[course]))
        y = pd.Series(disability)
        print(marksArray)

        return {
            'correlation_result': x.corr(y),
            'marks_factors': disDict,
            'data': healthArr
        }

    if(factor == '3'):  # gender choice
        gendDict = {}
        maleArr = []
        femaleArr = []
        maleSuccess = 0
        maleFailed = 0
        femaleSuccess = 0
        femaleFailed = 0
        for i in ids:
            student = Student.objects.get(id=i)
            gender.append(int(student.gender))
            print(list(dataset[course])[ids.index(i)])
            gendStr = ''
            if(student.gender == '1'):
                gendStr = 'male'
                maleArr.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] < 10):
                    maleFailed += 1
                else:
                    maleSuccess += 1
            if(student.gender == '2'):
                gendStr = 'female'
                femaleArr.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] < 10):
                    femaleFailed += 1
                else:
                    femaleSuccess += 1
            marksArray.append(gendDict)
        maleDict = {}
        femaleDict = {}

        maleDict['name'] = 'male'
        maleDict['succeeded'] = maleSuccess
        maleDict['failed'] = maleFailed

        femaleDict['name'] = 'female'
        femaleDict['succeeded'] = femaleSuccess
        femaleDict['failed'] = femaleFailed

        gendDict['male'] = statistics.mean(maleArr)
        gendDict['female'] = statistics.mean(femaleArr)
        x = pd.Series(list(dataset[course]))
        y = pd.Series(gender)
        return {
            'correlation_result': x.corr(y),
            'marks_factors': gendDict,
            'data': [maleDict, femaleDict]
        }

    if(factor == '4'):  # program choice
        progDict = {}
        dayArr = []
        eveningArr = []
        daySuccess=0
        dayFailed=0
        eveningSuccess=0
        eveningFailed=0
        for i in ids:
            student = Student.objects.get(id=i)
            progStr = ''
            if(student.program == '1'):
                progStr = 'day'
                dayArr.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] < 10):
                    dayFailed += 1
                else:
                    daySuccess += 1
            if(student.program == '2'):
                progStr = 'evening'
                eveningArr.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] < 10):
                    eveningFailed += 1
                else:
                    eveningSuccess += 1
            program.append(int(student.program))
            marksArray.append(
                [f'{progStr},{int(student.program)}', list(dataset[course])[ids.index(i)]])
        print(marksArray)
        dayDict={}
        eveningDict={}
        
        dayDict['name'] = 'day'
        dayDict['succeeded'] = daySuccess
        dayDict['failed'] = dayFailed

        eveningDict['name'] = 'evening'
        eveningDict['succeeded'] = eveningSuccess
        eveningDict['failed'] = eveningFailed
        
        progDict['day'] = statistics.mean(dayArr)
        progDict['evening'] = statistics.mean(eveningArr)
        x = pd.Series(list(dataset[course]))
        y = pd.Series(program)
        correlation = x.corr(y)
        if(isnan(correlation)):
            correlation = -2

        return {
            'correlation_result': correlation,
            'marks_factors': progDict,
            'data':[dayDict,eveningDict]
        }


def OverviewAnalysis(file):
    print(file)
    dataset = pd.read_csv(file)
    ids = list(dataset['Id'])
    programDict = {
        'day': 0,
        'evening': 0,
    }
    healthDict = {
        'normal': 0,
        'chronic_disease': 0,
        'disability': 0
    }
    genderDict = {
        'male': 0,
        'female': 0
    }
    for i in ids:
        student = Student.objects.get(id=i)
        if(student.program == '1'):
            programDict['day'] += 1
        if(student.program == '2'):
            programDict['evening'] += 1
        if(student.healthStatus == '1'):
            healthDict['normal'] += 1
        if(student.healthStatus == '2'):
            healthDict['chronic_disease'] += 1
        if(student.healthStatus == '3'):
            healthDict['disability'] += 1
        if(student.gender == '1'):
            genderDict['male'] += 1
        if(student.gender == '2'):
            genderDict['female'] += 1
    return {'program': programDict, 'health': healthDict, 'gender': genderDict}


def genderHistoAnalysis(file):
    print(file)
    dataset = pd.read_csv(file)
    ids = list(dataset['Id'])
    degree_counts = dataset.columns.value_counts()
    courses = list(degree_counts.keys())
    courses.pop(0)
    gender_data = []
    for j in courses:
        male = []
        female = []
        marks = list(dataset[j])
        course_data = {}
        course_marks = {}
        for i in ids:
            student = Student.objects.get(id=i)
            if(student.gender == '1'):
                male.append(list(dataset[j])[ids.index(i)])
            if(student.gender == '2'):
                female.append(list(dataset[j])[ids.index(i)])
        course_data['male'] = statistics.mean(male)
        course_data['female'] = statistics.mean(female)
        course_marks[j] = course_data
        gender_data.append(course_marks)
    return gender_data


def teacherHistoAnalysis(file):
    dataset = pd.read_csv(file)
    ids = list(dataset['Id'])
    teachers = Teacher.objects.all()
    teacherDict = {}
    for t in teachers:
        coursesGroups = CourseGroup.objects.filter(teacher=t.id)
        if(coursesGroups):
            courseMarks = []
            for cg in coursesGroups:
                fRegistration = Registration.objects.filter(courseGroup=cg)

                if(fRegistration):
                    for rg in fRegistration:
                        marks = list(dataset[rg.courseGroup.course.name])
                        for id in ids:
                            if(id == rg.student.id):
                                courseMarks.append(marks[id-1])

                teacherDict[t.teacherName] = statistics.mean(courseMarks)
                print(t.teacherName, ":", statistics.mean(courseMarks))
    return teacherDict


def healthHistoAnalysis(file):
    print(file)
    dataset = pd.read_csv(file)
    ids = list(dataset['Id'])
    degree_counts = dataset.columns.value_counts()
    courses = list(degree_counts.keys())
    courses.pop(0)
    health_data = []
    for j in courses:
        normal = []
        chronic_disease = []
        disability = []
        marks = list(dataset[j])
        course_data = {}
        course_marks = {}
        for i in ids:
            student = Student.objects.get(id=i)
            if(student.healthStatus == '1'):
                normal.append(list(dataset[j])[ids.index(i)])
            if(student.healthStatus == '2'):
                chronic_disease.append(list(dataset[j])[ids.index(i)])
            if(student.healthStatus == '3'):
                disability.append(list(dataset[j])[ids.index(i)])
        course_data['normal'] = statistics.mean(normal)
        course_data['chronic_disease'] = statistics.mean(chronic_disease)
        course_data['disability'] = statistics.mean(disability)
        course_marks[j] = course_data
        health_data.append(course_marks)
    return health_data


def reportFileAnalysis(file):
    dataset = pd.read_csv(file)
    ids = list(dataset['Id'])
    degree_counts = dataset.columns.value_counts()
    courses = list(degree_counts.keys())
    courses.pop(courses.index('Id'))
    reportDict = {}
    for course in courses:
        courseDict = {}
        allSuccess = 0
        allFailed = 0
        maleSuccess = 0
        maleFailed = 0
        femaleSuccess = 0
        femaleFailed = 0
        normalSuccess = 0
        normalFailed = 0
        chronicSuccess = 0
        chronicFailed = 0
        disabSuccess = 0
        disabFailed = 0
        allMean = []
        maleMean = []
        femaleMean = []
        normalMean = []
        chronicMean = []
        disabMean = []
        for i in ids:
            student = Student.objects.get(id=i)
            # all
            allMean.append(list(dataset[course])[ids.index(i)])
            if(list(dataset[course])[ids.index(i)] >= 10):
                allSuccess += 1
            if(list(dataset[course])[ids.index(i)] < 10):
                allFailed += 1

                # male
            if(student.gender == '1'):
                maleMean.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] >= 10):
                    maleSuccess += 1
                if(list(dataset[course])[ids.index(i)] < 10):
                    maleFailed += 1

                    # female
            if(student.gender == '2'):
                femaleMean.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] >= 10):
                    femaleSuccess += 1
                if(list(dataset[course])[ids.index(i)] < 10):
                    femaleFailed += 1

                    # normal
            if(student.healthStatus == '1'):
                normalMean.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] >= 10):
                    normalSuccess += 1
                if(list(dataset[course])[ids.index(i)] < 10):
                    normalFailed += 1

                    # chronic diseases
            if(student.healthStatus == '2'):
                print('chronic:', student.fname, ':', chronicSuccess)
                chronicMean.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] >= 10):
                    chronicSuccess = chronicSuccess + 1
                if(list(dataset[course])[ids.index(i)] < 10):
                    chronicFailed += 1

                    # disabilities
            if(student.healthStatus == '3'):
                disabMean.append(list(dataset[course])[ids.index(i)])
                if(list(dataset[course])[ids.index(i)] >= 10):
                    disabSuccess += 1
                if(list(dataset[course])[ids.index(i)] < 10):
                    disabFailed += 1
        courseDict['allSuccess'] = allSuccess
        courseDict['allFailed'] = allFailed
        courseDict['femaleSuccess'] = femaleSuccess
        courseDict['femaleFailed'] = femaleFailed
        courseDict['maleSuccess'] = maleSuccess
        courseDict['maleFailed'] = maleFailed
        courseDict['normalSuccess'] = normalSuccess
        courseDict['normalFailed'] = normalFailed
        courseDict['chronicSuccess'] = chronicSuccess
        courseDict['chronicFailed'] = chronicFailed
        courseDict['disabSuccess'] = disabSuccess
        courseDict['disabFailed'] = disabFailed
        courseDict['allMean'] = "{:.2f}".format(statistics.mean(allMean))
        courseDict['maleMean'] = "{:.2f}".format(statistics.mean(maleMean))
        courseDict['femaleMean'] = "{:.2f}".format(statistics.mean(femaleMean))
        courseDict['normalMean'] = "{:.2f}".format(statistics.mean(normalMean))
        courseDict['chronicMean'] = "{:.2f}".format(
            statistics.mean(chronicMean))
        courseDict['disabMean'] = "{:.2f}".format(statistics.mean(disabMean))
        reportDict[course] = courseDict
    print(reportDict)
    return reportDict
