import quopri


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
