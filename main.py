# importing libraries
from PySide6.QtWidgets import *
from PySide6.QtSql import QSqlDatabase
import sys
import mysql.connector


# creating a class
# that inherits the QDialog class
class Window(QDialog):

    # constructor
    def __init__(self):
        super(Window, self).__init__()

        # setting window title
        self.setWindowTitle("Form App")

        # setting geometry to the window
        self.setGeometry(100, 100, 600, 600)

        # creating a group box
        self.formGroupBox = QGroupBox("Form 1")



        # creating a line edit
        self.nameLineEdit = QLineEdit()

        self.emailLineEdit = QLineEdit()

        self.prodiLineEdit = QLineEdit()

        self.save = QPushButton('Simpan',self)

        self.save.resize(100, 30)
        self.save.setStyleSheet('background-color:rgb(0, 79, 170);color:white')

        # calling the method that create the form
        self.createForm()




        # adding action when form is accepted
        self.save.clicked.connect(self.saveToDatabase)
        self.save.clicked.connect(self.loadTable)



        # creating a vertical layout
        mainLayout = QVBoxLayout()

        hbox = QHBoxLayout()

        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)

        # db
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="desktop"
        )
        if self.db.is_connected():
            print("Berhasil terhubung ke database")

        # table

        self.tableWidget = QTableWidget(12, 3, self)






        # adding form group box to the layout
        mainLayout.addWidget(self.tableWidget)



        self.loadTable()




        # setting lay out
        self.setLayout(mainLayout)






    # get info method called when form is accepted
    def saveToDatabase(self):
        cursor = self.db.cursor()
        sql = "INSERT INTO data (nama,email, prodi) VALUES (%s, %s, %s)"
        val = (self.nameLineEdit.text(), self.emailLineEdit.text(), self.prodiLineEdit.text())
        cursor.execute(sql, val)

        self.db.commit()

        print("{} data ditambahkan".format(cursor.rowcount))

    # creat form method
    def createForm(self):
        # creating a form layout
        hbox = QHBoxLayout()
        layout = QFormLayout()

        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Name"), self.nameLineEdit)

        layout.addRow(QLabel("Email"), self.emailLineEdit)

        hbox.addWidget(self.prodiLineEdit)
        hbox.addWidget(self.save)
        hbox.addStretch()

        layout.addRow(QLabel("Prodi"),hbox)




        # save button
        layout.addRow(self.save)

        # setting layout
        self.formGroupBox.setLayout(layout)

    def loadTable(self):
        cursor = self.db.cursor()
        sql = "SELECT * FROM data"
        cursor.execute(sql)

        results = cursor.fetchall()

        for n,data in enumerate(results):
            for m, item in enumerate(data):
                newitem = QTableWidgetItem(item)
                self.tableWidget.setItem(n, m, newitem)

# main method
if __name__ == '__main__':
    # create pyqt5 app
    app = QApplication(sys.argv)

    # create the instance of our Window
    window = Window()

    # showing the window
    window.show()

    # start the app
    sys.exit(app.exec())