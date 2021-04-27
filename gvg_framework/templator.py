from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(i_temp_name, i_folder='templates', **kwargs):

    l_env = Environment()
    l_env.loader = FileSystemLoader(i_folder)
    l_template = l_env.get_template(i_temp_name)
    return l_template.render(**kwargs)
