from datetime import datetime
from calendar import monthrange
import tkinter as tk
from tkinter import ttk, messagebox


class SearchForm(tk.Toplevel):

    def __init__(self, app, types, statuses):
        super().__init__()
        self.view = app
        self.months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля",
                  "августа", "сентября", "октября", "ноября", "декабря"]
        self.types = types
        self.types_vars = [tk.IntVar(value=0) for _ in range(len(types))]
        self.statuses = statuses
        self.statuses_vars = [tk.IntVar(value=0) for _ in range(len(statuses))]
        self.init_search_form()


    def init_search_form(self):




        self.title('Поиск')
        self.resizable(False, False)

        start_header_frame = ttk.Frame(self)
        start_header_frame.pack(padx=8, pady = (15, 3), anchor="w")

        tk.Label(start_header_frame, text='Дата начала', font = ('Helvetica', 10, 'bold')).pack(side="left")

        ttk.Button(start_header_frame, text="Очистить", command=self.clear_start_date).pack(side="left")

        tk.Label(start_header_frame, text=':', font = ('Helvetica', 10, 'bold')).pack(side="left")


        labels_start_date = ttk.Frame(self)
        labels_start_date.pack(padx=0, pady = 3, anchor="w")

        label_start_date_from = tk.Label(labels_start_date, text='От:', font = ('Helvetica', 10, 'italic'))
        label_start_date_from.pack(side='left', padx=(80, 230))

        label_start_date_to = tk.Label(labels_start_date, text='До:', font = ('Helvetica', 10, 'italic'))
        label_start_date_to.pack()

        start_date_choose = ttk.Frame(self)
        start_date_choose.pack(pady = 3)


        self.start_day_from_cb = ttk.Combobox(start_date_choose, width=4)

        self.start_day_from_cb['values'] = list(range(1, 32))

        self.start_day_from_cb['state'] = 'readonly'

        self.start_day_from_cb.pack(side='left', padx=8)

        self.start_month_from_cb = ttk.Combobox(start_date_choose, width=12)

        self.start_month_from_cb['values'] = self.months

        self.start_month_from_cb['state'] = 'readonly'

        self.start_month_from_cb.bind("<<ComboboxSelected>>",
                                      lambda _: self.set_days_count(
                                          self.start_day_from_cb,
                                          self.start_month_from_cb,
                                          self.start_year_from_cb))

        self.start_month_from_cb.pack(side='left', padx=(0, 4))

        self.start_year_from_cb = ttk.Combobox(start_date_choose, width=6)

        self.start_year_from_cb['values'] = list(range(2020, 2031))

        self.start_year_from_cb['state'] = 'readonly'

        self.start_year_from_cb.bind("<<ComboboxSelected>>",
                                     lambda _: self.set_days_count(
                                         self.start_day_from_cb,
                                         self.start_month_from_cb,
                                         self.start_year_from_cb))

        self.start_year_from_cb.pack(side='left', padx=(0, 30))


        self.start_day_to_cb = ttk.Combobox(start_date_choose, width=4)

        self.start_day_to_cb['values'] = list(range(1, 32))

        self.start_day_to_cb['state'] = 'readonly'

        self.start_day_to_cb.pack(side='left', padx=8)

        self.start_month_to_cb = ttk.Combobox(start_date_choose, width=12)

        self.start_month_to_cb['values'] = self.months

        self.start_month_to_cb['state'] = 'readonly'

        self.start_month_to_cb.bind("<<ComboboxSelected>>",
                                    lambda _: self.set_days_count(
                                        self.start_day_to_cb,
                                        self.start_month_to_cb,
                                        self.start_year_to_cb))

        self.start_month_to_cb.pack(side='left', padx=(0, 4))

        self.start_year_to_cb = ttk.Combobox(start_date_choose, width=6)

        self.start_year_to_cb['values'] = list(range(2020, 2031))

        self.start_year_to_cb['state'] = 'readonly'

        self.start_year_to_cb.bind("<<ComboboxSelected>>",
                                   lambda _: self.set_days_count(
                                       self.start_day_to_cb,
                                       self.start_month_to_cb,
                                       self.start_year_to_cb))

        self.start_year_to_cb.pack(side='left', padx=(0, 10))

        ttk.Button(start_date_choose, command=self.repeat_start, text="Искать одну дату").pack(padx=(3, 12))


        end_header_frame = ttk.Frame(self)
        end_header_frame.pack(padx=8, pady = (15, 3), anchor="w")

        tk.Label(end_header_frame, text='Дата окончания', font = ('Helvetica', 10, 'bold')).pack(side="left")

        ttk.Button(end_header_frame, text="Очистить", command=self.clear_end_date).pack(side="left")

        tk.Label(end_header_frame, text=':', font = ('Helvetica', 10, 'bold')).pack(side="left")

        labels_end_date = ttk.Frame(self)
        labels_end_date.pack(padx=0, pady = 3, anchor="w")

        label_end_date_from = tk.Label(labels_end_date, text='От:', font = ('Helvetica', 10, 'italic'))
        label_end_date_from.pack(side='left', padx=(80, 230))

        label_end_date_to = tk.Label(labels_end_date, text='До:', font = ('Helvetica', 10, 'italic'))
        label_end_date_to.pack()

        end_date_choose = ttk.Frame(self)
        end_date_choose.pack(pady = (6, 8))


        self.end_day_from_cb = ttk.Combobox(end_date_choose, width=4)

        self.end_day_from_cb['values'] = list(range(1, 32))

        self.end_day_from_cb['state'] = 'readonly'

        self.end_day_from_cb.pack(side='left', padx=8)

        self.end_month_from_cb = ttk.Combobox(end_date_choose, width=12)

        self.end_month_from_cb['values'] = self.months

        self.end_month_from_cb['state'] = 'readonly'

        self.end_month_from_cb.bind("<<ComboboxSelected>>",
                                    lambda _: self.set_days_count(
                                        self.end_day_from_cb,
                                        self.end_month_from_cb,
                                        self.end_year_from_cb))

        self.end_month_from_cb.pack(side='left', padx=(0, 4))

        self.end_year_from_cb = ttk.Combobox(end_date_choose, width=6)

        self.end_year_from_cb['values'] = list(range(2020, 2031))

        self.end_year_from_cb['state'] = 'readonly'

        self.end_year_from_cb.bind("<<ComboboxSelected>>",
                                   lambda _: self.set_days_count(
                                       self.end_day_from_cb,
                                       self.end_month_from_cb,
                                       self.end_year_from_cb))

        self.end_year_from_cb.pack(side='left', padx=(0, 30))



        self.end_day_to_cb = ttk.Combobox(end_date_choose, width=4)

        self.end_day_to_cb['values'] = list(range(1, 32))

        self.end_day_to_cb['state'] = 'readonly'

        self.end_day_to_cb.pack(side='left', padx=8)

        self.end_month_to_cb = ttk.Combobox(end_date_choose, width=12)

        self.end_month_to_cb['values'] = self.months

        self.end_month_to_cb['state'] = 'readonly'

        self.end_month_to_cb.bind("<<ComboboxSelected>>",
                                  lambda _: self.set_days_count(
                                      self.end_day_to_cb,
                                      self.end_month_to_cb,
                                      self.end_year_to_cb))

        self.end_month_to_cb.pack(side='left', padx=(0, 4))

        self.end_year_to_cb = ttk.Combobox(end_date_choose, width=6)

        self.end_year_to_cb['values'] = list(range(2020, 2031))

        self.end_year_to_cb['state'] = 'readonly'

        self.end_year_to_cb.bind("<<ComboboxSelected>>",
                                 lambda _: self.set_days_count(
                                     self.end_day_to_cb,
                                     self.end_month_to_cb,
                                     self.end_year_to_cb))

        self.end_year_to_cb.pack(side="left", padx=(0, 10))

        ttk.Button(end_date_choose, command=self.repeat_end, text="Искать одну дату").pack(padx=(3, 12))

        description_header_frame = ttk.Frame(self)
        description_header_frame.pack(padx=8, pady = (15, 3), anchor="w")

        tk.Label(description_header_frame, text='Наименование', font = ('Helvetica', 10, 'bold')).pack(side="left")

        ttk.Button(description_header_frame, text="Очистить",
                   command=lambda: self.description_entry.delete(0, 'end')).pack(side="left")

        tk.Label(description_header_frame, text=':', font = ('Helvetica', 10, 'bold')).pack(side="left")

        description_frame = ttk.Frame(self)
        description_frame.pack(padx=10, pady = (6, 8), anchor="w")

        self.description_entry = ttk.Entry(description_frame, width=49)
        self.description_entry.pack()

        types_header_frame = ttk.Frame(self)
        types_header_frame.pack(padx=8, pady = (15, 3), anchor="w")

        tk.Label(types_header_frame, text='Типы', font = ('Helvetica', 10, 'bold')).pack(side="left")

        ttk.Button(types_header_frame, text="Выбрать все",
                   command=lambda: self.make_all(self.types_vars)).pack(side="left")

        ttk.Button(types_header_frame, text="Снять выбор",
                   command=lambda: self.make_all(self.types_vars, False)).pack(side="left")

        tk.Label(types_header_frame, text=':', font = ('Helvetica', 10, 'bold')).pack(side="left")

        types_frame = ttk.Frame(self)
        types_frame.pack(padx=10, pady = (6, 8), anchor="w")

        for i, t in enumerate(self.types):
            cb = tk.Checkbutton(types_frame, text=t[1], variable=self.types_vars[i])
            cb.pack(side="left", padx=3)


        prior_header_frame = ttk.Frame(self)
        prior_header_frame.pack(padx=8, pady = (15, 3), anchor="w")

        tk.Label(prior_header_frame, text='Приоритет не ниже:', font = ('Helvetica', 10, 'bold')).pack(side="left")

        prior_frame = ttk.Frame(self)
        prior_frame.pack(padx=12, pady = (6, 8), anchor="w")

        self.min_priority_cb = ttk.Combobox(prior_frame, width=12)

        self.min_priority_cb['values'] = list(range(1, 6))

        self.min_priority_cb['state'] = 'readonly'

        self.min_priority_cb.pack()


        statuses_header_frame = ttk.Frame(self)
        statuses_header_frame.pack(padx=8, pady = (15, 3), anchor="w")

        tk.Label(statuses_header_frame, text='Статусы', font = ('Helvetica', 10, 'bold')).pack(side="left")

        ttk.Button(statuses_header_frame, text="Выбрать все",
                   command=lambda: self.make_all(self.statuses_vars)).pack(side="left")

        ttk.Button(statuses_header_frame, text="Снять выбор",
                   command=lambda: self.make_all(self.statuses_vars, False)).pack(side="left")

        tk.Label(statuses_header_frame, text=':', font = ('Helvetica', 10, 'bold')).pack(side="left")

        statuses_frame = ttk.Frame(self)
        statuses_frame.pack(padx=10, pady = (6, 8), anchor="w")

        for i, st in enumerate(self.statuses):
            cb = tk.Checkbutton(statuses_frame, text=st, variable=self.statuses_vars[i])
            cb.pack(side="left", padx=3)






        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.pack(pady=(40,5))


        btn_search = ttk.Button(self, text='Поиск', command=self.build_and_run_query)
        btn_search.pack(pady=5)


        self.grab_set()


    def set_days_count(self, days_cb, month_cb, year_cb):
        month = month_cb.get()
        if not month:
            return
        month = self.months.index(month) + 1
        year = year_cb.get()
        if not year:
            year = datetime.now().year
        else:
            year = int(year)
        days_count = monthrange(year, month)[1]
        day = days_cb.get()
        if not day or int(day) < days_count:
            days_cb['values'] = list(range(1, days_count + 1))
        else:
            days_cb['values'] = list(range(1, days_count + 1))
            days_cb.set(days_count)


    def get_bound_datetime(self, day_cb, month_cb, year_cb, is_from=True):

        day = day_cb.get()
        month = month_cb.get()
        year = year_cb.get()

        if day and not (month and year):
            raise Exception("Задан день, но не заданы месяц и/или год")
        if month and not year:
            raise Exception("Задан месяц, но не задан год")

        if not year:
            return None

        year = int(year)
        month = self.months.index(month) + 1 if month else (1 if is_from else 12)
        day = int(day) if day else (1 if is_from else monthrange(year, month)[1])

        return datetime(year, month, day)


    def build_and_run_query(self):

        start_date_from = start_date_to = end_date_from = end_date_to = None

        try:

            start_date_from = self.get_bound_datetime(
                self.start_day_from_cb, self.start_month_from_cb, self.start_year_from_cb)

            start_date_to = self.get_bound_datetime(
                self.start_day_to_cb, self.start_month_to_cb, self.start_year_to_cb, is_from=False)

            end_date_from = self.get_bound_datetime(
                self.end_day_from_cb, self.end_month_from_cb, self.end_year_from_cb)

            end_date_to = self.get_bound_datetime(
                self.end_day_to_cb, self.end_month_to_cb, self.end_year_to_cb, is_from=False)

        except Exception as e:

            messagebox.showwarning("Поиск", str(e))
            return

        if start_date_from and start_date_to and start_date_from > start_date_to:
            messagebox.showwarning("Поиск", "Для даты начала 'от' больше чем 'до'")
            return

        if end_date_from and end_date_to and end_date_from > end_date_to:
            messagebox.showwarning("Поиск", "Для даты окончания 'от' больше чем 'до'")
            return

        if start_date_from and end_date_to and start_date_from > end_date_to:
            messagebox.showwarning("Поиск", "Для даты начала 'от' больше чем 'от' для даты окончания")
            return

        descr = self.description_entry.get().strip()

        min_prior = self.min_priority_cb.get()
        if min_prior:
            min_prior = int(min_prior)

        types_ids = []
        for i, t in enumerate(self.types_vars):
            if t.get():
                types_ids.append(self.types[i][0])


        statuses_ids = []
        for i, st in enumerate(self.statuses_vars):
            if st.get():
                statuses_ids.append(i)

        self.view.filter_data(start_date_from, start_date_to,
                              end_date_from, end_date_to,
                              descr, types_ids,
                              min_prior, statuses_ids)



    def make_all(self, boxes_vars, value=True):
        for v in boxes_vars:
            v.set(value)


    def clear_start_date(self):
        self.start_day_from_cb.set('')
        self.start_month_from_cb.set('')
        self.start_year_from_cb.set('')
        self.start_day_to_cb.set('')
        self.start_month_to_cb.set('')
        self.start_year_to_cb.set('')


    def clear_end_date(self):
        self.end_day_from_cb.set('')
        self.end_month_from_cb.set('')
        self.end_year_from_cb.set('')
        self.end_day_to_cb.set('')
        self.end_month_to_cb.set('')
        self.end_year_to_cb.set('')

    def repeat_start(self):
        self.start_day_to_cb.set(self.start_day_from_cb.get())
        self.start_month_to_cb.set(self.start_month_from_cb.get())
        self.start_year_to_cb.set(self.start_year_from_cb.get())

    def repeat_end(self):
        self.end_day_to_cb.set(self.end_day_from_cb.get())
        self.end_month_to_cb.set(self.end_month_from_cb.get())
        self.end_year_to_cb.set(self.end_year_from_cb.get())