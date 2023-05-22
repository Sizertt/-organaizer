import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from tkcalendar import Calendar



class ChooseDatetimeForm(tk.Toplevel):
    def __init__(self, app,
                 min_datetime=None,
                 cur_datetime=None,
                 max_datetime=None,
                 is_start=True):
        super().__init__()
        self.view = app
        self.min_datetime = min_datetime
        self.cur_datetime = cur_datetime
        self.max_datetime = max_datetime
        self.is_start = is_start
        self.init_form()

    def init_form(self):
        self.resizable(False, False)

        self.title(f'Дата и время {"начала" if self.is_start else "окончания"}')


        self.cal = Calendar(self, font="Arial 12", selectmode='day', locale='ru_RU',
                    mindate=self.min_datetime, maxdate=self.max_datetime,
                    year=self.cur_datetime.year, month=self.cur_datetime.month,
                    day=self.cur_datetime.day,
                    disabledforeground='red')
        self.cal.pack(fill="both")



        time_choose = ttk.Frame(self)
        time_choose.pack(pady = 5)


        self.hour_cb = ttk.Combobox(time_choose)

        self.hour_cb['values'] = list(range(24))

        self.hour_cb['state'] = 'readonly'

        self.hour_cb.pack(side='left', padx=4)

        self.minute_cb = ttk.Combobox(time_choose)

        self.minute_cb['values'] = [f"{t:02d}" for t in range(60)]

        self.minute_cb['state'] = 'readonly'

        self.minute_cb.pack()

        self.hour_cb.set(self.cur_datetime.hour)
        self.minute_cb.set(f"{self.cur_datetime.minute:02d}")

        self.grab_set()


        ttk.Button(self, text=f"Выбрать эту дату и время {'начала' if self.is_start else 'окончания'}",
                   command=self.choose_datetime).pack()


    def choose_datetime(self):
        try:
            day, month, year = map(int, self.cal.get_date().split("."))
            hour = int(self.hour_cb.get())
            minute = int(self.minute_cb.get())
        except:
            messagebox.showwarning(title="Выбор даты и времени", message="Не все параметры заданы")

        date_time = datetime(year, month, day, hour, minute)

        if self.is_start:
            self.view.update_start_datetime(date_time)
        else:
            self.view.update_end_datetime(date_time)


        self.destroy()
