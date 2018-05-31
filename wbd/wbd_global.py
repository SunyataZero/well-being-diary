
"""
Module comments:
Global vars are used for storing some of the global application states. Please don't use global vars for
storing other types of values
"""

import enum
import os
from PyQt5 import QtCore


ICONS_DIR_STR = "icons"


class ViewEnum(enum.Enum):
    daily_overview = 0
    question_view = 1
    search_view = 2


def get_base_dir() -> str:
    base_dir_str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # -__file__ is the file that was started, in other words mindfulness-at-the-computer.py
    return base_dir_str


def get_icon_path(i_file_name: str) -> str:
    ret_icon_path_str = os.path.join(get_base_dir(), ICONS_DIR_STR, i_file_name)
    return ret_icon_path_str


diary_view_locked_bool = False

BWB_APPLICATION_VERSION_STR = "prototype 4"
BWB_APPLICATION_NAME_STR = "Well-Being Journal"
NO_ACTIVE_QUESTION_INT = -1
NO_ACTIVE_JOURNAL_INT = -1

active_view_viewenum = ViewEnum.daily_overview
active_date_qdate = QtCore.QDate.currentDate()
active_question_id_it = NO_ACTIVE_QUESTION_INT  # -TODO: Change this
shown_month_1to12_it = QtCore.QDate.currentDate().month()
shown_year_it = QtCore.QDate.currentDate().year()
search_string_str = ""

diary_entries_per_page_int = 20
current_page_number_int = 0  # -starts at zero

background_image_path = ""
diary_text_size_ft = -1


def qdate_to_unixtime(i_qdate: QtCore.QDate) -> int:
    qdatetime = QtCore.QDateTime(i_qdate)
    unixtime_it = qdatetime.toMSecsSinceEpoch() // 1000
    return unixtime_it

testing_bool = False


def get_database_filename():
    if testing_bool:
        return ":memory:"
    else:
        return "bwb_database_file.db"


class MoveDirectionEnum(enum.Enum):
    up = 1
    down = 2


def create_links_using_delimiters(i_original: str, i_start_delimiter: str, i_end_delimiter: str):
    # i_start_replace_before: str, i_start_replace_after: str, i_end_replace: str
    new_str = ""
    count = 0
    start_int = 0
    while count < len(i_original):
        character_outer = i_original[count]
        if character_outer == i_start_delimiter:
            new_str += i_original[start_int:count]
            start_int = count + 1
            while count < len(i_original):
                character_inner = i_original[count]
                if character_inner == i_end_delimiter:
                    link_str = i_original[start_int:count]
                    new_str += '<a href="' + link_str + '">' + link_str + '</a>'
                    start_int = count + 1
                    break
                count += 1
        count += 1
    new_str += i_original[start_int:count]
    return new_str


"""
def get_active_date():
    global active_date
    return active_date
def set_active_date(i_qdate):
    global active_date
    active_date = i_qdate
"""
