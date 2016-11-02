import jinja2


def template_file(in_file, out_file, **template_values):
    with open(in_file) as fl:
        template = jinja2.Template(fl.read())

    rendered = template.render(**template_values)

    with open(out_file, 'w') as fl:
        fl.write(rendered)
