from datetime import date
from views import Index, About, StudyPrograms, CoursesList, \
    CreateCourse, CreateCategory, CategoryList, CopyCourse


# front controller
def secret_front(i_req):
    i_req['date'] = date.today()


def other_front(i_req):
    i_req['key'] = 'key'


glst_fronts = [secret_front, other_front]

gdic_routes = {
    '/': Index(),
    '/about/': About(),
    '/study_programs/': StudyPrograms(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-course/': CopyCourse()
}
