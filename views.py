from gvg_framework.templator import render


class Index:
    def __call__(self, i_req):
        return '200 OK', render('index.html', data=i_req.get('data', None))


class About:
    def __call__(self, i_req):
        return '200 OK', render('about.html')


class NotFound404:
    def __call__(self, i_req):
        return '404 WHAT', '404 PAGE Not Found'
