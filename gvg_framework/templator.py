import os
from jinja2 import Template


def render(i_temp_name, i_folder='templates', **kwargs):
    """
    :param i_temp_name: имя шаблона
    :param i_folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """
    i_full_file_nm = os.path.join(i_folder, i_temp_name)
    # Открываем шаблон по имени
    with open(i_full_file_nm, encoding='utf-8') as f:
        l_template = Template(f.read())
    return l_template.render(**kwargs)
