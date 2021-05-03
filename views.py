from datetime import date

from gvg_framework.templator import render
from patterns.creational_patterns import Engine, Logger

GSITE = Engine()
LOGGER = Logger('views')


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=GSITE.m_categories)


class About:
    def __call__(self, i_req):
        return '200 OK', render('about.html')


# контроллер - Расписания
class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список курсов
class CoursesList:
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
class CreateCourse:
    s_category_id = -1

    def __call__(self, i_req):
        if i_req['req_meth'] == 'POST':
            ldic_dat = i_req['dic_data']

            l_crs_name = ldic_dat['name']
            l_crs_name = GSITE.decode_value(l_crs_name)

            lo_cat = None
            if self.s_category_id != -1:
                lo_cat = GSITE.find_category_by_id(int(self.s_category_id))
                lo_crs = GSITE.create_course('record', l_crs_name, lo_cat)
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
class CreateCategory:
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
class CategoryList:
    def __call__(self, i_req):
        LOGGER.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=GSITE.m_categories)


# контроллер - копировать курс
class CopyCourse:
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
