import quopri
from gvg_framework.reqlib import GetReqMan, PostReqMan


class PageNotFound404:
    def __call__(self, i_req):
        return '404 WHAT', '404 PAGE Not Found'


class GvgFramework:
    """Класс GvgFramework - основа фреймворка"""
    def __init__(self, io_routes, io_fronts):
        self.m_lst_routes = io_routes
        self.m_lst_fronts = io_fronts

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        l_path = environ['PATH_INFO']

        if not l_path.endswith('/'):
            l_path = f'{l_path}/'

        ldic_req_data = {}
        ls_req_meth = environ['REQUEST_METHOD']
        ldic_req_data['req_meth'] = ls_req_meth

        if ls_req_meth == 'POST':
            ldic_data = PostReqMan().get_req_dict(environ)
            ldic_data = self.decode_value(ldic_data)
            ldic_req_data['dic_data'] = ldic_data
        if ls_req_meth == 'GET':
            ldic_data = GetReqMan().get_req_dict(environ)
            ldic_req_data['dic_data'] = ldic_data

        print(f'Пришел метод: <{ls_req_meth}>.')
        print(f'Пришли парам: <{ldic_data}>.')


        # Отработка паттерна page controller
        if l_path in self.m_lst_routes:
            lo_run_view = self.m_lst_routes[l_path]
        else:
            lo_run_view = PageNotFound404()
        ldic_reqs = {}
        # Отработка паттерна front controller
        for lo_run_front in self.m_lst_fronts:
            lo_run_front(ldic_reqs)
        # запуск контроллера с передачей объекта ldic_reqs
        l_code, l_body = lo_run_view(ldic_reqs)
        start_response(l_code, [('Content-Type', 'text/html')])
        return [l_body.encode('utf-8')]

    @staticmethod
    def decode_value(i_data):
        l_new_data = {}
        for k, v in i_data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            l_new_data[k] = val_decode_str
        return l_new_data
