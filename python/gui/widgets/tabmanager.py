import json

from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QThreadPool

from python.gui.widgets.tabs.dashboard import DashboardTab
from python.gui.widgets.tabs.logtab import LogTab
from python.gui.widgets.tabs.program import ProgramTab

"""
This script creates a TabManager that manages multiple tabs.

"""


class TabManager(QTabWidget):
    def __init__(self, parent, status_bar):
        super().__init__()
        self.parent = parent
        self.threadpool = QThreadPool()
        self.status_bar = status_bar

        self.only_valid_files = []
        self.active_tabs = []
        self.tabs = []

        self.dashboard_tab = DashboardTab(self)
        self.tabs.append(self.dashboard_tab)
        self.addTab(self.dashboard_tab, self.dashboard_tab.name)

        self.log_tab = LogTab(self)
        self.tabs.append(self.log_tab)
        self.addTab(self.log_tab, self.log_tab.name)

        self.populate_programs()

        self.tabBarClicked.connect(lambda: self.check_active_tabs())
            # self.setTabsClosable(True)

    def populate_programs(self):
        json_folder_path = "/home/pi/Dev/prod/zaf_data"

        from os import listdir
        from os.path import isfile, join
        self.only_valid_files = [f for f in listdir(json_folder_path) if isfile(join(json_folder_path, f)) and "json" in f]

        for file in self.only_valid_files:
            with open(join(json_folder_path, file)) as json_file:
                data = json.load(json_file)

                tab1 = ProgramTab(self, name=data["Program_name"])

                self.tabs.append(tab1)
                self.addTab(tab1, tab1.name)

    def addprogramtab(self):
        # Check how many ProgramTab are there
        num_ptab = []
        for i in self.tabs:
            if isinstance(i, ProgramTab):
                num_ptab.append(int(i.objectName().split(" ")[-1]))
        num_ptab.sort()
        j = 1
        for i in num_ptab:
            if j == i:
                j += 1
            else:
                break
        name = f"Program {j}"
        tab = QWidget()
        tab.setObjectName(name)
        tab.layout = QHBoxLayout()
        tab.layout.setAlignment(Qt.AlignCenter)
        tab1 = ProgramTab(self, tab)
        tab1.setObjectName(name)
        self.tabs.append(tab1)
        self.insertTab(j + 1, tab, name)  # .addTab(tab, name)

    def check_active_tabs(self):
        self.active_tabs = []
        for tb in self.tabs:
            if isinstance(tb, ProgramTab):
                self.active_tabs.append({tb.objectName(): tb.is_enabled})
        self.tabs[0].update_active_program_list()

    def reconstruct_program(self, data):
        # Check number of ProgramTabs
        num_pgtab = 0
        for tab in self.tabs:
            if isinstance(tab, ProgramTab):
                num_pgtab += 1
        # add tabs if needed
        for _ in range(len(data) - num_pgtab):
            self.addprogramtab()

        # reconstruct tabs
        for pg in data:
            for tab in self.tabs:
                if isinstance(tab, ProgramTab):
                    if tab.program_log["Program"] == pg["Program"]:
                        for key, val in pg.items():
                            tab.program_log[key] = val
                        tab.reset(tab.program_log)
        self.check_active_tabs()
