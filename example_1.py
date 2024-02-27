from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
     QLineEdit, QPushButton, QComboBox
import sys


class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()

        #Creating Widget
        distance_label = QLabel("Distance: ")
        self.distance_edit = QLineEdit()

        self.combo_box = QComboBox()
        self.combo_box.addItems(['Metirc(Km)', 'Imperial(Miles)'])

        time_label = QLabel("Time(hours): ")
        self.time_edit = QLineEdit()


        button =  QPushButton("Calculate")
        button.clicked.connect(self.calculate_speed)
        self.output_label = QLabel("")

        #Adding widget to Grid Layout
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_edit,  0, 1)
        grid.addWidget(self.combo_box, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_edit, 1, 1)
        grid.addWidget(button, 2, 1, 1, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_speed(self):
        #Getting distance and time values
        distance = float(self.distance_edit.text())
        time = float(self.time_edit.text())

        #Calculating average speed
        speed = distance/time

        #Checking what user chose in the combo
        if self.combo_box.currentText() == "Metirc(Km)":
            speed = round(speed, 2)
            unit = 'km/h'
        if  self.combo_box.currentText() == "Imperial(Miles)":
            speed = round(speed * 0.621371, 2)
            unit = 'mi/h'

        #Displaying result on the screen
        self.output_label.setText(f"The average speed is {speed} {unit}")


app = QApplication(sys.argv)
speed_calculator = SpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())
