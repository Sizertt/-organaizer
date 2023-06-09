from tkinter import *
import pickle
from tkinter import messagebox
from difflib import SequenceMatcher

from resources.scripts.DB import DB

class LoginForm():


    def __init__(self, db: DB):
        self.root_log = Tk()
        self.root_log.geometry("300x500")
        self.root_log.title("Войти в систему")
        self.db = db
        self.user_logined = None
        self.show()


    def show(self):
        checked = BooleanVar()
        text_enter_login = Label(self.root_log, text="Введите Ваш логин:")
        enter_login = Entry(self.root_log)
        text_enter_pass = Label(self.root_log, text="Введите Ваш пароль:")
        enter_password = Entry(self.root_log, show="*")
        button_enter = Button(self.root_log, text="Войти", command=lambda: log_pass())
        remember_checkbutton = Checkbutton(self.root_log, text="Запомнить меня на этом устройстве", variable=checked)
        button_reg = Button(self.root_log, text="Зарегестрироваться", command=lambda: register())
        text_enter_login.pack()
        enter_login.pack()
        text_enter_pass.pack()
        enter_password.pack()
        remember_checkbutton.pack()
        button_enter.pack()
        button_reg.pack()

        def log_pass():

            password = enter_password.get()

            username = enter_login.get().strip()

            if not username:
                messagebox.showerror("Ошибка", "Введите имя пользователя (не из одних пробелов)")
                return

            if not password:
                messagebox.showerror("Ошибка", "Введите пароль (не из одних пробелов)")
                return

            user_id = self.db.get_user_id(username)

            if not user_id or not self.db.username_match_password(username, password):
                messagebox.showerror("Ошибка", "Неверное имя или пароль")
                return

            self.user_logined = (user_id, username)

            if checked.get():
                self.db.save_user(user_id)
            else:
                self.db.unsave_user()

            self.root_log.destroy()


        def register():

            password = enter_password.get()

            username = enter_login.get().strip()

            if not username:
                messagebox.showerror("Ошибка", "Введите имя пользователя (не из одних пробелов)")
                return

            if not password:
                messagebox.showerror("Ошибка", "Введите пароль (не из одних пробелов)")
                return

            if self.db.get_user_id(username):
                messagebox.showerror("Ошибка", f"Имя {username} уже занято, выберите другое")
                return
            
            if len(username) < 4 or len(password) < 4:
                messagebox.showerror("Ошибка", "Логин и пароль должны содержать не менее 4 символов")
                return
            
            similarity = SequenceMatcher(None, username, password).ratio()
            if similarity > 0.8:
                messagebox.showerror("Ошибка", "Пароль не должен быть похожим на логин")
                return

            user_id = self.db.register_user(username, password)

            self.user_logined = (user_id, username)

            if checked.get():
                self.db.save_user(user_id)
            else:
                self.db.unsave_user()


            self.root_log.destroy()
