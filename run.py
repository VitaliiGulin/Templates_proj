from wsgiref.simple_server import make_server
from gvg_framework.main import GvgFramework,\
    GVGDebugApplication, GVGFakeApplication
from urls import glst_fronts
from views import gdic_routes

G_APP = GVGDebugApplication(gdic_routes, glst_fronts)
#print('gdic_routes', gdic_routes)
#print('glst_fronts', glst_fronts)

with make_server('', 7788, G_APP) as srv_inst:
    print("Прослушка на порту 7788...")
    srv_inst.serve_forever()
