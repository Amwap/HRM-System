import requests
import random
import datetime
import time


name = """Александрова Кира Максимовна
Архипова Ангелина Макаровна
Архипова Анна Тимофеевна
Балашов Григорий Тимофеевич
Балашова Валерия Андреевна
Баранов Андрей Тимофеевич
Бородина Александра Артемьевна
Буров Георгий Янович
Васильев Мирон Дмитриевич
Васильева Дарья Данииловна
Виноградов Владимир Семёнович
Вишневская Василиса Максимовна
Власов Тимур Максимович
Воробьев Артём Артёмович
Голубев Руслан Львович
Гончарова Ангелина Макаровна
Горбачева Вера Ивановна
Горюнова Анастасия Павловна
Грачева Мария Михайловна
Григорьева Анна Романовна
Григорьева Виктория Александровна
Гусев Константин Фёдорович
Гусев Елисей Дмитриевич
Гусев Андрей Богданович
Гусева Ева Максимовна
Денисова Анна Вячеславовна
Дмитриев Александр Александрович
Дмитриев Иван Ярославович
Дмитриев Дмитрий Владимирович
Дорофеев Степан Филиппович
Ершов Виктор Матвеевич
Ефимов Игорь Ильич
Ефремова Яна Егоровна
Зайцев Максим Олегович
Зайцева Александра Семёновна
Захаров Григорий Алексеевич
Иванова Анна Михайловна
Исаева Диана Андреевна
Калашникова Василиса Анатольевна
Карпов Тимур Денисович
Кириллов Андрей Владимирович
Киселева Анастасия Алексеевна
Климов Артём Олегович
Ковалев Александр Всеволодович
Ковалева Милана Дмитриевна
Козырева Анастасия Александровна
Козырева Юлия Фёдоровна
Колпакова Мария Ильинична
Коновалова Валерия Александровна
Кочергин Михаил Леонидович
Кочетков Андрей Миронович
Кочетков Артём Александрович
Крюкова Кристина Макаровна
Крюкова Нина Руслановна
Крюкова София Романовна
Кузнецов Никита Георгиевич
Кузьмина Ксения Артёмовна
Лаптев Дмитрий Артёмович
Лебедева Яна Андреевна
Лобанова Таисия Михайловна
Лукина Ульяна Данииловна
Малышев Платон Григорьевич
Медведев Дмитрий Андреевич
Медведева Виктория Михайловна
Мельников Никита Александрович
Михайлов Максим Михайлович
Михайлова Елизавета Данииловна
Михеев Марк Михайлович
Моисеева Анастасия Сергеевна
Наумов Михаил Александрович
Наумов Николай Алексеевич
Некрасова Анна Николаевна
Нечаева Кристина Михайловна
Никифоров Иван Ильич
Николаев Демьян Максимович
Осипов Арсений Артемьевич
Панков Сергей Тимофеевич
Пантелеев Лев Даниилович
Плотникова Алиса Арсеньевна
Родионова Кира Сергеевна
Сазонов Григорий Вадимович
Селезнев Александр Владимирович
Соколов Егор Никитич
Соловьев Сергей Иванович
Соловьев Фёдор Егорович
Соловьева Мария Александровна
Соловьева Злата Максимовна
Сорокина Мария Дмитриевна
Спиридонова Виктория Артёмовна
Терентьева Полина Тимуровна
Тимофеева София Романовна
Успенский Илья Михайлович
Федоров Матвей Арсеньевич
Федотов Глеб Маркович
Филатов Александр Иванович
Фирсов Гордей Тимофеевич
Харитонова Таисия Станиславовна
Черняева Валерия Ильинична
Щербакова София Михайловна
Яковлева Варвара Георгиевна
"""

list_name = name.split('\n')
count = 0
groups_id = [15, 16, 9, 8, 7]



for j in groups_id: 
    number_of_group=j
    for i in range(0,10):
        count+=1
        name = random.choice(list_name)
        fname = name.split(" ")[1]
        fsurename = name.split(" ")[0]
        fpat = name.split(" ")[2]
        query_list = [
            'login=admin',
            'element=createStudent',
            'student_id=',
            f'name={fname}',
            f'surename={fsurename}',
            f'patronymic={fpat}',
            f'email=user{count}@mail.ru',
            'phone=8(900)XXX-XX-XX',
            'note=',
            f'group={number_of_group}',
            f'parentsArePensioners={random.choice(["да", "нет"])}',
            f'amountOfChildren={random.choice([0, 0, 0, 0, 0, 1, 1, 1, 2, 3,])}',
            f'dateOfBirth=2004-02-12',
            'cityOfRegistration=Москва',
            'cityOfResidence=Москва',
            'gender=м',
            f'juvenileAffairsUnit={random.choice(["да", "нет"])}',
            f'fullFamily={random.choice([0, 1, 2, 3])}',
            'interests=',
            f'sportsSections={random.choice(["Плавание", "Волейбол", "Баскетбол", "Лёгкая-атлетика", "", "", "", "" ])}'    
        ]

        form="&".join(query_list)
        # http://j7287160.myjino.ru/api/
        print(form)
        print(j)
        print(count)
        r = requests.get('http://j7287160.myjino.ru/api?' + form)
        print(r.status_code)
        time.sleep(1)