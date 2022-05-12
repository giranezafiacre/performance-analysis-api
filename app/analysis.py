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
    
    marksDict=[]
    if(factor == '0'):  # teachers choice
        for i in ids:
            courseId = Course.objects.filter(name=course)[0]

            registration = Registration.objects.filter(
                student=Student.objects.get(id=i), courseGroup__course=courseId)[0]
            chosencoursegroup = registration.courseGroup
            coursegroup = CourseGroup.objects.get(id=chosencoursegroup.id)
            teacherId = coursegroup.teacher
            teacher = Teacher.objects.get(id=teacherId.id)
            teachers.append(teacher.id)
            marksDict.append([list(dataset[course])[ids.index(i)],teacher.id])
        
        x = pd.Series(list(dataset[course]))
        y = pd.Series(background)
        return {
            'correlation_result':x.corr(y),
            'marks_factors':marksDict
        }

    if(factor == '1'):  # backgrounds choice
        for i in ids:
            student = Student.objects.get(id=i)
            backId = student.backId
            background.append(backId.id)
            marksDict.append([list(dataset[course])[ids.index(i)],backId.id])
        
        x = pd.Series(list(dataset[course]))
        y = pd.Series(background)
        return {
            'correlation_result':x.corr(y),
            'marks_factors':marksDict
        }

    if(factor == '2'):  # disability choice
        for i in ids:
            student = Student.objects.get(id=i)
            disability.append(int(student.healthStatus))
            marksDict.append([list(dataset[course])[ids.index(i)],int(student.healthStatus)])
        
        x = pd.Series(list(dataset[course]))
        y = pd.Series(disability)
        return {
            'correlation_result':x.corr(y),
            'marks_factors':marksDict
        }

    if(factor == '3'):  # gender choice
        
        for i in ids:
            student = Student.objects.get(id=i)
            gender.append(int(student.gender))
            print(list(dataset[course])[ids.index(i)])
            marksDict.append([list(dataset[course])[ids.index(i)],int(student.gender)])
        
        x = pd.Series(list(dataset[course]))
        y = pd.Series(gender)
        return {
            'correlation_result':x.corr(y),
            'marks_factors':marksDict
        }

    if(factor == '4'):  # program choice
        for i in ids:
            student = Student.objects.get(id=i)
            program.append(int(student.program))
            marksDict.append([list(dataset[course])[ids.index(i)],int(student.program)])
        
        x = pd.Series(list(dataset[course]))
        y = pd.Series(program)
        return {
            'correlation_result':x.corr(y),
            'marks_factors':marksDict
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
