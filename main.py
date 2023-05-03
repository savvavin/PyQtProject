import sys
import sqlite3

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.setFixedSize(249, 195)
        self.login_btn.clicked.connect(self.login)
        self.signup_btn.clicked.connect(self.signup)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.id = 0
        self.login = ''
        self.password = ''
        self.counter = 1
        self.info = []

    def login(self):
        if (self.login_text.text() != '') and (self.password_text.text() != ''):
            res = self.connection.cursor().execute("""SELECT * FROM users
                        WHERE login = ? AND 
                        password = ?""", (self.login_text.text(), self.password_text.text())).fetchall()

            if len(res) != 0:
                self.id = res[0][0]
                self.login = res[0][1]
                self.password = res[0][2]
                self.info = res[0]

                if self.login == 'admin':
                    self.windowAdmin = MainWindowAdmin(self.info)
                    self.windowAdmin.show()
                    self.close()
                else:
                    self.windowUser = MainWindow(self.info)
                    self.windowUser.show()
                    self.close()
            else:
                self.sost.setText('неверный логин или пароль')
        else:
            self.sost.setText('поля пустые!')

    def signup(self):
        if (self.login_text.text() != '') and (self.password_text.text() != ''):
            res = self.connection.cursor().execute("SELECT * FROM users").fetchall()
            for i in res:
                if self.login_text.text() != i[1]:
                    self.connection.cursor().execute("""INSERT INTO users(login, password)
                    VALUES(?,?)""", (self.login_text.text(), self.password_text.text())).fetchall()
                    self.connection.commit()
                    self.sost.setText('пользователь успешно зарегестрирован')
                    break
                else:
                    self.sost.setText('логин уже занят')
        else:
            self.sost.setText('поля пустые!')


