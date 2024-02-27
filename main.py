from PyQt6.QtCore import  Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
     QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, \
     QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    """QMainWindow allows us to add a menu bar and tool bars and a status bar
 And QMainWindow is the class that allows us to do this division between, among
 the different sections 
 But QWidget doesn't have that capability
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        #Adding  a Menu Bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        #Adding the submenu item in "File" menu and this submenu items are actually known as actions
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.add_NewStudentData)
        file_menu_item.addAction(add_student_action)

        #Adding the submenu item in "Help" menu
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        #If help menu not showing
        # about_action.setMenuRole(QAction.MenuRole.NoRole)

        #Adding the submenu item in "Edit" menu
        find_students_action = QAction('Search', self)
        find_students_action.triggered.connect(self.show_searchStudents)
        edit_menu_item.addAction(find_students_action)
        

        #Adding the table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile", "Age", "Gender", "Address"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):

        """Laoding data from the  database into our table"""
        connection = sqlite3.connect("D:\Student_ManagementSystem_UsingPyQt\database.db")
        result = connection.execute("SELECT * FROM students")
        # This allow whenever we laod the program or do something these data will not be added on top of the existing data
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number) #it is used to insert the empty row
            for column_number, data in enumerate(row_data):
                #It is used to populate the cells or insert the actual data
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def add_NewStudentData(self):
        """Adding the new student data into the table"""
        dialog = InsertDialog()
        dialog.exec()

    def show_searchStudents(self):
        """Showing search window"""
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    """It generates new pop-up window when the user click on the add student action"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Student Details")
        self.setFixedWidth(500)
        self.setFixedHeight(600)

        layout = QVBoxLayout()

        #Adding Student name widget
        self.Student_name = QLineEdit()
        self.Student_name.setPlaceholderText("StudentName")
        layout.addWidget(self.Student_name)

        #Adding course name widget 
        self.course_name = QComboBox()
        self.course_name.setPlaceholderText("ChooseCourse")
        courses = ["Biology", "Physics", "Mathematics", "Computer Science", "Astronomy", "Economy", \
                   "Political Science", "Sociology", "History", "Geography", "French", "Spanish", \
                   "Chemistry", "DSA", "English", "Cloud Computing", "Artificial Intelligence", \
                   "DBMS", "Operating System", "Networking"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        #Adding mobile number
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("MobileNumber")
        layout.addWidget(self.mobile_number)

        #Adding age, gender and address
        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")
        layout.addWidget(self.age)

        self.gender = QComboBox()
        self.gender.setPlaceholderText( "Gender")
        self.gender.addItems(['M', 'F'])
        layout.addWidget(self.gender)

        self.address = QLineEdit()
        self.address.setPlaceholderText("StudentAddress")
        layout.addWidget(self.address)

        #Adding a  Submit Button
        submitButton=QPushButton('Submit')
        submitButton.clicked.connect(self.add_StudentData)
        layout.addWidget(submitButton)

        #Setting the Layout of the Widget to the QVBoxLayout
        self.setLayout(layout)

    def  add_StudentData(self):
        name = self.Student_name.text().strip()
        course = self.course_name.itemText(self.course_name.currentIndex()).capitalize()
        mobile = self.mobile_number.text().strip()
        age = self.age.text().strip()
        gender = self.gender.currentText()
        address = self.address.text().strip()
        connection = sqlite3.connect("D:\Student_ManagementSystem_UsingPyQt\database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile, age, gender, address) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, course, mobile, age, gender, address))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    """docstring for SearchDialog"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedWidth(200)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        #Adding Search Widget
        self.searchLabel =QLineEdit()
        self.searchLabel.setPlaceholderText("Enter name to search")
        layout.addWidget(self.searchLabel)

        searchButton = QPushButton("Search")
        searchButton.clicked.connect(self.show_result)
        layout.addWidget(searchButton)

        self.setLayout(layout)

    def show_result(self):
        name = self.searchLabel.text()
        connection = sqlite3.connect('D:/Student_ManagementSystem_UsingPyQt/database.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,)).fetchall()
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name,
         Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())