import copy
import quopri
from patterns.behavioral_patterns import ConsoleWriter, Subject


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            l_name = args[0]
        if kwargs:
            l_name = kwargs['i_name']

        if l_name in cls.__instance:
            return cls.__instance[l_name]
        else:
            cls.__instance[l_name] = super().__call__(*args, **kwargs)
            return cls.__instance[l_name]


class Logger(metaclass=SingletonByName):
    def __init__(self, i_name, i_writer=ConsoleWriter()):
        self.m_name = i_name
        self.m_writer = i_writer

    def log(self, i_text):
        l_text = f'log({self.m_name})---> {i_text}'
        self.m_writer.write(l_text)


LOGGER = Logger('cre_pat')


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name
    pass


# преподаватель
class Teacher(User):
    pass


# студент
class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    s_types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.s_types[type_](name)


# порождающий паттерн Прототип - Курс
class CoursePrototype:
    def clone(self, i_type, i_name, i_cat):
        ls_new_name = f'copy_{i_name}'
        return CourseFactory.create(i_type, ls_new_name, i_cat)
        #return copy.deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, i_name, i_cat):
        self.name = i_name
        self.m_category = i_cat
        self.m_category.m_courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# Интерактивный курс
class InteractiveCourse(Course):
    s_type = 'interactive'


# Курс в записи
class RecordCourse(Course):
    s_type = 'record'


class Category:
    s_auto_id = 0

    def __init__(self, i_name):
        self.id = Category.s_auto_id
        Category.s_auto_id += 1
        self.name = i_name
        self.m_courses = []

    def course_count(self):
        return len(self.m_courses)


# порождающий паттерн Абстрактная фабрика - фабрика курсов
class CourseFactory:
    s_types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, i_type, i_name, i_cat):
        return cls.s_types[i_type](i_name, i_cat)


class Engine:
    def __init__(self):
        self.m_teachers = []
        self.m_students = []
        self.m_courses = []
        self.m_categories = []

    @staticmethod
    def create_user(i_type, name):
        return UserFactory.create(i_type, name)

    @staticmethod
    def create_category(i_name):
        return Category(i_name)

    def find_category_by_id(self, i_id):
        LOGGER.log(f'Engine.find_category_by_id.Input: <{i_id}>.')
        LOGGER.log(f'Engine.find_category_by_id.Data: <{self.m_categories}>.')

        for item in self.m_categories:
            if item.id == i_id:
                return item
        raise KeyError

    @staticmethod
    def create_course(i_type, i_name, i_cat):
        return CourseFactory.create(i_type, i_name, i_cat)

    def get_course(self, i_name) -> Course:
        for rec in self.m_courses:
            if rec.name == i_name:
                return rec
        return None

    def get_student(self, i_name) -> Student:
        for rec in self.m_students:
            if rec.name == i_name:
                return rec

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')

