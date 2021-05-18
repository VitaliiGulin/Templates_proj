import threading
from patterns.archit_sys_mappers import GCONN

# архитектурный системный паттерн - UnitOfWork
class UnitOfWork:
    """
    Паттерн UNIT OF WORK
    """
    # Работает с конкретным потоком
    s_cur = threading.local()

    def __init__(self, i_con):
        self.m_ins_objs = []
        self.m_upd_objs = []
        self.m_del_objs = []
        self.m_con = i_con

    def set_mapper_registry(self, i_reg):
        self.m_reg = i_reg

    def ins_refresh(self, i_rec):
        self.m_ins_objs.clear()
        self.m_ins_objs.append(i_rec)

    def upd_refresh(self, i_rec):
        self.m_upd_objs.clear()
        self.m_upd_objs.append(i_rec)

    def del_refresh(self, i_rec):
        self.m_del_objs.clear()
        self.m_del_objs.append(i_rec)

    def commit(self):
        self.flush_ins()
        self.flush_upd()
        self.flush_del()
        self.m_con.commit()

    def flush_ins(self):
        for rec in self.m_ins_objs:
            self.m_reg.get_mapper_by_obj(rec).insert(rec)

    def flush_upd(self):
        for rec in self.m_upd_objs:
            self.m_reg.get_mapper_by_obj(rec).update(rec)

    def flush_del(self):
        for rec in self.m_del_objs:
            self.m_reg.get_mapper_by_obj(rec).delete(rec)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork(GCONN))

    @classmethod
    def set_current(cls, i_uow):
        cls.s_cur.m_uow = i_uow

    @classmethod
    def get_current(cls):
        return cls.s_cur.m_uow

