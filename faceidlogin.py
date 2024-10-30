import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime
import time

class CalendarClockApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calendar & Clock")
        self.geometry("400x500")
        self.configure(bg="#2c3e50")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 12))
        self.style.configure("TButton", background="#3498db", foreground="#ecf0f1", font=("Arial", 10), borderwidth=0)
        self.style.map("TButton", background=[("active", "#2980b9")])

        self.create_widgets()

    def create_widgets(self):
        # Clock Frame
        clock_frame = ttk.Frame(self, padding="10", style="TLabel")
        clock_frame.pack(pady=20)

        self.time_label = ttk.Label(clock_frame, font=("Arial", 36), style="TLabel")
        self.time_label.pack()

        self.date_label = ttk.Label(clock_frame, font=("Arial", 14), style="TLabel")
        self.date_label.pack()

        # Calendar Frame
        calendar_frame = ttk.Frame(self, padding="10", style="TLabel")
        calendar_frame.pack(pady=20, expand=True, fill="both")

        self.cal = calendar.Calendar(firstweekday=6)
        self.year = datetime.now().year
        self.month = datetime.now().month

        self.month_label = ttk.Label(calendar_frame, font=("Arial", 16, "bold"), style="TLabel")
        self.month_label.pack()

        self.cal_widget = ttk.Treeview(calendar_frame, columns=list(calendar.day_abbr), show='', height=7)
        self.cal_widget.pack(expand=True, fill="both")

        for i, day in enumerate(calendar.day_abbr):
            self.cal_widget.heading(i, text=day, anchor="center")
            self.cal_widget.column(i, anchor="center", width=50)

        # Navigation Frame
        nav_frame = ttk.Frame(self, style="TLabel")
        nav_frame.pack(pady=10)

        prev_button = ttk.Button(nav_frame, text="<", command=self.prev_month)
        prev_button.pack(side="left", padx=5)

        next_button = ttk.Button(nav_frame, text=">", command=self.next_month)
        next_button.pack(side="right", padx=5)

        self.update_calendar()
        self.update_clock()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%B %d, %Y")
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.after(1000, self.update_clock)

    def update_calendar(self):
        self.month_label.config(text=f"{calendar.month_name[self.month]} {self.year}")

        for item in self.cal_widget.get_children():
            self.cal_widget.delete(item)

        for week in self.cal.monthdayscalendar(self.year, self.month):
            week_with_empty = [day if day != 0 else "" for day in week]
            self.cal_widget.insert("", "end", values=week_with_empty)

        if self.month == datetime.now().month and self.year == datetime.now().year:
            today = datetime.now().day
            for item in self.cal_widget.get_children():
                values = self.cal_widget.item(item)["values"]
                if today in values:
                    index = values.index(today)
                    self.cal_widget.set(item, column=index, value=f">{today}<")

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.update_calendar()

if __name__ == "__main__":
    app = CalendarClockApp()
    app.mainloop()