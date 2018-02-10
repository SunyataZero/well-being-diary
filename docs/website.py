import webbrowser
from string import Template
# Documentation: https://docs.python.org/3/library/string.html#template-strings


template_file = open("template.html", "r")
index_content_file = open("index.content.html", "r")
user_guide_content_file = open("user_guide.content.html", "r")

template = Template(template_file.read())
home_str = template.substitute(content=index_content_file.read())
user_guide_str = template.substitute(content=user_guide_content_file.read())

index_content_file.close()
user_guide_content_file.close()
template_file.close()

with open("index.html", "w") as text_file:
    text_file.write(home_str)

with open("user_guide.html", "w") as text_file:
    text_file.write(user_guide_str)

webbrowser.open("index.html")
