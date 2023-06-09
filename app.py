from datetime import datetime, timedelta

import tkinter as tk
from tkinter import ttk, messagebox

from resources.scripts.DB import DB, STATUSES
from resources.scripts.Search import SearchForm
from resources.scripts.Login import LoginForm
from resources.scripts.ChooseDatetime import ChooseDatetimeForm

class Main(tk.Frame):
    def __init__(self, root, db: DB, user_id: int, username: str):
        super().__init__(root)
        self.root = root
        self.db = db
        self.user_id = user_id
        self.username = username
        self.columns = ('ID', 'start', 'end', 'description', 'type', 'priority', 'status')
        self.headers = ('ID', 'Начало', 'Окончание', 'Наименование', 'Тип', 'Приоритет', 'Статус')
        self.temp_controls = []
        self.init_main()
        self.view_records()



    def add_entry(self, text):

        for c in self.temp_controls:
            c.destroy()
        self.temp_controls = []

        d = datetime.now()
        i = self.db.insert_data(self.user_id, d, d, text, 1, 5)
        l = self.tree.get_children("")
        n = len(l)
        self.tree.delete(l[n-1])
        self.tree.insert('', 'end', values=self.make_readable((i, d, d, text, 1, 5, 0), self.db.get_data_types()))
        self.tree.insert('', 'end', values=("+", "", "", "", "", "", ""))
        self.tree.yview_moveto(1)


    def add_entry_text(self):

        l = self.tree.get_children("")
        n = len(l)
        y = 25 + 20 * (n - 1)
        y = min(y, 305)

        for c in self.temp_controls:
            c.destroy()
        self.temp_controls = []

        self.tree.yview_moveto(1)
        name_label = tk.Label(self.tree, text="Введите название и нажмите Enter:")
        name_label.place(x=105, y=y)
        name_entry = tk.Entry(self.tree, width=49)
        name_entry.place(x=309, y=y)
        self.temp_controls.extend((name_label, name_entry))
        name_entry.bind('<Return>', lambda e: self.add_entry(name_entry.get()))
        name_entry.focus()



    def do_popup(self, event):

        for c in self.temp_controls:
            c.destroy()
        self.temp_controls = []



        try:
            item = self.tree.identify_row(event.y)
            if not item or self.tree.set(item, '#1') == "+": return
            self.tree.focus(item)
            self.tree.selection_set(item)
            self.selection_set = self.tree.set(item)
            self.selection_item = item
            self.popup.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup.grab_release()

    def update_description(self, description):

        for c in self.temp_controls:
            c.destroy()
        self.temp_controls = []

        self.db.update_description(self.selection_set["ID"], description)
        self.tree.set(self.selection_item, "description", description)


    def update_type(self, type_):

        for c in self.temp_controls:
            c.destroy()
        self.temp_controls = []

        self.db.update_type_id(self.selection_set["ID"], type_[0])
        self.tree.set(self.selection_item, "type", type_[1])

    def update_priority(self, priority):

        for c in self.temp_controls:
            c.destroy()
        self.temp_controls = []

        self.db.update_priority(self.selection_set["ID"], priority)
        self.tree.set(self.selection_item, "priority", priority)

    def update_status(self, status_id):

        for c in self.temp_controls:
            c.destroy()
        self.temp_controls = []

        self.db.update_status(self.selection_set["ID"], status_id)
        self.tree.set(self.selection_item, "status", STATUSES[status_id])

    def init_main(self):

        #Create menu
        self.popup = tk.Menu(self, tearoff=0)
        types = self.db.get_data_types()[1:] # пропускаем первый пустой тип
        submenu = tk.Menu(self.popup)
        self.popup.add_cascade(label='Сменить тип', menu=submenu, underline=0)
        for type_ in types:
            submenu.add_command(label=type_[1], command=lambda type_=type_: self.update_type(type_))

        submenu = tk.Menu(self.popup)
        self.popup.add_cascade(label='Сменить приоритет', menu=submenu, underline=0)
        for i in range(1, 6):
            submenu.add_command(label=i, command=lambda i=i: self.update_priority(i))

        submenu = tk.Menu(self.popup)
        self.popup.add_cascade(label='Сменить статус', menu=submenu, underline=0)
        for i in range(len(STATUSES)):
            submenu.add_command(label=STATUSES[i], command=lambda i=i: self.update_status(i))

        self.popup.add_command(label="Удалить", command=self.delete_selected_record)


        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./resources/images/plus.png')
        btn_insert_dialog = tk.Button(toolbar, text='Добавить', command=self.add_entry_text, bg='#d7d8e0', bd=0, compound=tk.TOP, image=self.add_img)
        btn_insert_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./resources/images/minus.png')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#d7d8e0', bd=0, image=self.delete_img, compound=tk.TOP, command=self.delete_selected_record)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./resources/images/find.png')
        btn_search = tk.Button(toolbar, text="Поиск", bg='#d7d8e0', bd=0, image=self.search_img, compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='./resources/images/update.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg="#d7d8e0", bd=0, image=self.refresh_img, compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.exit_img = tk.PhotoImage(file='./resources/images/exit.png')
        btn_exit = tk.Button(toolbar, text='Выйти', bg="#d7d8e0", bd=0, image=self.exit_img, compound=tk.TOP, command=self.exit)
        btn_exit.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=self.columns, height=15, show='headings')
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('start', width=130, anchor=tk.CENTER)
        self.tree.column('end', width=130, anchor=tk.CENTER)
        self.tree.column('description', width=300, anchor=tk.CENTER)
        self.tree.column('type', width=120, anchor=tk.CENTER)
        self.tree.column('priority', width=100, anchor=tk.CENTER)
        self.tree.column('status', width=120, anchor=tk.W)

        vsb = tk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        vsb.place(relx=0.98, rely=0, relheight=1, relwidth=0.02)


        for i, col in enumerate(self.columns):
            self.tree.heading(col, text=self.headers[i], command=lambda num=i: \
                            self.treeview_sort_column(self.tree, num, False))

        self.tree.bind("<Button-3>", self.do_popup)

        def left_btn_handler(event):

            column = self.tree.identify_column(event.x)

            y = event.y

            if (y - 25) % 20 < 2:
                y += 1

            item = self.tree.identify_row(y)

            for c in self.temp_controls:
                c.destroy()
            self.temp_controls = []

            if not item or event.y <= 25: return

            self.selection_set = self.tree.set(item)
            self.selection_item = item

            if self.tree.set(item, '#1') == "+":
                self.add_entry_text()
                return

            if column == "#2":
                ChooseDatetimeForm(self,
                                   min_datetime=datetime(2020, 1, 1),
                                   cur_datetime=datetime.strptime(self.tree.set(item, '#2'), '%Y-%m-%d %H:%M'),
                                   max_datetime=datetime(2030, 12, 31))

            if column == "#3":
                ChooseDatetimeForm(self,
                                   min_datetime=datetime(2020, 1, 1),
                                   cur_datetime=datetime.strptime(self.tree.set(item, '#3'), '%Y-%m-%d %H:%M'),
                                   max_datetime=datetime(2030, 12, 31),
                                   is_start=False)

            if column == "#4":
                name_entry = tk.Entry(self.tree, width=49)
                name_entry.insert(0, self.tree.set(item, '#4'))
                name_entry.place(x=309, y=20 * ((event.y - 25) // 20) + 25)
                self.temp_controls.append(name_entry)
                name_entry.bind('<Return>', lambda e: self.update_description(name_entry.get()))
                name_entry.focus()

            if column == "#5":
                types = self.db.get_data_types()[1:] # не берем пустой
                combobox = ttk.Combobox(self.tree, justify='center', values=[t[1] for t in types], state='readonly', width=15)
                combobox.option_add('*TCombobox*Listbox.Justify', 'center')
                self.temp_controls.append(combobox)
                combobox.place(x=610, y=20 * ((event.y - 25) // 20) + 25)
                combobox.set(self.tree.set(item, '#5'))
                combobox.event_generate('<Button-1>')
                combobox.bind("<<ComboboxSelected>>", lambda e: self.update_type(types[combobox.current()]))

            if column == "#6":
                combobox = ttk.Combobox(self.tree, justify='center', values=list(range(1, 6)), state='readonly', width=13)
                combobox.option_add('*TCombobox*Listbox.Justify', 'center')
                self.temp_controls.append(combobox)
                combobox.place(x=731, y=20 * ((event.y - 25) // 20) + 25)
                combobox.set(self.tree.set(item, '#6'))
                combobox.event_generate('<Button-1>')
                combobox.bind("<<ComboboxSelected>>", lambda e: self.update_priority(combobox.current() + 1))

            if column == '#7':
                combobox = ttk.Combobox(self.tree, values=STATUSES, state='readonly', width=14)
                self.temp_controls.append(combobox)
                combobox.place(x=832, y=20 * ((event.y - 25) // 20) + 25)
                combobox.set(self.tree.set(item, '#7'))
                combobox.event_generate('<Button-1>')
                combobox.bind("<<ComboboxSelected>>", lambda e: self.update_status(combobox.current()))

        self.tree.bind("<Button-1>", left_btn_handler)

        self.tree.pack()


    def update_start_datetime(self, new_start: datetime):
        if not self.tree.selection():
            messagebox.showwarning(title="Установка даты и времени начала", message="Ничего не выбрано")
            return

        self.db.update_starts_at(self.selection_set["ID"], new_start)
        self.tree.set(self.selection_item, "start", new_start.strftime("%Y-%m-%d %H:%M"))

        end_datetime=datetime.strptime(self.tree.set(self.selection_item, '#3'), '%Y-%m-%d %H:%M')
        if end_datetime < new_start:
            self.db.update_ends_at(self.selection_set["ID"], new_start)
            self.tree.set(self.selection_item, "end", new_start.strftime("%Y-%m-%d %H:%M"))


    def update_end_datetime(self, new_end: datetime):
        if not self.tree.selection():
            messagebox.showwarning(title="Установка даты и времени окончания", message="Ничего не выбрано")
            return

        self.db.update_ends_at(self.selection_set["ID"], new_end)
        self.tree.set(self.selection_item, "end", new_end.strftime("%Y-%m-%d %H:%M"))

        start_datetime=datetime.strptime(self.tree.set(self.selection_item, '#2'), '%Y-%m-%d %H:%M')
        if start_datetime > new_end:
            self.db.update_starts_at(self.selection_set["ID"], new_end)
            self.tree.set(self.selection_item, "start", new_end.strftime("%Y-%m-%d %H:%M"))


    @staticmethod
    def make_readable(row, types):

        id = row[0]
        start = datetime.fromisoformat(row[1]) if type(row[1]) is str else row[1]
        start = start.strftime("%Y-%m-%d %H:%M")
        end = datetime.fromisoformat(row[2]) if type(row[2]) is str else row[2]
        end = end.strftime("%Y-%m-%d %H:%M")
        description = row[3]
        type_ = types[row[4] - 1][1]
        priority = row[5]
        status = STATUSES[row[6]]

        return (id, start, end, description, type_, priority, status)


    def show_records(self, rows):
        self.tree.delete(*self.tree.get_children())
        types = self.db.get_data_types()
        for row in rows:
            self.tree.insert('', 'end', values=self.make_readable(row, types))
        self.tree.insert('', 'end', values=("+", "", "", "", "", "", ""))


    def view_records(self):

        for i, colm in enumerate(self.columns):
            self.tree.heading(colm, text=self.headers[i]) # при обновлении теряется сортировка, поэтому убираем стрелочки из названий столбцов

        rows = self.db.fetch_all_data(self.user_id)
        self.show_records(rows)


    def delete_selected_record(self):
        if not self.tree.selection():
            messagebox.showwarning(title="Удаление", message="Ничего не выбрано")
            return

        for selection_item in self.tree.selection():
            self.db.remove_data(self.tree.set(selection_item, '#1'))
        self.view_records()


    def filter_data(self,
                    starts_from=None, starts_to=None,
                    ends_from=None, ends_to=None,
                    description=None, types_ids=None,
                    min_priority=None, statuses_ids=None):

        for i, colm in enumerate(self.columns):
            self.tree.heading(colm, text=self.headers[i])

        rows = self.db.filter_data(self.user_id,
                    starts_from, starts_to,
                    ends_from, ends_to,
                    description, types_ids,
                    min_priority, statuses_ids)
        self.show_records(rows)



    def open_search_dialog(self):

        types = db.get_data_types()[1:] # не берем пустой тип

        SearchForm(self, types, STATUSES)


    def treeview_sort_column(self, treeview: ttk.Treeview, num, reverse: bool):

        col = self.columns[num]

        l = treeview.get_children("")
        n = len(l)
        treeview.delete(l[n-1])
        l = l[:-1]

        try:
            data_list = [
                (int(treeview.set(k, col)), k) for k in l
            ]
        except Exception:
            data_list = [(treeview.set(k, col), k) for k in l]



        data_list.sort(reverse=reverse)

        for index, (val, k) in enumerate(data_list):
            treeview.move(k, "", index)

        for i, colm in enumerate(self.columns):
            treeview.heading(colm, text=self.headers[i])


        treeview.heading(
            column=col,
            text=f"⬇️{self.headers[num]}" if reverse else f"⬆️{self.headers[num]}",
            command=lambda _num=num: self.treeview_sort_column(
                treeview, _num, not reverse
            ),
        )

        treeview.insert('', 'end', values=("+", "", "", "", "", "", ""))


    def exit(self):
        self.root.destroy()
        self.db.unsave_user()
        login(self.db)




def showform(db, user):
    root = tk.Tk()
    app = Main(root, db, user[0], user[1])
    app.pack()
    root.title(f'Ежедневник пользователя {user[1]}')
    root.resizable(False, False)
    root.mainloop()


def login(db):
    login = LoginForm(db)

    login.root_log.mainloop()

    user = login.user_logined

    if user is not None:
        showform(db, user)


#Запуск с проверкой на существующего пользователя
if __name__ == "__main__":

    db = DB()

    user = db.get_saved_user()

    if not user:
        login(db)
    else:
        showform(db, user)
