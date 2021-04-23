from datetime import date
from views import Index, About


# front controller
def secret_front(i_req):
    i_req['data'] = date.today()


def other_front(i_req):
    i_req['key'] = 'key'


glst_fronts = [secret_front, other_front]

gdic_routes = {
    '/': Index(),
    '/about/': About(),
}
