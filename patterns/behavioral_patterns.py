import jsonpickle
from gvg_framework.templator import render


class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.m_observers = []

    def notify(self):
        for rec in self.m_observers:
            rec.update(self)


class SmsNotifier(Observer):
    def update(self, i_sub):
        print('SMS->', 'к нам присоединился', i_sub.students[-1].name)


class EmailNotifier(Observer):
    def update(self, i_sub):
        print('EMAIL->', 'к нам присоединился', i_sub.students[-1].name)


class BaseSerializer:
    def __init__(self, i_obj):
        self.m_obj = i_obj

    def save(self):
        return jsonpickle.dumps(self.m_obj)

    @staticmethod
    def load(i_dat):
        return jsonpickle.loads(i_dat)


class TemplateView:
    s_template_fn = 'template.html'
    s_ctx_data = {}

    def get_context_data(self):
        return self.s_ctx_data

    def get_template(self):
        return self.s_template_fn

    def render_template_with_context(self):
        l_tmp = self.get_template()
        l_dat = self.get_context_data()
        return '200 OK', render(l_tmp, **l_dat)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    slst_dat = []
    s_template_fn = 'list.html'
    ctx_obj_name = 'objects_list'

    def get_queryset(self):
        return self.slst_dat

    def get_ctx_obj_name(self):
        return self.ctx_obj_name

    def get_context_data(self):
        l_dat = self.get_queryset()
        l_obj = self.get_ctx_obj_name()
        l_dict_ret = {l_obj: l_dat}
        return l_dict_ret


class CreateView(TemplateView):
    s_template_fn = 'create.html'

    @staticmethod
    def get_request_data(i_req):
        return i_req['dic_data']

    def create_obj(self, data):
        pass

    def __call__(self, i_req):
        if i_req['req_meth'] == 'POST':
            l_dat = self.get_request_data(i_req)
            self.create_obj(l_dat)
            return self.render_template_with_context()
        else:
            return super().__call__(i_req)


class ConsoleWriter:
    def write(self, i_text):
        print(i_text)


class FileWriter:
    def __init__(self, i_file_nm):
        self.m_file_nm = i_file_nm

    def write(self, i_text):
        with open(self.m_file_nm, 'a', encoding='utf-8') as f:
            f.write(f'{i_text}\n')

