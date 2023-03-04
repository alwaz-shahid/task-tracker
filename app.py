import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber, QComboBox
from PyQt5.QtCore import QTimer, Qt, QTime

class TimeTracker(QWidget):

    def __init__(self):
        super().__init__()
        self.tasks = {}
        self.initUI()

    def initUI(self):
        # Create widgets
        self.task_label = QLabel("Task:")
        self.task_combo = QComboBox()
        self.task_combo.addItem("")
        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Stop")
        self.time_lcd = QLCDNumber()
        self.time_lcd.setDigitCount(8)
        self.time_lcd.display("00:00:00")

        # Create layout
        task_layout = QHBoxLayout()
        task_layout.addWidget(self.task_label)
        task_layout.addWidget(self.task_combo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.stop_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(task_layout)
        main_layout.addWidget(self.time_lcd)
        main_layout.addLayout(button_layout)

        # Set widget properties
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)

        # Set layout
        self.setLayout(main_layout)

        # Connect signals and slots
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.stop_btn.clicked.connect(self.stop_timer)
        self.task_combo.currentTextChanged.connect(self.update_task_combo)

        # Set timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time_lcd)

    def update_task_combo(self):
        current_task = self.task_combo.currentText()
        if current_task:
            self.start_btn.setEnabled(True)
        else:
            self.start_btn.setEnabled(False)

    def start_timer(self):
        current_task = self.task_combo.currentText()
        self.tasks[current_task] = {"elapsed_time": QTime(0, 0, 0), "timer_id": self.timer.start()}

        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)

    def pause_timer(self):
        current_task = self.task_combo.currentText()
        self.timer.stop()

        if current_task in self.tasks:
            self.tasks[current_task]["elapsed_time"] = self.tasks[current_task]["elapsed_time"].addMSecs(self.timer.remainingTime())
            self.tasks[current_task]["timer_id"] = None

        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_timer(self):
        current_task = self.task_combo.currentText()
        self.timer.stop()

        if current_task in self.tasks:
            self.tasks[current_task]["elapsed_time"] = self.tasks[current_task]["elapsed_time"].addMSecs(self.timer.remainingTime())
            self.tasks[current_task]["timer_id"] = None

            # Save time data
            print(f"Task: {current_task}, Time: {self.tasks[current_task]['elapsed_time'].toString('hh:mm:ss')}")

        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)

    def update_time_lcd(self):
        current_task = self.task_combo.currentText()

        if current_task in self.tasks and self.tasks[current_task]["timer_id"] is not None:
            elapsed_time = self.tasks[current_task]["elapsed_time"].addMSecs(self.timer.remainingTime())
            self.time_lcd.display(elapsed_time.toString("hh:mm:ss"))

    def run(self):
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TimeTracker()
    ex.run()

