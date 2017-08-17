import sqlite3
import sys
import logging
import argparse
import configparser

import PyQt5
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import wbd.wbd_global


if __name__ == "__main__":
    # Application setup..
    # ..command line arguments
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--persistent", "-p", help="Persistent db storage", action="store_true")
    # -for info about "store_true" please search here: https://docs.python.org/3/howto/argparse.html
    args = argument_parser.parse_args()
    if args.persistent:
        wbd.wbd_global.persistent_bool = True
    else:
        wbd.wbd_global.persistent_bool = False

    # ..configuration file
    config = configparser.ConfigParser()
    config.read("settings.ini")
    wbd.wbd_global.background_image_path = config["general"]["background-image-path"]
    wbd.wbd_global.diary_text_size_ft = float(config["general"]["diary-text-size"])

    # === Creating the main window ===
    app = QtWidgets.QApplication(sys.argv)
    # -"QWidget: Must construct a QApplication before a QWidget"
    main_window = wbd.window.WellBeingWindow()

    # System tray
    tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icon.png"), app)
    tray_menu = QtWidgets.QMenu()
    tray_restore_action = QtWidgets.QAction("Restore")
    # noinspection PyUnresolvedReferences
    tray_restore_action.triggered.connect(main_window.show)
    tray_menu.addAction(tray_restore_action)
    tray_quit_action = QtWidgets.QAction("Quit")
    # noinspection PyUnresolvedReferences
    tray_quit_action.triggered.connect(sys.exit)
    tray_menu.addAction(tray_quit_action)
    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    # Application information
    logging.info("===== Starting " + wbd.wbd_global.BWB_APPLICATION_NAME_STR + " - "
        + wbd.wbd_global.BWB_APPLICATION_VERSION_STR + " =====")
    logging.info("Python version: " + str(sys.version))
    logging.info("SQLite version: " + str(sqlite3.sqlite_version))
    logging.info("PySQLite (Python module) version: " + str(sqlite3.version))
    logging.info("Qt version: " + str(QtCore.qVersion()))
    logging.info("PyQt (Python module) version: " + str(PyQt5.Qt.PYQT_VERSION_STR))
    logging.info(wbd.wbd_global.BWB_APPLICATION_NAME_STR + " Application version: " + str(wbd.wbd_global.BWB_APPLICATION_VERSION_STR))
    db_conn = wbd.model.DbHelperM.get_db_connection()
    logging.info(wbd.wbd_global.BWB_APPLICATION_NAME_STR + " Database schema version: " + str(wbd.model.get_schema_version(db_conn)))
    logging.info("=====")

    sys.exit(app.exec_())
