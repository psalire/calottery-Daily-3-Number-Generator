import tkinter as tk

def create_gui_frame(gui, r, c, columnspan=1, rowspan=1):
    frame = tk.Frame(gui)
    frame.grid_columnconfigure((0, 1), weight=1)
    frame.grid_rowconfigure((0, 1), weight=1)
    frame.grid(row=r, column=c, sticky= 'N', columnspan=columnspan, rowspan=rowspan)
    return frame

def create_gui_scrollbar(frame, reference, row=1, column=1):
    scrollbar = tk.Scrollbar(frame)
    scrollbar.configure(command=reference.yview)
    scrollbar.grid(row=row, column=column, sticky='NS')
    reference.config(yscrollcommand=scrollbar.set)
    return scrollbar

def populate_days_listbox(month, days_listbox):
    if month in ['Jan','Mar','May','Jul','Aug','Oct','Dec']:
        total_days = range(1,32)
    elif month != 'Feb':
        total_days = range(1,31)
    else:
        total_days = range(1,30)
    days_listbox.delete(0, tk.END)
    for d in total_days:
        days_listbox.insert(tk.END, d)

def usemidday_to_string(u):
    if u.get() == True:
        return 'Midday'
    return 'Evening'

def update_month(event, m, d, y, u, date, days):
    w = event.widget
    m.set(w.get(w.curselection()))
    populate_days_listbox(m.get(), days)
    date.set('Using Draw: {} {}, {} ({})'.format(m.get(), d.get(), y.get(), usemidday_to_string(u)))

def update_day(event, m, d, y, u, date):
    w = event.widget
    d.set(w.get(w.curselection()))
    date.set('Using Draw: {} {}, {} ({})'.format(m.get(), d.get(), y.get(), usemidday_to_string(u)))

def update_year(event, m, d, y, u, date):
    w = event.widget
    y.set(w.get(w.curselection()))
    date.set('Using Draw: {} {}, {} ({})'.format(m.get(), d.get(), y.get(), usemidday_to_string(u)))

def update_tod(m, d, y, u, date):
    date.set('Using Draw: {} {}, {} ({})'.format(m.get(), d.get(), y.get(), usemidday_to_string(u)))
