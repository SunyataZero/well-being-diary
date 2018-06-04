import csv
import datetime
import shutil
import sqlite3
import time
import enum
import re

import wbd.wbd_global

#################
#
# Model
#
# This module contains everything related to the model for the application:
# * The db schema
# * The db connection
# * Data structure classes (each of which contains functions for reading and writing to the db)
# * Database creation and setup
# * Various functions (for backing up the db etc)
#
# Notes:
# * When inserting vales, it's best to use "VALUES (?, ?)" because then the sqlite3 module will take care of
#   escaping strings for us
#
#################

SQLITE_FALSE = 0
SQLITE_TRUE = 1
SQLITE_NULL = "NULL"
TIME_NOT_SET = 25
NO_REFERENCE = -1


class QuestionSetupEnum(enum.Enum):
    # -only used at setup
    practice = 1
    gratitude = 2
    sharing = 3
    contribution = 4
    study = 5
    self_compassion = 6


def get_schema_version(i_db_conn):
    t_cursor = i_db_conn.execute("PRAGMA user_version")
    return t_cursor.fetchone()[0]


def set_schema_version(i_db_conn, i_version_it):
    i_db_conn.execute("PRAGMA user_version={:d}".format(i_version_it))


def initial_schema_and_setup(i_db_conn):
    """Auto-increment is not needed in our case: https://www.sqlite.org/autoinc.html
    """
    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.HabitTable.name + "("
        + DbSchemaM.HabitTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.HabitTable.Cols.sort_order + " INTEGER NOT NULL, "
        + DbSchemaM.HabitTable.Cols.title + " TEXT NOT NULL, "
        + DbSchemaM.HabitTable.Cols.description + " TEXT NOT NULL DEFAULT '', "
        + DbSchemaM.HabitTable.Cols.archived + " INTEGER DEFAULT " + str(SQLITE_FALSE) + ", "
        + DbSchemaM.HabitTable.Cols.hour + " INTEGER DEFAULT " + str(TIME_NOT_SET) + ", "
        + DbSchemaM.HabitTable.Cols.default_journal_ref
        + " INTEGER REFERENCES " + DbSchemaM.JournalTable.name + "(" + DbSchemaM.JournalTable.Cols.id + ")"
        + " NOT NULL DEFAULT '" + str(wbd.wbd_global.NO_ACTIVE_JOURNAL_INT) + "'"
        + ")"
    )

    i_db_conn.execute(
        "INSERT INTO " + DbSchemaM.HabitTable.name + "("
        + DbSchemaM.HabitTable.Cols.id + ", "
        + DbSchemaM.HabitTable.Cols.sort_order + ", "
        + DbSchemaM.HabitTable.Cols.title + ", "
        + DbSchemaM.HabitTable.Cols.description
        + ") VALUES (?, ?, ?, ?)", (wbd.wbd_global.NO_ACTIVE_QUESTION_INT, -1, "<i>no question</i>", "")
    )

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.DiaryEntryTable.name + "("
        + DbSchemaM.DiaryEntryTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.DiaryEntryTable.Cols.date_added + " INTEGER, "
        + DbSchemaM.DiaryEntryTable.Cols.rating + " INTEGER NOT NULL DEFAULT '" + str(1) + "', "
        + DbSchemaM.DiaryEntryTable.Cols.diary_text + " TEXT, "
        + DbSchemaM.DiaryEntryTable.Cols.habit_ref
        + " INTEGER REFERENCES " + DbSchemaM.HabitTable.name + "(" + DbSchemaM.HabitTable.Cols.id + ")"
        + " NOT NULL DEFAULT '" + str(wbd.wbd_global.NO_ACTIVE_QUESTION_INT) + "',"
        + DbSchemaM.DiaryEntryTable.Cols.journal_ref
        + " INTEGER REFERENCES " + DbSchemaM.JournalTable.name + "(" + DbSchemaM.JournalTable.Cols.id + ")"
        + " NOT NULL DEFAULT '" + str(wbd.wbd_global.NO_ACTIVE_JOURNAL_INT) + "'"
        + ")"
    )

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.ReminderTable.name + "("
        + DbSchemaM.ReminderTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.ReminderTable.Cols.title + " TEXT DEFAULT '', "
        + DbSchemaM.ReminderTable.Cols.reminder + " TEXT DEFAULT ''"
        + ")"
    )
    # + " NOT NULL DEFAULT '" + str(wbd.bwbglobal.NO_ACTIVE_QUESTION_INT) + "'"

    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.JournalTable.name + "("
        + DbSchemaM.JournalTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.JournalTable.Cols.sort_order + " INTEGER NOT NULL, "
        + DbSchemaM.JournalTable.Cols.title + " TEXT NOT NULL, "
        + DbSchemaM.JournalTable.Cols.description + " TEXT NOT NULL DEFAULT ''"
        + ")"
    )

    """
    i_db_conn.execute(
        "CREATE INDEX " + DbSchemaM.DiaryEntryTable.name + "("
        + ")"
    )
    """



