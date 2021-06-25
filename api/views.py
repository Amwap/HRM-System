from django.core.checks import messages
from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from django.http import HttpResponse, response
from django.db.models import Q
import operator
from functools import reduce

from credentials import smtp_login, smtp_password
import random
import smtplib
import datetime

# host = 'http://127.0.0.1:8000'
host = 'j7287160.myjino.ru'

def sendCode(request):
    try:
        code = random.randint(1000, 9999)
        to_email = request.GET['email']
        text = f'%s %s' % ('Your verification code', str(code))
        text = text.encode('ascii')
        password = smtp_password
        login = smtp_login

        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(login, password)
        smtpserver.sendmail(login, [to_email], text)
        return code
        # return 1234 # tpipest

    except:
        return None


class Login(View):
    """ Возвращает страницу авторизации """
    def get(self, request):
        if "login" in  request.GET:
            try:
                login = request.GET['login']
                password = request.GET['password']
                tutor = Tutor.objects.filter(login=login).first()
                if tutor.verify != 'complete':
                    tutor.delete()
                if tutor.password == password:
                    tutor.log_in = True
                    tutor.save()
                    print('AUTORIZATION')
                    return render(request, 'redirection.html', {'link': f'?login={login}'})

                else:
                    return render(request, 'login.html', {"link": f'/login', "text": "Неправильный логин <br> или пароль"})
            except:
                 return render(request, 'login.html', {"link": f'/login', "text": "Неправильный логин <br> или пароль"})

        return render(request, 'login.html', {"link": f'/login'})


class Registration(View):
    """ Возвращает страницу Регистрации """
    def get(self, request): 
        if "login" in  request.GET:
            try:
                code = sendCode(request)
                if code == None: raise Exception()
                tutor = Tutor(
                    name = request.GET['name'],
                    surename = request.GET['surename'],
                    patronymic = request.GET['patronymic'],
                    email = request.GET['email'],
                    phone = request.GET['phone'],
                    login = request.GET['login'],
                    password = request.GET['password'],
                    verify = code)
                tutor.save()
                return render(request, 'verify.html', {'link': f'/login'})
            except: pass

        elif 'code' in request.GET:
            tutor = Tutor.objects.filter(verify=request.GET['code']).first()
            if tutor == None: 
                return render(request, 'verify.html', {'text': "Неверный код верификации"})
            else:
                tutor.verify = 'complete' 
                tutor.save()
                return render(request, 'redirection.html', {'link': host})

        return render(request, 'registration.html')


class Autorization(View):
    """ Возвращает страницу Регистрации """
    def get(self, request): 
        try: 
            login = request.GET['login']
            tutor = Tutor.objects.filter(login=login).first()
            if tutor != None: return render(request, 'redirection.html', {'link': f'/?login={login}'})
            else: return render(request, 'login.html', {"link": f'/login'})
        except:
            return render(request, 'login.html', {"link": f'/login'})


class Main(View):
    """ Возвращает основной шаблон """
    def get(self, request): 
        if "login" in  request.GET:
            tutor = Tutor.objects.filter(login=request.GET['login']).first()
            if tutor == None: 
                return render(request, 'redirection.html', {'link': f'/login'})

            if tutor.log_in == False:
                return render(request, 'redirection.html', {'link': f'/login'})

            return render(request, 'index.html')
        else:
            return render(request, 'redirection.html', {'link': f'/login'})


