from datetime import date

from gvg_framework.templator import render
from patterns.creational import Engine, Logger
from patterns.structural_patterns import GvgRoute, GvgDebug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    TemplateView, ListView, CreateView, BaseSerializer
from patterns.archit_sys_uow import UnitOfWork
from patterns.archit_sys_mappers import MapperRegistry

GSITE = Engine()
LOGGER = Logger('views')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

gdic_routes = {}


@GvgRoute(idic_routes=gdic_routes, i_url='/')
class Index:
    @GvgDebug(i_name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=GSITE.m_categories)


@GvgRoute(idic_routes=gdic_routes, i_url='/about/')
class About:
    @GvgDebug(i_name='About')
    def __call__(self, i_req):
        return '200 OK', render('about.html')


# контроллер - Расписания
@GvgRoute(idic_routes=gdic_routes, i_url='/study_programs/')
class StudyPrograms:
    @GvgDebug(i_name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# контроллер 404
class NotFound404:
    @GvgDebug(i_name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@GvgRoute(idic_routes=gdic_routes, i_url='/courses-list/')
class CoursesList:
    @GvgDebug(i_name='CoursesList')
    def __call__(self, i_req):
        LOGGER.log(f'CoursesList.__call__.Input: <{i_req}>.')
        try:
            l_cat_id = int(i_req['dic_data']['id'])
            LOGGER.log(f'CoursesList.__call__.Data.l_cat_id: <{l_cat_id}>.')

            lo_cat = GSITE.find_category_by_id(l_cat_id)
            return '200 OK', render('course_list.html', objects_list=lo_cat.m_courses, name=lo_cat.name, id=lo_cat.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
@GvgRoute(idic_routes=gdic_routes, i_url='/create-course/')
class CreateCourse:
    s_category_id = -1

    @GvgDebug(i_name='CreateCourse')
    def __call__(self, i_req):
        if i_req['req_meth'] == 'POST':
            ldic_dat = i_req['dic_data']

            l_crs_name = ldic_dat['name']
            l_crs_name = GSITE.decode_value(l_crs_name)

            lo_cat = None
            if self.s_category_id != -1:
                lo_cat = GSITE.find_category_by_id(int(self.s_category_id))
                lo_crs = GSITE.create_course('record', l_crs_name, lo_cat)
                lo_crs.m_observers.append(email_notifier)
                lo_crs.m_observers.append(sms_notifier)
                GSITE.m_courses.append(lo_crs)

            return '200 OK', render('course_list.html', objects_list=lo_cat.m_courses,
                                    name=lo_cat.name, id=lo_cat.id)

        else:
            try:
                self.s_category_id = int(i_req['dic_data']['id'])
                category = GSITE.find_category_by_id(int(self.s_category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
@GvgRoute(idic_routes=gdic_routes, i_url='/create-category/')
class CreateCategory:
    @GvgDebug(i_name='CreateCategory')
    def __call__(self, i_req):
        LOGGER.log(f'CreateCategory.__call__.Input: <{i_req}>.')

        if i_req['req_meth'] == 'POST':
            ldic_dat = i_req['dic_data']

            ls_cat_name = ldic_dat['name']
            ls_cat_name = GSITE.decode_value(ls_cat_name)
            l_category_id = ldic_dat.get('category_id')

            LOGGER.log(f'CreateCategory.__call__.DATA: name: <{ls_cat_name}>, <{l_category_id}>.')

            if l_category_id:
                lo_new_cat = GSITE.find_category_by_id(int(l_category_id))
            else:
                lo_new_cat = GSITE.create_category(ls_cat_name)

            LOGGER.log(f'CreateCategory.__call__.DATA: lo_new_cat: <{lo_new_cat}>.')

            GSITE.m_categories.append(lo_new_cat)

            return '200 OK', render('index.html', objects_list=GSITE.m_categories)
        else:
            l_categories = GSITE.m_categories
            return '200 OK', render('create_category.html', categories=l_categories)


# контроллер - список категорий
@GvgRoute(idic_routes=gdic_routes, i_url='/category-list/')
class CategoryList:
    @GvgDebug(i_name='CategoryList')
    def __call__(self, i_req):
        LOGGER.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=GSITE.m_categories)


# контроллер - копировать курс
@GvgRoute(idic_routes=gdic_routes, i_url='/copy-course/')
class CopyCourse:
    @GvgDebug(i_name='CopyCourse')
    def __call__(self, i_req):
        LOGGER.log(f'CopyCourse.__call__.Input: <{i_req}>.')

        l_req_pars = i_req['dic_data']

        LOGGER.log(f'CopyCourse.__call__.DATA.l_req_pars: <{l_req_pars}>.')

        try:
            ls_old_crs = l_req_pars['name']
            lo_old_crs = GSITE.get_course(ls_old_crs)

            LOGGER.log(f'CopyCourse.__call__.DATA.l_req_pars: old_name: <{ls_old_crs}>, old_course: <{lo_old_crs}>.')

            if lo_old_crs:
                lo_new_crs = lo_old_crs.clone(lo_old_crs.s_type,
                                              ls_old_crs,
                                              lo_old_crs.m_category)
                GSITE.m_courses.append(lo_new_crs)

            return '200 OK', render('course_list.html', objects_list=GSITE.m_courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@GvgRoute(idic_routes=gdic_routes, i_url='/student-list/')
class StudentListView(ListView):
    s_template_fn = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_mapper_by_nam('student')
        return mapper.all()

@GvgRoute(idic_routes=gdic_routes, i_url='/create-student/')
class StudentCreateView(CreateView):
    s_template_fn = 'create_student.html'

    def create_obj(self, i_dat: dict):
        lb_name = i_dat['name']
        ls_name = GSITE.decode_value(lb_name)
        l_new_obj = GSITE.create_user('student', ls_name)
        GSITE.m_students.append(l_new_obj)
        l_new_obj.mark_for_ins()
        UnitOfWork.get_current().commit()


@GvgRoute(idic_routes=gdic_routes, i_url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    s_template_fn = 'add_student.html'

    def get_context_data(self):
        l_ctx = super().get_context_data()
        l_ctx['courses'] = GSITE.m_courses
        l_ctx['students'] = GSITE.m_students
        return l_ctx

    def create_obj(self, i_dat: dict):
        l_crs_nm = i_dat['course_name']
        l_crs_nm = GSITE.decode_value(l_crs_nm)
        lo_crs = GSITE.get_course(l_crs_nm)
        l_std_nm = i_dat['student_name']
        l_std_nm = GSITE.decode_value(l_std_nm)
        lo_std = GSITE.get_student(l_std_nm)
        lo_crs.add_student(lo_std)


@GvgRoute(idic_routes=gdic_routes, i_url='/api/')
class CourseApi:
    @GvgDebug(i_name='CourseApi')
    def __call__(self, i_req):
        return '200 OK', BaseSerializer(GSITE.m_courses).save()

