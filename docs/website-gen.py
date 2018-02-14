import webbrowser
from string import Template
# Documentation: https://docs.python.org/3/library/string.html#template-strings

TEMPLATE_FILE_STR = "template.html"
TARGET_INDEX_FILE_STR = "index"
TARGET_USER_GUIDE_FILE_STR = "index"
CONTENT_STR = ".content"
SUFFIX_STR = ".html"

with open(TEMPLATE_FILE_STR, "r") as template_file,\
open(TARGET_INDEX_FILE_STR + CONTENT_STR + SUFFIX_STR, "r") as index_content_file,\
open(TARGET_USER_GUIDE_FILE_STR + CONTENT_STR + SUFFIX_STR, "r") as user_guide_content_file:
    template = Template(template_file.read())
    home_str = template.substitute(content=index_content_file.read())
    user_guide_str = template.substitute(content=user_guide_content_file.read())

with open(TARGET_INDEX_FILE_STR + SUFFIX_STR, "w") as index_file,\
open(TARGET_USER_GUIDE_FILE_STR + SUFFIX_STR, "w") as user_guide_file:
    index_file.write(home_str)
    user_guide_file.write(user_guide_str)

webbrowser.open("index.html")
