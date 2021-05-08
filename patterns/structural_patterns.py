from time import time


class GvgRoute:
    def __init__(self, idic_routes, i_url):
        self.m_routes = idic_routes
        self.m_url = i_url

    def __call__(self, cls):
        self.m_routes[self.m_url] = cls()


class GvgDebug:
    def __init__(self, i_name):
        self.m_name = i_name

    def __call__(self, cls):
        def timeit(i_method):
            def timed(*args, **kw):
                l_start_time = time()
                l_res = i_method(*args, **kw)
                l_work_time = time() - l_start_time

                print(f'gvg.debug --> {self.m_name} выполнялся {l_work_time:2.2f} ms')
                return l_res
            return timed
        return timeit(cls)
