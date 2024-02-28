from PyQt6.QtCore import  Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
     QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, \
     QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
import mysql.connector


class DatabaseConnection:
    def  __init__(self, host = "localhost", user = "root", password = "sUrya@8394096721", database = "school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database
        )
        return  connection


class MainWindow(QMainWindow):
    """QMainWindow allows us to add a menu bar and tool bars and a status bar
 And QMainWindow is the class that allows us to do this division between, among
 the different sections 
 But QWidget doesn't have that capability
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        #Adding  a Menu Bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        #Adding the submenu item in "File" menu and this submenu items are actually known as actions
        add_student_action = QAction(QIcon(rf"D:\Student_ManagementSystem_UsingPyQt\icons\add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.add_NewStudentData)
        file_menu_item.addAction(add_student_action)

        #Adding the submenu item in "Help" menu
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        #If help menu not showing
        # about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        #Adding the submenu item in "Edit" menu
        find_students_action = QAction(QIcon("D:\Student_ManagementSystem_UsingPyQt\icons\search.png"), 'Search', self)
        edit_menu_item.addAction(find_students_action)
        find_students_action.triggered.connect(self.show_searchStudents)
        

        #Adding the table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile", "Age", "Gender", "Address"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        #Creating toolbar and adding toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(find_students_action)

        #Creating status bar and adding status bar element
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        #Detecting a cell click
        self.table.cellClicked.connect(self.getCellValue)
    
    def getCellValue(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children  = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):

        """Laoding data from the  database into our table"""
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
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

    def edit(self):
        """This function will be called when we click on the Edit button of any record."""
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        """This function will be called when we click on the Delete button of any record."""
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        """Displaying About Window"""
        dialog = AboutDialog()
        dialog.exec()



class AboutDialog(QMessageBox):
    """About Dialog Class"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
Hello ! This is a simple database management system developed using PyQt6 and SQLite3.  
The main purpose of this application is to demonstrate how you can use SQL with Python  
to perform basic operations such as adding, editing, deleting records from a database.  
You are free to modify and distribute it according to your needs.  
If you have any questions or suggestions, please feel free to contact me at:   
suryaprakashsharma453@gmail.com
"""
        self.setText(content)


class EditDialog(QDialog):
    """docstring for EditDialog"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Details")
        self.setFixedWidth(500)
        self.setFixedHeight(600)

        layout = QVBoxLayout()

        #Getting student name from selected row
        index = main_window.table.currentRow() #this method wil return an integer
        student_name = main_window.table.item(index, 1).text()

        #Getting id from selected row
        self.student_id = main_window.table.item(index, 0).text()

        #Adding Student name widget
        self.Student_name = QLineEdit(student_name)
        self.Student_name.setPlaceholderText("StudentName")
        layout.addWidget(self.Student_name)

        #Adding course name widget 
        course_n = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        #self.course_name.setPlaceholderText("ChooseCourse")
        courses = ["Biology", "Physics", "Mathematics", "Computer Science", "Astronomy", "Economy", \
                   "Political Science", "Sociology", "History", "Geography", "French", "Spanish", \
                   "Chemistry", "DSA", "English", "Cloud Computing", "Artificial Intelligence", \
                   "DBMS", "Operating System", "Networking"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_n)
        layout.addWidget(self.course_name)

        #Adding mobile number
        mobile_no = main_window.table.item(index, 3).text()
        self.mobile_number = QLineEdit(mobile_no)
        self.mobile_number.setPlaceholderText("MobileNumber")
        layout.addWidget(self.mobile_number)

        #Adding age, gender and address
        ag = main_window.table.item(index, 4).text()
        self.age = QLineEdit(ag)
        self.age.setPlaceholderText("Age")
        layout.addWidget(self.age)

        gend = main_window.table.item(index, 5).text()
        self.gender = QComboBox()
        #self.gender.setPlaceholderText( "Gender")
        self.gender.addItems(['M', 'F'])
        self.gender.setCurrentText(gend)
        layout.addWidget(self.gender)

        add = main_window.table.item(index, 6).text()
        self.address = QLineEdit(add)
        self.address.setPlaceholderText("StudentAddress")
        layout.addWidget(self.address)

        #Adding a  Submit Button
        submitButton=QPushButton('Update')
        submitButton.clicked.connect(self.update_StudentData)
        layout.addWidget(submitButton)

        #Setting the Layout of the Widget to the QVBoxLayout
        self.setLayout(layout)

    def update_StudentData(self):
        """This function is used to update the student data"""
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, course = %s, mobile = %s, age = %s, \
                       gender = %s, address = %s WHERE id = %s", 
                       (self.Student_name.text(), self.course_name.itemText(self.course_name.currentIndex()), 
                        self.mobile_number.text(), self.age.text(), 
                        self.gender.itemText(self.gender.currentIndex()), 
                        self.address.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        #Refreshing the table
        main_window.load_data()

        self.close()


class DeleteDialog(QDialog):
    """docstring for DeleteDialog"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Details")

        layout = QGridLayout()

        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2) 
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no,  1, 1)

        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.reject)

    def delete_student(self):
        """This method deletes a record from database."""
        #Getting index and id from selected row
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = %s", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()

        #Removing the deleted data from TableView
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record Deleted Successfully!")
        confirmation_widget.exec()


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
        gender_list = ['M', 'F']
        self.gender.addItems(gender_list)
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
        gender = self.gender.itemText(self.gender.currentIndex())
        address = self.address.text().strip()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile, age, gender, address) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, course, mobile, age, gender, address))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()


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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name = %s", (name, ))
        result = cursor.fetchall()
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name,
         Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

        self.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())