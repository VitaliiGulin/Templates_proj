import quopri
from gvg_framework.reqlib import GetReqMan, PostReqMan
from patterns.creational import Logger

LOGGER = Logger('main')


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

        LOGGER.log(f'GvgFramework._call_.DATA: <{ls_req_meth}>, <{ldic_data}>.')

        # Отработка паттерна page controller
        if l_path in self.m_lst_routes:
            lo_run_view = self.m_lst_routes[l_path]
        else:
            lo_run_view = PageNotFound404()
        # Отработка паттерна front controller
        for lo_run_front in self.m_lst_fronts:
            lo_run_front(ldic_req_data)
        # запуск контроллера с передачей объекта ldic_req_data
        l_code, l_body = lo_run_view(ldic_req_data)
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


# Другие виды Application.
# Одновременно, и наследование, и композиция излишни.
# Тут наследование я убрал.
class GVGDebugApplication():
    def __init__(self, io_routes, io_fronts):
        self.m_app = GvgFramework(io_routes, io_fronts)

    def __call__(self, i_env, i_start_res):
        #print('GVG.DEBUG!')
        #print(i_env)
        return self.m_app(i_env, i_start_res)


# А тут я композицию убрал.
class GVGFakeApplication(GvgFramework):
    def __init__(self, io_routes, io_fronts):
        super().__init__(io_routes, io_fronts)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']