class MainWindow(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setFixedSize(706, 562)
        self.post_btn.clicked.connect(self.post)
        self.reload_btn.clicked.connect(self.reload)
        self.profile_btn.clicked.connect(self.profile)
        self.search_btn.clicked.connect(self.search)
        self.delete_btn.clicked.connect(self.delete)
        self.exit_btn.clicked.connect(self.exit)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.reload()
        self.id = info[0]
        self.login = info[1]
        self.password = info[2]
        self.info = info

    def reload(self):
        res = self.connection.cursor().execute("SELECT * FROM posts").fetchall()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader()
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    def post(self):
        post_text = self.post_text.toPlainText()
        self.connection.cursor().execute("""INSERT INTO posts(login, text)
        VALUES(?,?)""", (self.login, post_text)).fetchall()
        self.connection.commit()
        self.reload()

    def profile(self):
        self.profileUser = Profile(self.info)
        self.profileUser.show()
        self.close()

    def search(self):
        self.searchUser = Search(self.info)
        self.searchUser.show()
        self.close()

    def delete(self):
        self.deleteUser = Delete(self.info)
        self.deleteUser.show()
        self.close()

    def exit(self):
        self.LoginUser = Login()
        self.LoginUser.show()
        self.close()


class Delete(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi('delete.ui', self)
        self.setFixedSize(309, 252)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.delete_btn.clicked.connect(self.delete)
        self.back_btn.clicked.connect(self.back)
        self.info = info

    def delete(self):
        delete_text = 0
        try:
            delete_text = int(self.delete_text.text())
        except ValueError:
            self.label_text.setText('неккоректное значение')
        res = self.connection.cursor().execute("SELECT * FROM posts").fetchall()
        for i in res:
            if i[0] == delete_text:
                if i[1] == self.info[1]:
                    self.connection.cursor().execute("""DELETE from posts
                    where id = ?""", (delete_text,)).fetchall()
                    self.connection.commit()
                    self.label_text.setText('успешно')
        if self.label_text.text() == '':
            self.label_text.setText('неверно')

    def back(self):
        self.windowUser = MainWindow(self.info)
        self.windowUser.show()
        self.close()


class MainWindowAdmin(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi('main_window_admin.ui', self)
        self.setFixedSize(704, 566)
        self.post_btn.clicked.connect(self.post)
        self.reload_btn.clicked.connect(self.reload)
        self.profile_btn.clicked.connect(self.profile)
        self.search_btn.clicked.connect(self.search)
        self.delete_btn.clicked.connect(self.delete)
        self.exit_btn.clicked.connect(self.exit)
        self.deletepers_btn.clicked.connect(self.deletepers)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.reload()
        self.id = info[0]
        self.login = info[1]
        self.password = info[2]
        self.info = info

    def reload(self):
        res = self.connection.cursor().execute("SELECT * FROM posts").fetchall()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    def post(self):
        post_text = self.post_text.toPlainText()
        self.connection.cursor().execute("""INSERT INTO posts(login, text)
        VALUES(?,?)""", (self.login, post_text)).fetchall()
        self.connection.commit()
        self.reload()

    def profile(self):
        self.profileUser = Profile(self.info)
        self.profileUser.show()
        self.close()

    def search(self):
        self.searchAdmin = SearchAdmin(self.info)
        self.searchAdmin.show()
        self.close()

    def delete(self):
        self.deleteAdmin = DeleteAdmin(self.info)
        self.deleteAdmin.show()
        self.close()

    def exit(self):
        self.LoginUser = Login()
        self.LoginUser.show()
        self.close()

    def deletepers(self):
        self.DeletePers = DeletePers(self.info)
        self.DeletePers.show()
        self.close()


class DeletePers(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi('deletepers.ui', self)
        self.setFixedSize(660, 316)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.delete_btn.clicked.connect(self.delete)
        self.back_btn.clicked.connect(self.back)
        self.reload()
        self.info = info

    def delete(self):
        delete_textt = 0
        try:
            delete_textt = int(self.line_text.text())
        except ValueError:
            self.label_text.setText('неккоректное значение')
        self.label_text.setText('')
        res = self.connection.cursor().execute("SELECT * FROM users").fetchall()
        for i in res:
            if i[0] == delete_textt:
                self.connection.cursor().execute("""DELETE from users
                                    where id = ?""", (delete_textt,)).fetchall()
                self.connection.commit()
                self.label_text.setText('успешно')
        if self.label_text.text() == '':
            self.label_text.setText('неверно')
        self.reload()

    def reload(self):
        res = self.connection.cursor().execute("SELECT * FROM users").fetchall()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    def back(self):
        self.windowAdmin = MainWindowAdmin(self.info)
        self.windowAdmin.show()
        self.close()


class SearchAdmin(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi('search.ui', self)
        self.setFixedSize(423, 487)
        self.search_btn.clicked.connect(self.search)
        self.back_btn.clicked.connect(self.back)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.info = info

    def search(self):
        search_text = self.search_text.text()
        res = self.connection.cursor().execute("SELECT * FROM users").fetchall()
        for i in res:
            if i[1] == search_text:
                self.login_text.setText(i[1])
                self.password_text.setText(i[2])
                self.desc_text.setText(i[3])
        if self.login_text.text() == '':
            self.login_text.setText('не найдено')
            self.password_text.setText('не найдено')
            self.desc_text.setText('не найдено')

    def back(self):
        self.windowAdmin = MainWindowAdmin(self.info)
        self.windowAdmin.show()
        self.close()


class DeleteAdmin(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi('delete.ui', self)
        self.setFixedSize(309, 252)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.delete_btn.clicked.connect(self.delete)
        self.back_btn.clicked.connect(self.back)
        self.info = info

    def delete(self):
        delete_text = 0
        try:
            delete_text = int(self.delete_text.text())
        except ValueError:
            self.label_text.setText('неккоректное значение')
        res = self.connection.cursor().execute("SELECT * FROM posts").fetchall()
        for i in res:
            if i[0] == delete_text:
                self.connection.cursor().execute("""DELETE from posts
                where id = ?""", (delete_text,)).fetchall()
                self.connection.commit()
                self.label_text.setText('успешно')
        if self.label_text.text() == '':
            self.label_text.setText('неверно')

    def back(self):
        self.windowAdmin = MainWindowAdmin(self.info)
        self.windowAdmin.show()
        self.close()


class Profile(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi('profile.ui', self)
        self.setFixedSize(439, 383)
        self.id = info[0]
        self.log.setText(str(info[1]))
        self.pas.setText(str(info[2]))
        self.save_btn.clicked.connect(self.save)
        self.back_btn.clicked.connect(self.back)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.info = info
        res = self.connection.cursor().execute("SELECT * FROM users").fetchall()
        for i in res:
            if i[0] == self.id:
                self.descc.setText(i[3])

    def save(self):
        desc_text = self.desc.text()
        self.connection.cursor().execute("""UPDATE users
        SET description = ?
        WHERE id = ?""", (desc_text, self.id)).fetchall()
        self.connection.commit()
        res = self.connection.cursor().execute("SELECT * FROM users").fetchall()
        for i in res:
            if i[0] == self.id:
                self.descc.setText(i[3])

    def back(self):
        self.windowUser = MainWindow(self.info)
        self.windowUser.show()
        self.close()


class Search(QMainWindow):
    def __init__(self, info):
        super().__init__()
        uic.loadUi('search.ui', self)
        self.setFixedSize(423, 487)
        self.search_btn.clicked.connect(self.search)
        self.back_btn.clicked.connect(self.back)
        self.connection = sqlite3.connect("project_db.sqlite")
        self.info = info

    def search(self):
        search_text = self.search_text.text()
        res = self.connection.cursor().execute("SELECT * FROM users").fetchall()
        for i in res:
            if i[1] == search_text:
                self.login_text.setText(i[1])
                self.password_text.setText('*' * len(i[2]))
                self.desc_text.setText(i[3])
        if self.login_text.text() == '':
            self.login_text.setText('не найдено')
            self.password_text.setText('не найдено')
            self.desc_text.setText('не найдено')

    def back(self):
        self.windowUser = MainWindow(self.info)
        self.windowUser.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())
