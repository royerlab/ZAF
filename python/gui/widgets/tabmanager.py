import json

from PyQt5.QtWidgets import (
    QTabWidget,
)
from PyQt5.QtCore import QThreadPool
from crontab import CronTab

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

        self.cron = CronTab(user='pi')

        self.only_valid_files = []
        self.active_tabs = []
        self.tabs = []
        self.program_tabs = []

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
        self.update_valid_json_files_list()

        for file_path in self.only_valid_files:
            with open(file_path) as json_file:
                data = json.load(json_file)

                tab1 = ProgramTab(self, name=data["Program_name"])
                self.tabs.append(tab1)
                self.program_tabs.append(tab1)

                tab1.reset(data)

                self.addTab(tab1, tab1.name)

        self.check_active_tabs()

    def addprogramtab(self):
        self.update_valid_json_files_list()

        # Check how many ProgramTab are there and find first available integer index
        valid_program_indices = set()
        for file_path in self.only_valid_files:
            index_and_format = file_path.split("Program")[1]
            index = int(index_and_format.split(".")[0])
            valid_program_indices.add(index)

        j=1
        while j in valid_program_indices:
            j += 1

        name = f"Program{j}"
        tab1 = ProgramTab(self, name=name)

        self.tabs.append(tab1)
        self.program_tabs.append(tab1)
        self.addTab(tab1, tab1.name)

        self.check_active_tabs()

    def check_active_tabs(self):
        self.active_tabs = []
        for tb in self.tabs:
            if isinstance(tb, ProgramTab):
                self.active_tabs.append({tb.name: tb.is_enabled_checkbox})
        self.tabs[0].update_program_list()

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
                    if tab.program_settings["Program"] == pg["Program"]:
                        for key, val in pg.items():
                            tab.program_settings[key] = val
                        tab.reset(tab.program_settings)
        self.check_active_tabs()

    def update_valid_json_files_list(self):
        json_folder_path = "/home/pi/Dev/prod/zaf_data"

        from os import listdir
        from os.path import isfile, join
        self.only_valid_files = [
            join(json_folder_path, f) for f in listdir(json_folder_path) if isfile(join(json_folder_path, f)) and "json" in f
        ]

    def update_crontab_job(self):

        self.cron.remove_all()

        for program_tab in self.program_tabs:

            if program_tab.program_settings["Day"] is not None and program_tab.program_settings["Enabled"]:

                hour, _, minute, _ = program_tab.program_settings["Time"].split()

                program_tab.cron_job = self.cron.new(
                    command=f'cd Dev/prod/ZAF && python3 -m python.zaf_plus.fishfeed {program_tab.json_path}',
                    comment=program_tab.name
                )
                program_tab.cron_job.hour.on(hour)
                program_tab.cron_job.minute.on(minute)

                dow = [day.upper() for day in program_tab.program_settings["Day"]]

                if dow:
                    program_tab.cron_job.dow.on(*dow)

        self.cron.write()