"""
Example of db upgrade code:
def upgrade_1_2(i_db_conn):
    backup_db_file()
    i_db_conn.execute(
        "ALTER TABLE " + DbSchemaM.ObservancesTable.name + " ADD COLUMN "
        + DbSchemaM.ObservancesTable.Cols.user_text + " TEXT DEFAULT ''"
    )


def upgrade_1_2(i_db_conn):
    backup_db_file()
    i_db_conn.execute(
        "ALTER TABLE " + DbSchemaM.QuestionTable.name + " ADD COLUMN "
        + DbSchemaM.QuestionTable.Cols.hour + " INTEGER DEFAULT " + str(TIME_NOT_SET)
    )


def upgrade_2_3(i_db_conn):
    backup_db_file()
    i_db_conn.execute(
        "ALTER TABLE " + DbSchemaM.QuestionTable.name + " ADD COLUMN "
        + DbSchemaM.QuestionTable.Cols.labels + " TEXT DEFAULT ''"
    )
"""


upgrade_steps = {
    1: initial_schema_and_setup
}


class DbHelperM(object):
    __db_connection = None  # "Static"

    # noinspection PyTypeChecker
    @staticmethod
    def get_db_connection():
        if DbHelperM.__db_connection is None:
            DbHelperM.__db_connection = sqlite3.connect(wbd.wbd_global.get_database_filename())

            # Upgrading the database
            # Very good upgrade explanation:
            # http://stackoverflow.com/questions/19331550/database-change-with-software-update
            # More info here: https://www.sqlite.org/pragma.html#pragma_schema_version
            current_db_ver_it = get_schema_version(DbHelperM.__db_connection)
            target_db_ver_it = max(upgrade_steps)
            for upgrade_step_it in range(current_db_ver_it + 1, target_db_ver_it + 1):
                if upgrade_step_it in upgrade_steps:
                    upgrade_steps[upgrade_step_it](DbHelperM.__db_connection)
                    set_schema_version(DbHelperM.__db_connection, upgrade_step_it)
            DbHelperM.__db_connection.commit()

            # TODO: Where do we close the db connection? (Do we need to close it?)
            # http://stackoverflow.com/questions/3850261/doing-something-before-program-exit

            if wbd.wbd_global.testing_bool:
                populate_db_with_test_data()

        return DbHelperM.__db_connection


class DbSchemaM:
    class HabitTable:
        name = "habit"

        class Cols:
            id = "id"  # key
            sort_order = "sort_order"
            title = "title"
            description = "description"
            archived = "archived"
            hour = "hour"
            default_journal_ref = "default_journal"

    class DiaryEntryTable:
        name = "diary_entry"

        class Cols:
            id = "id"  # key
            date_added = "date_added"
            rating = "rating"
            diary_text = "diary_text"
            habit_ref = "habit_ref"
            journal_ref = "journal_ref"

    class ReminderTable:
        name = "reminder"

        class Cols:
            id = "id"  # key
            title = "title"
            reminder = "reminder"

    class JournalTable:
        name = "journal"

        class Cols:
            id = "id"  # key
            sort_order = "sort_order"
            title = "title"
            description = "description"