class Api(View):
    """ Обрабатывает аргументы запроса """
    def get(self, request): 
        tutor = Tutor.objects.filter(login=request.GET['login']).first()
        if tutor != None:
            groups = Group.objects.filter(leader=tutor)
            self.permissions = []

            if len(groups) != 0: self.permissions.append('tutor')
            if tutor.specialist == 'да': self.permissions.append('spec')
            if tutor.admin == 'да': 
                self.permissions = []
                self.permissions.append('admin')

        if request.GET['element'] == 'checkRegistrationData':
            return self.checkRegistrationData(request)

        elif request.GET['element'] == 'panel':
            return self.sendPanel(request)

        elif request.GET['element'] == 'groupsTable':
            return self.sendGroupsTable(request)

        elif request.GET['element'] == 'tutorsTable':
            return self.sendTutorsTable(request)

        elif request.GET['element'] == 'studentsTable':
            return self.sendStudentsTable(request)

        elif request.GET['element'] == 'emptyStuffPage':
            return self.sendEmptyStuffPage(request)

        elif request.GET['element'] == 'emptyStudentPage':
            return self.sendEmptyStudentPage(request)

        elif request.GET['element'] == 'emptyGroupPage':
            return self.sendEmptyGroupPage(request)

        elif request.GET['element'] == 'emptyParentPage':
            return self.sendEmptyParentPage(request)

        elif request.GET['element'] == 'createStuff':
            return self.createStuff(request)

        elif request.GET['element'] == 'createStudent':
            return self.createStudent(request)

        elif request.GET['element'] == 'createGroup':
            return self.createGroup(request)

        elif request.GET['element'] == 'createParent':
            return self.createParent(request)

        elif request.GET['element'] == 'leader':
            return self.openStuff(request)

        elif request.GET['element'] == 'group':
            return self.openGroup(request)

        elif request.GET['element'] == 'student':
            return self.openStudent(request)

        elif request.GET['element'] == 'parent':
            return self.openParent(request)

        elif request.GET['element'] == 'deleteTutor':
            return self.deleteTutor(request)

        elif request.GET['element'] == 'deleteParent':
            return self.deleteParent(request)

        elif request.GET['element'] == 'deleteGroup':
            return self.deleteGroup(request)

        elif request.GET['element'] == 'deleteStudent':
            return self.deleteStudent(request)

        elif request.GET['element'] == 'searchQuery':
            return self.searchQuery(request)

        elif request.GET['element'] == 'groupStats':
            return self.statsPage(request)

        elif request.GET['element'] == 'exit':
            return self.exit(request)


    def exit(self, request):
        tutor = Tutor.objects.get(login=request.GET['login'])
        tutor.log_in = False
        tutor.save()
        return render(request, 'redirection.html', {'link': host})



    def statsPage(self, request):
        if request.GET['element_id'] == 'all':
            students = Student.objects.filter()
            head = 'Статистика по всем группам'

        elif request.GET['element_id'] != 'all':
            group = Group.objects.get(id=request.GET['element_id'])
            students = Student.objects.filter(group=group)
            head = f'Статистика группы: {group.name}'


        sections = students.exclude(sportsSections='')
        students_sections = [ i.sportsSections for i in sections]
        split_sections = [] 
        for i in students_sections: split_sections += i.split(' ')


        data = [
            ['Количество студентов', len(students)],
            ['Количество спортивных секций', len(set(split_sections))],
            ['Количество студентов', len(students_sections)],
            ['Количество семей (всего)', students.filter(amountOfChildren__range=(1, 9)).count()],
            ['Количество многодетных семей', students.filter(amountOfChildren__range=(3, 9)).count()],
            ['Количество не полных семей, где дети нуждаются в социальной поддержке', students.filter(fullFamily__range=(0, 1), juvenileAffairsUnit='да').count()],
            ['Дети сироты', students.filter(fullFamily=0).count()],
            ['Количество учащихся состоящих на внутреннем учёте', students.all().count()],
            ['Родители пенсионеры', students.filter(parentsArePensioners='да').count()],
        ]
        return render(request, 'pages/stats_page.html', {'data':data, 'head':head})

    def searchQuery(self, request):
        text = request.GET['data']

        if request.GET['subelement'] == 'studentsTable':
            headers = [
                    {'index':1, 'name':'ФИО'},
                    {'index':2, 'name':'email'},
                    {'index':3, 'name':'Телефон'},
                    {'index':4, 'name':'Группа'},
            ]
            fieldnames = ['name', 'surename', 'patronymic', 'patronymic', 'email', 'phone']

            if 'tutor' in  self.permissions:
                tutor = Tutor.objects.get(login=request.GET['login'])
                groups = Group.objects.filter(leader=tutor) 
                qgroup = reduce(operator.or_, (Q(**{fieldname: text}) for fieldname in fieldnames))
                asgns = Student.objects.filter(qgroup, group=groups[0])

            if ('admin' in self.permissions) or ('spec' in self.permissions):
                qgroup = reduce(operator.or_, (Q(**{fieldname: text}) for fieldname in fieldnames))
                asgns = Student.objects.filter(qgroup)
            
            return render(request, 'tables/students_table.html', {'headers': headers, 'students': asgns})


        elif request.GET['subelement'] == 'tutorsTable':
            headers = [
                    {'index':1, 'name':'ФИО'},
                    {'index':2, 'name':'Админ'},
                    {'index':3, 'name':'Специалист'},
                    {'index':4, 'name':'email'},
                    {'index':5, 'name':'Телефон'},
                #  {'index':6, 'name':'Группа'}
            ]
            fieldnames = ['name', 'surename', 'patronymic', 'email', 'phone', 'login']
            qgroup = reduce(operator.or_, (Q(**{fieldname: text}) for fieldname in fieldnames))
            asgns = Tutor.objects.filter(qgroup)
            
            return render(request, 'tables/tutors_table.html', { 'headers': headers, 'tutors': asgns})

        elif request.GET['subelement'] == 'groupsTable':
            headers = [
                    {'index':1, 'name':'Руководитель'},
                    {'index':2, 'name':'Группа'}
            ]
            fieldnames = ['name']

            if 'tutor' in  self.permissions:
                tutor = Tutor.objects.get(login=request.GET['login'])
                qgroup = reduce(operator.or_, (Q(**{fieldname: text}) for fieldname in fieldnames))
                asgns = Group.objects.filter(qgroup, leader=tutor)

            if ('admin' in self.permissions) or ('spec' in self.permissions):
                qgroup = reduce(operator.or_, (Q(**{fieldname: text}) for fieldname in fieldnames))
                asgns = Group.objects.filter(qgroup)


            return render(request, 'tables/group_table.html', {'groups': asgns, 'headers': headers})



    def checkRegistrationData(self, request):
        tutor_email = Tutor.objects.filter(email=request.GET['email']).first()
        student_email = Tutor.objects.filter(email=request.GET['email']).first()
        if (student_email == None) and (tutor_email == None):
            return HttpResponse('ok')

        else: return HttpResponse('Данный email уже зарегистрирован')
    
    def deleteStudent(self, request):
        student = Student.objects.get(id=request.GET['student_id'])
        name = student.name 
        student.delete()
        return HttpResponse(f'Студент "{name}" был удалён.')
        
    
    def deleteGroup(self, request):
        group = Group.objects.get(id=request.GET['group_id'])
        name = group.name
        group.delete()
        return HttpResponse(f'Группа "{name}" была удалён.')


    def deleteParent(self, request):
        parent = Parent.objects.get(id=request.GET['parent_id'])
        name = parent.getFIO()
        parent.delete()
        return HttpResponse(f'Пользователь "{name}" был удалён.')

    def deleteTutor(self, request):
        tutor = Tutor.objects.get(id=request.GET['tutor_id'])
        name = tutor.getFIO()
        tutor.delete()
        return HttpResponse(f'Пользователь "{name}" был удалён.')


    def openParent(self, request):
        parent = Parent.objects.get(id=request.GET['element_id'])
        student = parent.student
        return render(request, 'pages/parent_page.html', {'parent': parent, 'student': student})

    def openStuff(self, request):
        tutor = Tutor.objects.get(id=request.GET['element_id'])
        return render(request, 'pages/stuff_form.html', {'tutor': tutor})

    def openGroup(self, request):
        group = Group.objects.get(id=request.GET['element_id'])
        members = Student.objects.filter(group=group)
        if 'tutor' in  self.permissions:
            tutors = [Tutor.objects.get(login=request.GET['login'])]
            
        if ('admin' in self.permissions) or ('spec' in self.permissions):
            tutors = Tutor.objects.all()

        headers = [
                    {'index':1, 'name':'ФИО'},
                    {'index':2, 'name':'Email'},
                    {'index':3, 'name':'Телефон'},
                    {'index':4, 'name':'Группа'},
            ]

        return render(request, 'pages/group_page.html', {'tutors': tutors, 'group':group, 'students': members, 'headers': headers})

    def openStudent(self, request):
        student = Student.objects.get(id=request.GET['element_id'])
        parents = Parent.objects.filter(student=student)
        groups=''
        if 'tutor' in self.permissions:
            tutor = Tutor.objects.get(login=request.GET['login'])
            groups = Group.objects.filter(leader=tutor)

        if ('admin' in self.permissions):
            groups = Group.objects.all()

        return render(request, 'pages/student_form.html', {'student': student, 'parents':parents, 'user_query_id':f'&student={student.id}', 'groups': groups })


    def sendPanel(self, request):
        """ Возвращает главную панель """
        return render(request, 'panel.html', {'permissions': self.permissions})


    def sendGroupsTable(self, request):
        """ Возвращает таблицу группы + руководители """
        headers = [
                {'index':1, 'name':'Руководитель'},
                {'index':2, 'name':'Группа'}
        ]
        if 'tutor' in  self.permissions:
            tutor = Tutor.objects.get(login=request.GET['login'])
            groups = Group.objects.filter(leader=tutor)

        if ('admin' in self.permissions) or ('spec' in self.permissions):
            groups = Group.objects.all()

        if request.GET['sorted'] == 'sort_by_group':
            groups = sorted(groups, key=lambda x: x.name)

        if request.GET['sorted'] == 'sort_by_alphabet':
            groups = sorted(groups, key=lambda x: x.leader.getFIO())

        return render(request, 'tables/group_table.html', {'groups': groups, 'headers': headers})


    def sendTutorsTable(self, request):
        """ Возвращает таблицу стаффа """
        tutors = Tutor.objects.all()
        headers = [
                {'index':1, 'name':'ФИО'},
                {'index':2, 'name':'Админ'},
                {'index':3, 'name':'Специалист'},
                {'index':4, 'name':'email'},
                {'index':5, 'name':'Телефон'},
            #  {'index':6, 'name':'Группа'}
        ]


        if request.GET['sorted'] == 'sort_by_alphabet':
            tutors = sorted(tutors, key=lambda x: x.getFIO())
        return render(request, 'tables/tutors_table.html', { 'headers': headers, 'tutors': tutors})


    def sendStudentsTable(self, request):
        """ Возвращает таблицу со студентами """
        if 'tutor' in  self.permissions:
            tutor = Tutor.objects.get(login=request.GET['login'])
            groups = Group.objects.filter(leader=tutor) 
            students = Student.objects.filter(group=groups[0])

        if ('admin' in self.permissions) or ('spec' in self.permissions):
            students = Student.objects.all()

        headers = [
                {'index':1, 'name':'ФИО'},
                {'index':2, 'name':'email'},
                {'index':3, 'name':'Телефон'},
                {'index':4, 'name':'Группа'},
        ]
        if request.GET['sorted'] == 'sort_by_group':
            students = sorted(students, key=lambda x: x.group.name)

        if request.GET['sorted'] == 'sort_by_alphabet':
            students = sorted(students, key=lambda x: x.getFIO())

        return render(request, 'tables/students_table.html', {'headers': headers, 'students': students})

    def sendEmptyStuffPage(self, request):
        """ Возвращает пустую страницу стаффа"""
        return render(request, 'pages/stuff_form.html')


    def sendEmptyStudentPage(self, request):
        """ Возвращает пустую страницу студента """
        groups=''
        if 'tutor' in  self.permissions:
            tutor = Tutor.objects.get(login=request.GET['login'])
            groups = Group.objects.filter(leader=tutor)

        if ('admin' in self.permissions):
            groups = Group.objects.all()

        return render(request, 'pages/student_form.html',{"groups": groups, 'user_query_id': ''})

    def sendEmptyGroupPage(self, request):
        tutors = Tutor.objects.all()
        return render(request, 'pages/group_page.html', {"tutors": tutors, 'empty': True})

    def sendEmptyParentPage(self, request):
        student = Student.objects.get(id=request.GET['student'])
        return render(request, 'pages/parent_page.html', {'student': student})


    def createStuff(self, request):
        """ Создаёт участника стаффа """
        if request.GET['stuff_id'] not in ['undefined', '']:
            tutor = Tutor.objects.get(id=request.GET['stuff_id'])
            tutor.name=request.GET['name']
            tutor.surename=request.GET['surename']
            tutor.patronymic=request.GET['patronymic']
            tutor.phone=request.GET['phone']
            tutor.email=request.GET['email']
            tutor.note=request.GET['note']
            tutor.admin=request.GET['admin']
            tutor.specialist=request.GET['specialist']
            tutor.login=request.GET['login']
            tutor.password=request.GET['password']
            tutor.save()
            return HttpResponse("Пользователь обновлён.")

        else:
            request.GET['stuff_id'] == None
            warning = ''
            check_email = Tutor.objects.filter(email=request.GET['email']).first()
            check_login = Tutor.objects.filter(phone=request.GET['login']).first()
            if check_email != None: warning += 'Данный email уже зарегистрирован. '
            if check_login != None: warning += 'Данный логин уже зарегистрирован.'
            if warning != '': return HttpResponse(warning)
            tutor = Tutor(
                name=request.GET['name'],
                surename=request.GET['surename'],
                patronymic=request.GET['patronymic'],
                phone=request.GET['phone'],
                email=request.GET['email'],
                note=request.GET['note'],
                admin=request.GET['admin'],
                specialist=request.GET['specialist'],
                login=request.GET['login'],
                password=request.GET['password'],
            )
            tutor.save()
            return HttpResponse("Пользователь добавлен.")


    def createStudent(self, request):
        """ Создаёт студента """
        group_id = Group.objects.filter(id=request.GET['group']).first()
        if request.GET['student_id'] not in ['undefined', '']:
            student = Student.objects.get(id=request.GET['student_id'])
            student.name=request.GET["name"]
            student.surename=request.GET["surename"]
            student.patronymic=request.GET["patronymic"]
            student.email=request.GET["email"]
            student.phone=request.GET["phone"]
            student.note=request.GET["note"]
            student.group=group_id
            student.parentsArePensioners=request.GET["parentsArePensioners"]
            student.amountOfChildren=request.GET["amountOfChildren"]
            student.dateOfBirth=datetime.datetime.strptime(request.GET['dateOfBirth'], '%Y-%m-%d')
            student.cityOfRegistration=request.GET["cityOfRegistration"]
            student.cityOfResidence=request.GET["cityOfResidence"]
            student.gender=request.GET["gender"]
            student.juvenileAffairsUnit=request.GET["juvenileAffairsUnit"]
            student.fullFamily=request.GET["fullFamily"]
            student.interests=request.GET["interests"]
            student.sportsSections=request.GET["sportsSections"]
            student.save()
            return HttpResponse("Данные студента обновлены")
        else:
            check_email = Student.objects.filter(email=request.GET['email']).first()
            if check_email != None: return HttpResponse('Данный email уже зарегистрирован. ')
            student = Student(
                name=request.GET["name"],
                surename=request.GET["surename"],
                patronymic=request.GET["patronymic"],
                email=request.GET["email"],
                phone=request.GET["phone"],
                note=request.GET["note"],
                group=group_id,
                parentsArePensioners=request.GET["parentsArePensioners"],
                amountOfChildren=request.GET["amountOfChildren"],
                dateOfBirth=request.GET["dateOfBirth"],
                cityOfRegistration=request.GET["cityOfRegistration"],
                cityOfResidence=request.GET["cityOfResidence"],
                gender=request.GET["gender"],
                juvenileAffairsUnit=request.GET["juvenileAffairsUnit"],
                fullFamily=request.GET["fullFamily"],
                interests=request.GET["interests"],
                sportsSections=request.GET["sportsSections"]
            )
            student.save()
            return HttpResponse("Новый студент добавлен")


    def createGroup(self, request):
        tutor = Tutor.objects.filter(id=request.GET['leader']).first()
        if request.GET['group_id'] not in ['undefined', '']:
            group = Group.objects.get(id=request.GET['group_id'])
            group.name=request.GET['name']
            group.year=request.GET['year']
            group.leader=tutor
            group.save()
            return HttpResponse("Изменения сохранены")
        else:
            group = Group(
                name=request.GET['name'],
                year=request.GET['year'],
                leader=tutor
            )
            group.save()
            return HttpResponse("Новая группа добавлена.")


    def createParent(self, request):
        if request.GET['parent_id'] not in ['undefined', '']:
            student = Student.objects.get(email=request.GET['student_id'])
            parent = Parent.objects.get(id=request.GET['parent_id'])
            parent.student=student
            parent.name=request.GET['name']
            parent.surename=request.GET['surename']
            parent.patronymic=request.GET['patronymic']
            parent.phone=request.GET['phone']
            parent.email=request.GET['email']
            parent.note=request.GET['note']
            parent.who=request.GET['who']
            parent.save()
            return HttpResponse("Данные обновлены.")

        else: 
            student = Student.objects.get(id=request.GET['student_id'])
            parent = Parent(
                student=student,
                name=request.GET['name'],
                surename=request.GET['surename'],
                patronymic=request.GET['patronymic'],
                phone=request.GET['phone'],
                email=request.GET['email'],
                note=request.GET['note'],
                who=request.GET['who']
            )
            parent.save()
            return HttpResponse("Новый родитель добавлен.")