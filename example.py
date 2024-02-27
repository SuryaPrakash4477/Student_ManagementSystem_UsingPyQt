from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
     QLineEdit, QPushButton

import sys
from datetime import datetime


#QWidget is used to create the windows
class AgeCalculator(QWidget):
    def __init__(self):
        #This line means that I am calling the constructor of the parent class i.e., QWidget
        #super() is a function which return the parent of the class
        """Super class is the parent class, in other words an it is saying that the
    __init__ method  of the parent class should be called when we overwrite that method
    again in a child class.
        """
        super().__init__()
        self.setWindowTitle("Age Calculator") 
        grid = QGridLayout()

        #Creating Widget
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        date_birth_label = QLabel("Date of Birth MM/DD/YYYY:")
        self.date_birth_line_edit = QLineEdit()

        # Adding button widget to the grid
        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        #Adding all the above widget to the grid object
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_birth_label, 1, 0)
        grid.addWidget(self.date_birth_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        #To add that grid object to the the AgeCalculator widget
        #self symbolizes the instance, the AgeCalculator instance
        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        date_of_birth = self.date_birth_line_edit.text()
        year_of_birth = datetime.strptime(date_of_birth,  "%m/%d/%Y").date().year
        age = current_year - year_of_birth
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old.")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())