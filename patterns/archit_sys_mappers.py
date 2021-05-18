from man import GCONN
from patterns.archit_sys_uow import UnitOfWork


class DomainObject:
    def mark_for_ins(self):
        UnitOfWork.get_current().ins_refresh(self)

    def mark_for_upd(self):
        UnitOfWork.get_current().upd_refresh(self)

    def mark_for_del(self):
        UnitOfWork.get_current().del_refresh(self)


class User:
    def __init__(self, name):
        self.name = name
    pass


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class StudentMapper:
    def __init__(self, i_con):
        self.m_con = i_con
        self.m_cur = i_con.cursor()
        self.m_tab = 'student'

    def all(self):
        ls_stat = f'SELECT * from {self.m_tab}'
        self.m_cur.execute(ls_stat)
        l_res = []
        for item in self.m_cur.fetchall():
            id, name = item
            l_stu = Student(name)
            l_stu.id = id
            l_res.append(l_stu)
        return l_res

    def find_by_id(self, id):
        ls_stat = f"SELECT id, name FROM {self.m_tab} WHERE id=?"
        self.m_cur.execute(ls_stat, (id,))
        l_res = self.m_cur.fetchone()
        if l_res:
            return Student(*l_res)
        else:
            return None

    def insert(self, obj):
        ls_stat = f"INSERT INTO {self.m_tab} (name) VALUES (?)"
        self.m_cur.execute(ls_stat, (obj.name,))

    def update(self, obj):
        ls_stat = f"UPDATE {self.m_tab} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.m_cur.execute(ls_stat, (obj.name, obj.id))

    def delete(self, obj):
        ls_stat = f"DELETE FROM {self.m_tab} WHERE id=?"
        self.m_cur.execute(ls_stat, (obj.id,))


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    s_map = {
        'student': StudentMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper_by_obj(obj):
        print("Call from MapperRegistry.get_mapper", obj, obj.__class__)
        if isinstance(obj, Student):
            print("Пришел на вход Student!")
            return StudentMapper(GCONN)
        #if isinstance(obj, Category):
            #return CategoryMapper(GCONN)

    @staticmethod
    def get_mapper_by_nam(name):
        return MapperRegistry.s_map[name](GCONN)