class QuestionM:
    def __init__(
    self, i_id: int, i_order: int, i_title: str, i_description: str, i_archived: bool, i_hour: int, i_labels: str,
    ) -> None:
        self.id_int = i_id
        self.sort_order_int = i_order
        self.title_str = i_title
        self.description_str = i_description
        self.archived_bl = i_archived
        self.hour_int = i_hour
        self.labels_str = i_labels

    @staticmethod
    def add(i_title_str: str, i_question_str: str, i_archived: bool=False, i_hour: int=TIME_NOT_SET) -> int:
        # i_question_id_int: int,
        sort_order = len(QuestionM.get_all())
        print("sort_order = " + str(sort_order))

        archived_bool_as_int = SQLITE_FALSE
        if i_archived:
            archived_bool_as_int = SQLITE_TRUE

        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.HabitTable.name + "("
            + DbSchemaM.HabitTable.Cols.sort_order + ", "
            + DbSchemaM.HabitTable.Cols.title + ", "
            + DbSchemaM.HabitTable.Cols.description + ", "
            + DbSchemaM.HabitTable.Cols.archived + ", "
            + DbSchemaM.HabitTable.Cols.hour
            + ") VALUES (?, ?, ?, ?, ?)",
            (sort_order, i_title_str, i_question_str, archived_bool_as_int, i_hour)
        )
        db_connection.commit()

        question_id_int = db_cursor.lastrowid
        return question_id_int

    @staticmethod
    def get(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.HabitTable.name
            + " WHERE " + DbSchemaM.HabitTable.Cols.id + "=" + str(i_id_it)
        )
        journal_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return QuestionM(*journal_db_te)

    @staticmethod
    def get_all(i_show_archived_questions_bool = False):
        if i_show_archived_questions_bool:
            show_archived_questions_bool_as_int = SQLITE_TRUE
        else:
            show_archived_questions_bool_as_int = SQLITE_FALSE
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.HabitTable.name
            + " WHERE " + DbSchemaM.HabitTable.Cols.archived + "=" + str(show_archived_questions_bool_as_int)
            + " ORDER BY " + DbSchemaM.HabitTable.Cols.hour + ", " + DbSchemaM.HabitTable.Cols.sort_order
        )
        journal_db_te_list = db_cursor_result.fetchall()
        db_connection.commit()

        return [QuestionM(*journal_db_te) for journal_db_te in journal_db_te_list]

    @staticmethod
    def update_sort_order(i_id: int, i_sort_order: int) -> None:
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.HabitTable.name
            + " SET " + DbSchemaM.HabitTable.Cols.sort_order + " = ?"
            + " WHERE " + DbSchemaM.HabitTable.Cols.id + " = ?",
            (str(i_sort_order), str(i_id))
        )
        db_connection.commit()

    @staticmethod
    def update_hour(i_id_it, i_new_hour: int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.HabitTable.name
            + " SET " + DbSchemaM.HabitTable.Cols.hour + " = ?"
            + " WHERE " + DbSchemaM.HabitTable.Cols.id + " = ?",
            (str(i_new_hour), str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def update_title(i_id_it, i_new_text_sg):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.HabitTable.name
            + " SET " + DbSchemaM.HabitTable.Cols.title + " = ?"
            + " WHERE " + DbSchemaM.HabitTable.Cols.id + " = ?",
            (i_new_text_sg, str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def update_description(i_id_it, i_new_text_sg):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.HabitTable.name
            + " SET " + DbSchemaM.HabitTable.Cols.description + " = ?"
            + " WHERE " + DbSchemaM.HabitTable.Cols.id + " = ?",
            (i_new_text_sg, str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def update_archived(i_id_it, i_archived_bool):

        archived_bool_as_int = SQLITE_FALSE
        if i_archived_bool:
            archived_bool_as_int = SQLITE_TRUE

        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.HabitTable.name
            + " SET " + DbSchemaM.HabitTable.Cols.archived + " = ?"
            + " WHERE " + DbSchemaM.HabitTable.Cols.id + " = ?",
            (str(archived_bool_as_int), str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def remove(i_id_it):

        if i_id_it == wbd.wbd_global.NO_ACTIVE_QUESTION_INT:
            raise Exception("This cannot be removed")
            return

        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "DELETE FROM " + DbSchemaM.HabitTable.name
            + " WHERE " + DbSchemaM.HabitTable.Cols.id + "=" + str(i_id_it)
        )

        db_cursor.execute(
            "UPDATE " + DbSchemaM.DiaryEntryTable.name
            + " SET " + DbSchemaM.DiaryEntryTable.Cols.habit_ref + "=" + SQLITE_NULL
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.habit_ref + "=" + str(i_id_it)
        )

        db_connection.commit()


class JournalM:
    def __init__(
    self, i_id: int, i_order: int, i_title: str, i_description: str) -> None:
        self.id_int = i_id
        self.sort_order_int = i_order
        self.title_str = i_title
        self.description_str = i_description

    @staticmethod
    def add(i_title_str: str, i_description: str) -> int:
        sort_order = len(JournalM.get_all())
        print("sort_order = " + str(sort_order))

        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.JournalTable.name + "("
            + DbSchemaM.JournalTable.Cols.sort_order + ", "
            + DbSchemaM.JournalTable.Cols.title + ", "
            + DbSchemaM.JournalTable.Cols.description
            + ") VALUES (?, ?, ?)",
            (sort_order, i_title_str, i_description)
        )
        db_connection.commit()

        journal_id_int = db_cursor.lastrowid
        return journal_id_int

    @staticmethod
    def get(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.JournalTable.name
            + " WHERE " + DbSchemaM.JournalTable.Cols.id + "=" + str(i_id_it)
        )
        journal_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return JournalM(*journal_db_te)

    @staticmethod
    def get_all():
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.JournalTable.name
        )
        journal_db_te_list = db_cursor_result.fetchall()
        db_connection.commit()

        return [JournalM(*journal_db_te) for journal_db_te in journal_db_te_list]

    @staticmethod
    def update_title(i_id_it, i_new_text_sg):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.JournalTable.name
            + " SET " + DbSchemaM.JournalTable.Cols.title + " = ?"
            + " WHERE " + DbSchemaM.JournalTable.Cols.id + " = ?",
            (i_new_text_sg, str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def update_description(i_id_it, i_new_text_sg):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.JournalTable.name
            + " SET " + DbSchemaM.JournalTable.Cols.description + " = ?"
            + " WHERE " + DbSchemaM.JournalTable.Cols.id + " = ?",
            (i_new_text_sg, str(i_id_it))
        )
        db_connection.commit()


class DiaryEntryM:
    def __init__(self, i_id, i_date_added_it, i_rating: int, i_diary_text, i_habit_ref_it, i_journal_ref: int):
        self.id = i_id
        self.date_added_it = i_date_added_it
        self.rating_int = i_rating
        self.diary_text = i_diary_text
        self.habit_ref_it = i_habit_ref_it
        self.journal_ref_it = i_journal_ref

    @staticmethod
    def add(i_date_added_it, i_favorite_it, i_diary_text, i_journal_ref_it: int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.DiaryEntryTable.name + "("
            + DbSchemaM.DiaryEntryTable.Cols.date_added + ", "
            + DbSchemaM.DiaryEntryTable.Cols.rating + ", "
            + DbSchemaM.DiaryEntryTable.Cols.diary_text + ", "
            + DbSchemaM.DiaryEntryTable.Cols.habit_ref
            + ") VALUES (?, ?, ?, ?)",
            (i_date_added_it, i_favorite_it, i_diary_text, i_journal_ref_it)
        )
        db_connection.commit()

        # t_diary_id = db_cursor.lastrowid

    @staticmethod
    def update_note(i_id_it, i_new_text_sg):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.DiaryEntryTable.name
            + " SET " + DbSchemaM.DiaryEntryTable.Cols.diary_text + " = ?"
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.id + " = ?",
            (i_new_text_sg, str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def update_question(i_id_it, i_habit_ref_id_int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.DiaryEntryTable.name
            + " SET " + DbSchemaM.DiaryEntryTable.Cols.habit_ref + " = ?"
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.id + " = ?",
            (str(i_habit_ref_id_int), str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def clear_question(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.DiaryEntryTable.name
            + " SET " + DbSchemaM.DiaryEntryTable.Cols.habit_ref + " = ?"
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.id + " = ?",
            (None, str(i_id_it))
            # -Please note: We cannot use "SQLITE_NULL" (which is the string "null", instead we use None
        )
        db_connection.commit()

    @staticmethod
    def update_date(i_id_it, i_new_time_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.DiaryEntryTable.name
            + " SET " + DbSchemaM.DiaryEntryTable.Cols.date_added + " = ?"
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.id + " = ?",
            (str(i_new_time_it), str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def update_favorite(i_id_it, i_rating: int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.DiaryEntryTable.name
            + " SET " + DbSchemaM.DiaryEntryTable.Cols.rating + " = ?"
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.id + " = ?",
            (str(i_rating), str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def remove(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "DELETE FROM " + DbSchemaM.DiaryEntryTable.name
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.id + "=" + str(i_id_it)
        )
        db_connection.commit()

    @staticmethod
    def get(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryEntryTable.name + " WHERE "
            + DbSchemaM.DiaryEntryTable.Cols.id + "=" + str(i_id_it)
        )
        diary_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return DiaryEntryM(*diary_db_te)

    @staticmethod
    def get_all(i_reverse_bl = False):
        t_direction_sg = "ASC"
        if i_reverse_bl:
            t_direction_sg = "DESC"
        ret_diary_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryEntryTable.name
            + " ORDER BY " + DbSchemaM.DiaryEntryTable.Cols.date_added + " " + t_direction_sg
        )
        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            ret_diary_list.append(DiaryEntryM(*diary_db_te))
        db_connection.commit()
        return ret_diary_list

    @staticmethod
    def get_all_for_search_term(i_search_term_str: str, i_page_number_int: int):
        ret_diary_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryEntryTable.name
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.diary_text
            + " LIKE " + '"%' + i_search_term_str + '%"'
            + " ORDER BY " + DbSchemaM.DiaryEntryTable.Cols.date_added + " DESC "
            + " LIMIT " + str(wbd.wbd_global.diary_entries_per_page_int)
            + " OFFSET " + str(i_page_number_int * wbd.wbd_global.diary_entries_per_page_int)
        )
        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            ret_diary_list.append(DiaryEntryM(*diary_db_te))
        db_connection.commit()

        ret_diary_list.reverse()

        return ret_diary_list

    @staticmethod
    def get_all_for_question(i_question_id_it, i_page_number_int: int):
        ret_diary_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryEntryTable.name
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.habit_ref + "=" + str(i_question_id_it)
            + " ORDER BY " + DbSchemaM.DiaryEntryTable.Cols.date_added + " DESC "
            + " LIMIT " + str(wbd.wbd_global.diary_entries_per_page_int)
            + " OFFSET " + str(i_page_number_int * wbd.wbd_global.diary_entries_per_page_int)
        )
        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            ret_diary_list.append(DiaryEntryM(*diary_db_te))
        db_connection.commit()

        ret_diary_list.reverse()

        return ret_diary_list

    @staticmethod
    def get_all_for_active_day(i_reverse_bl=False):
        start_of_day_datetime = datetime.datetime(
            year=wbd.wbd_global.active_date_qdate.year(),
            month=wbd.wbd_global.active_date_qdate.month(),
            day=wbd.wbd_global.active_date_qdate.day()
        )
        start_of_day_unixtime_it = int(start_of_day_datetime.timestamp())

        ret_diary_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryEntryTable.name
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.date_added + ">=" + str(start_of_day_unixtime_it)
            + " AND " + DbSchemaM.DiaryEntryTable.Cols.date_added + "<" + str(start_of_day_unixtime_it + 24 * 3600)
        )
        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            ret_diary_list.append(DiaryEntryM(*diary_db_te))
        db_connection.commit()

        if i_reverse_bl:
            ret_diary_list.reverse()
        return ret_diary_list

    @staticmethod
    def get_for_question_and_active_day(i_question_id: int) -> list:
        start_of_day_datetime = datetime.datetime(
            year=wbd.wbd_global.active_date_qdate.year(),
            month=wbd.wbd_global.active_date_qdate.month(),
            day=wbd.wbd_global.active_date_qdate.day()
        )
        start_of_day_unixtime_it = int(start_of_day_datetime.timestamp())

        ret_diary_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryEntryTable.name
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.date_added + ">=" + str(start_of_day_unixtime_it)
            + " AND " + DbSchemaM.DiaryEntryTable.Cols.date_added + "<" + str(start_of_day_unixtime_it + 24 * 3600)
            + " AND " + DbSchemaM.DiaryEntryTable.Cols.habit_ref + "=" + str(i_question_id)
        )

        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            ret_diary_list.append(DiaryEntryM(*diary_db_te))
        db_connection.commit()

        return ret_diary_list

    @staticmethod
    def get_all_tags_or_friends(i_special_char_str: str) -> list:
        ret_tag_tuple_list_list = []
        # ret_tag_tuple_list_list: [("#tag1", [id1, id2, ___]), ("#tag2", [id1, id3, ___]), ___]
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryEntryTable.name
            + " WHERE " + DbSchemaM.DiaryEntryTable.Cols.diary_text
            + " LIKE " + '"%' + i_special_char_str + '%"'
        )
        # -http://sqlite.org/lang_expr.html#like
        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            diary_entry = DiaryEntryM(*diary_db_te)
            string_with_hashtag_str = diary_entry.diary_text
            t_diary_id_int = diary_entry.id
            regexp_pattern_obj = re.compile("\\" + i_special_char_str + r"\w+")
            # Please note: we need to escape the caret ("^") character becase this is a
            # special character ("literal")
            regexp_search_result_list = regexp_pattern_obj.findall(string_with_hashtag_str)
            # https://docs.python.org/3/library/re.html

            for t_re_tag_str in regexp_search_result_list:
                # -regexp_search_result_list: ["#tag1", "#tag2", ___]
                flag_boolean = False
                for (t_ret_tag_str, t_ret_diary_id_list) in ret_tag_tuple_list_list:
                    if t_re_tag_str == t_ret_tag_str:
                        t_ret_diary_id_list.append(t_diary_id_int)
                        flag_boolean = True
                        break
                if flag_boolean:
                    break
                else:
                    ret_tag_tuple_list_list.append((t_re_tag_str, [t_diary_id_int]))

        db_connection.commit()

        # TODO: Removing duplicates

        return ret_tag_tuple_list_list


class ReminderM:
    def __init__(self, i_id_int: int, i_title_str: str, i_reminder_str: str) -> None:
        self.id_int = i_id_int
        self.title_str = i_title_str
        self.reminder_str = i_reminder_str

    @staticmethod
    def add(i_title_str: str, i_reminder_str: str) -> None:
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.ReminderTable.name + "("
            + DbSchemaM.ReminderTable.Cols.title + ", "
            + DbSchemaM.ReminderTable.Cols.reminder
            + ") VALUES (?, ?)", (i_title_str, i_reminder_str)
        )

        db_connection.commit()

    @staticmethod
    def get(i_id_int: int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.ReminderTable.name
            + " WHERE " + DbSchemaM.ReminderTable.Cols.id + "=" + str(i_id_int)
        )
        reminder_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return ReminderM(*reminder_db_te)

    @staticmethod
    def get_all():
        ret_reminder_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.ReminderTable.name
        )
        reminder_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in reminder_db_te_list:
            ret_reminder_list.append(ReminderM(*diary_db_te))
        db_connection.commit()
        return ret_reminder_list

    @staticmethod
    def remove(i_id_int):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "DELETE FROM " + DbSchemaM.ReminderTable.name
            + " WHERE " + DbSchemaM.ReminderTable.Cols.id + "=" + str(i_id_int)
        )
        db_connection.commit()


def export_all():
    # If we want to automate this: https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
    csv_writer = csv.writer(open("exported.csv", "w"))
    for diary_item in DiaryEntryM.get_all():
        time_datetime = datetime.date.fromtimestamp(diary_item.date_added_it)
        date_str = time_datetime.strftime("%Y-%m-%d")
        csv_writer.writerow((date_str, diary_item.diary_text))
    for question_item in QuestionM.get_all():
        csv_writer.writerow((question_item.title_str, question_item.title_str))
        csv_writer.writerow((question_item.title_str, question_item.description_str))


def backup_db_file():
    if wbd.wbd_global.testing_bool:
        return
    date_sg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name_sg = wbd.wbd_global.get_database_filename() + "_" + date_sg
    shutil.copyfile(wbd.wbd_global.get_database_filename(), new_file_name_sg)
    return


def populate_db_with_test_data():
    delta_day_it = 24 * 60 * 60

    meditation_id_int = QuestionM.add(
        "Meditation",
        "Meditation description",
        i_hour=10)
    lunch_id_int = QuestionM.add(
        "Lunch",
        "Lunch description",
        i_hour=12)

    gratitude_journal_id_int = JournalM.add("Gratitude", "")
    mind_cultivation_journal_id_int = JournalM.add("Mind cultivation", "")
    contribution_journal_id_int = JournalM.add("Contribution", "Contribution and generosity")
    wisdom_journal_id_int = JournalM.add("Wisdom", "")

    gratitude_id_int = QuestionM.add(
        QuestionSetupEnum.gratitude.name.capitalize(),
        "What did I do to water the seeds of joy in myself today? What posivite things came my way today?")
    practice_id_int = QuestionM.add(
        QuestionSetupEnum.practice.name.capitalize(),
        "What practices did I do today? Sitting meditation ? Walking meditation? Gathas?")
    sharing_id_int = QuestionM.add(
        QuestionSetupEnum.sharing.name.capitalize(),
        "Did I share my happiness with others? Did I enjoy the happiness of others?")
    contribution_id_int = QuestionM.add(
        QuestionSetupEnum.contribution.name.capitalize(),
        "How did I contribute to the well-being on others? Did I share my joy with my friends and family?")
    study_id_int = QuestionM.add(
        QuestionSetupEnum.study.name.capitalize(),
        "What did I read and listen to today and learn? Dharma talks? Lectures? Books? Sutras?")

    DiaryEntryM.add(
        time.time(), SQLITE_FALSE,
        "Dear Buddha, today i was #practicing #sitting meditation before meeting a friend of mine to be able to be more present during our meeting",
        wbd.wbd_global.NO_ACTIVE_QUESTION_INT)

    DiaryEntryM.add(
        time.time(), SQLITE_FALSE,
        "Dear Buddha, i'm #grateful for being able to breathe!",
        gratitude_id_int)
    DiaryEntryM.add(time.time() - delta_day_it, SQLITE_FALSE,
        "Most difficult today was my negative thinking, #practicing with this by changing the peg from negative thoughts to positive thinking",
        practice_id_int)
    DiaryEntryM.add(
        time.time() - 7 * delta_day_it, SQLITE_FALSE,
        "Grateful for having a place to live, a roof over my head, food to eat, and people to care for",
        gratitude_id_int)
    DiaryEntryM.add(
        time.time() - 7 * delta_day_it, SQLITE_FALSE,
        "Grateful for the blue sky and the white clouds",
        gratitude_id_int)
    DiaryEntryM.add(
        time.time() - 3 * delta_day_it, SQLITE_FALSE,
        "Dear Buddha, today i read about the four foundations of mindfulness. Some important parts: 1. Body 2. Feelings 3. Mind 4. Objects of mind",
        study_id_int)
    DiaryEntryM.add(
        time.time() - 4 * delta_day_it, SQLITE_FALSE,
        "Programming and working on the application. Using Python and Qt. Cooperating with @John and @Emma",
        contribution_id_int)
    DiaryEntryM.add(
        time.time(), SQLITE_FALSE,
        "Dharma talk from ^Plum-Village",
        practice_id_int)

    ReminderM.add("Inter-being",
        "All things in the universe inter-are, our suffering and happiness inter-is with the suffernig and happiness of others")
    ReminderM.add("No Mud, no lotus",
        "A lotus flower cannot grow on marble!")

