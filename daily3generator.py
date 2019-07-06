import argparse
import itertools
import re
import requests
import sys
import tkinter as tk
from datetime import datetime, timedelta
from gui import *

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tothotnumbers', type=int, nargs=1, default=[4], help='Number of "hot numbers" to use in generating playable numbers. Max: 10 Default: 4')
    parser.add_argument('--includetriples', action='store_true', default=False, help='Include triples in playable numbers. Default: False')
    return parser.parse_args()

def fetch_daily3_file():
    print('Fetching...')
    page = requests.get('https://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=daily-3&Order=No')
    print('Fetched.')
    content = str(page.content).replace(r'\r', '\r').replace(r'\n', '\n')
    with open('daily3results.txt', 'wb') as out_file:
        # Write file with fixed line endings
        out_file.write(content.encode())
    return content

def open_daily3_file():
    content = open('daily3results.txt', 'r').read()
    return content

def get_line_num_by_date(date_to_use, lines, lookback_size, use_midday_draw, latest_draw_date):
    date_line_num = 0
    if date_to_use == None:
        date_to_use = latest_draw_date
    elif date_to_use != latest_draw_date:
        diff = latest_draw_date - date_to_use
        if diff.days < 0:
            print('Error: Date ({}) is in the future.'.format(date_to_use.strftime('%b %d, %Y')))
            return 'Error: Date ({}) is in the future.'.format(date_to_use.strftime('%b %d, %Y')), None
        date_line_num = diff.days * 2
    if date_line_num + lookback_size > len(lines):
        print('Error: Date ({}) + lookback_size ({}) is out of range.'.format(date_to_use.strftime('%b %d, %Y'), lookback_size))
        return 'Error: Date ({}) + lookback_size ({}) is out of range.'.format(date_to_use.strftime('%b %d, %Y'), lookback_size), None
    if use_midday_draw == True and lines[date_line_num][15:27] == lines[date_line_num+1][15:27]:
        date_line_num += 1
    elif use_midday_draw == False and date_line_num != 0 and lines[date_line_num][15:27] == lines[date_line_num-1][15:27]:
        date_line_num -= 1
    return date_to_use, date_line_num

def get_hot_numbers(lines, tot_hotnumbers):
    # Initialize histogram
    histogram = {}
    for i in range(10):
        histogram[str(i)] = 0
    # Count frequencies
    for line in lines:
        numbers = re.findall(r'\d+', line)[3:]
        for number in numbers:
            histogram[number] += 1
    frequency_histogram = 'Frequency Histogram:\n'
    for num in histogram:
        frequency_histogram += '{}: {}\n'.format(num, histogram[num])
    frequency_histogram += '\n'
    return sorted(histogram, key=histogram.get)[:tot_hotnumbers], frequency_histogram

def print_playable_sets(hot_numbers, include_triples, output_msg):
    output = 'Numbers to play ({}):\n'.format(','.join(hot_numbers))
    i = 1
    if include_triples == False:
        # Print all combinations
        for set in itertools.combinations_with_replacement(hot_numbers, 3):
            if all(x == set[0] for x in set) == False:
                output += '{:>2}. {}\n'.format(i, ''.join(set))
                i += 1
    else:
        # Print all combinations
        for set in itertools.combinations_with_replacement(hot_numbers, 3):
            output += '{:>2}. {}'.format(i, ''.join(set))
            i += 1
    print(output)
    output_msg.set(output)

def daily3(args, m, d, y, use_midday_draw, lookback_size, output_msgs):
    date_to_use = '{} {}, {}'.format(m, d, y)
    try:
        date_to_use = datetime.strptime(date_to_use, '%b %d, %Y')
    except ValueError:
        print('Error: Invalid date')
        output_msgs[0].set('Error: Invalid date')
        return
    tot_hotnumbers = args.tothotnumbers[0]
    if tot_hotnumbers > 10:
        print('Error: must be 0 < tot_hotnumbers <= 10')
        output_msgs[0].set('Error: must be 0 < tot_hotnumbers <= 10')
        return
    include_triples = args.includetriples

    # Get txt file
    lotto_file = open_daily3_file()
    lines = lotto_file.split('\n')[5:]

    # Get latest draw date
    latest_draw_date = datetime.strptime(lines[0][15:27], '%b %d, %Y')
    print('')

    # Get line number by date
    date_to_use, date_line_num = get_line_num_by_date(date_to_use, lines, lookback_size, use_midday_draw, latest_draw_date)
    if date_line_num == None:
        output_msgs[0].set(date_to_use)
        output_msgs[1].set('')
        return

    output = '{:<17}: '.format('Lookback-size') + str(lookback_size) + '\n'
    output += '{:<17}: '.format('Include Triples') + str(include_triples) + '\n'
    output += '{:<17}: {}'.format('Using Midday Draw', use_midday_draw) + '\n\n'
    output += '{:<17}: {} (Draw #{})'.format('Using Date', date_to_use.strftime('%b %d, %Y'), int(lines[date_line_num][:5])) + '\n'
    hot_numbers, frequency_histogram = get_hot_numbers(
        lines[date_line_num:date_line_num+lookback_size],
        tot_hotnumbers
    )
    output += frequency_histogram
    output_msgs[0].set(output)
    print_playable_sets(hot_numbers, include_triples, output_msgs[1])

###################### MAIN ######################
def main():
    # Get args
    args = get_args()
    # Fetch latest draw file
    lotto_file = fetch_daily3_file().split('\n')[5:]
    # Create GUI
    gui = tk.Tk()
    ## Configure grids
    gui.grid_columnconfigure((0,1,2,3), weight=1)
    gui.grid_rowconfigure((0,1,2,3,4), weight=1)
    gui.title('CA Daily 3 Generator')
    ## Argument vars
    month = tk.StringVar()
    day = tk.StringVar()
    year = tk.StringVar()
    output_msg_col1 = tk.StringVar()
    output_msg_col2 = tk.StringVar()
    use_midday = tk.BooleanVar()
    lookback_size = tk.IntVar()
    ## Initialize argument vars
    month.set(datetime.today().strftime('%b'))
    day.set(datetime.today().strftime('%d'))
    year.set(datetime.today().strftime('%Y'))
    use_midday.set(False)
    lookback_size.set(10)
    ### Create frames
    month_frame = create_gui_frame(gui, 0, 0)
    day_frame = create_gui_frame(gui, 0, 1)
    year_frame = create_gui_frame(gui, 0, 2)
    msg_frame = create_gui_frame(gui, 0, 3)
    tod_frame = create_gui_frame(gui, 2, 0, columnspan=3)
    lb_frame = create_gui_frame(gui, 3, 0, columnspan=3)
    ### Listboxes for date selection
    months = tk.Listbox(month_frame, width=5)
    days = tk.Listbox(day_frame, width=5)
    years = tk.Listbox(year_frame, width=5)
    ### Fill Month listbox
    for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        months.insert(tk.END, m)
    tk.Label(month_frame, text='Month: ', font='Arial 10 bold').grid(row=0, column=0, sticky='W')
    months.grid(row=1, column=0)
    create_gui_scrollbar(month_frame, months)
    ### Fill Day listbox
    populate_days_listbox(datetime.today().strftime('%b'), days)
    tk.Label(day_frame, text='Day: ', font='Arial 10 bold').grid(row=0, column=0, sticky='W')
    days.grid(row=1, column=0)
    create_gui_scrollbar(day_frame, days)
    ### Fill Year listbox
    for y in range(1992, int(year.get())+1):
        years.insert(0, y)
    tk.Label(year_frame, text='Year: ', font='Arial 10 bold').grid(row=0, column=0, sticky='W')
    years.grid(row=1, column=0)
    create_gui_scrollbar(year_frame, years)
    ### Radio buttons for time of day selection
    tk.Label(tod_frame, text='Draw Time:').grid(row=0, column=0)
    tk.Radiobutton(tod_frame, text='Evening', variable=use_midday,
        value=False, command=lambda: update_tod(month, day, year, use_midday, date)).grid(row=0, column=1)
    tk.Radiobutton(tod_frame, text='Midday', variable=use_midday,
        value=True, command=lambda: update_tod(month, day, year, use_midday, date)).grid(row=0, column=2)
    ### Spinbox for lookback size
    tk.Label(lb_frame, text='Lookback Size:').grid(row=0, column=0)
    tk.Spinbox(lb_frame, from_=1, to_=len(lotto_file), textvariable=lookback_size, width=10).grid(row=0, column=1)
    ## Display selected date
    date = tk.StringVar()
    date.set('Using Draw: {} {}, {} ({})'.format(month.get(), day.get(), year.get(), usemidday_to_string(use_midday)))
    tk.Label(gui, textvariable=date, font='Arial 11 bold', width=30).grid(row=4, columnspan=3)
    months.bind('<ButtonRelease-1>', lambda e: update_month(e, month, day, year, use_midday, date, days))
    days.bind('<ButtonRelease-1>', lambda e: update_day(e, month, day, year, use_midday, date))
    years.bind('<ButtonRelease-1>', lambda e: update_year(e, month, day, year, use_midday, date))
    ## Output message box
    tk.Label(msg_frame, text='Result:', font='Arial 10 bold').grid(row=0, column=0, sticky='W', columnspan=2)
    tk.Message(msg_frame, textvariable=output_msg_col1).grid(row=1, column=0)
    tk.Message(msg_frame, textvariable=output_msg_col2).grid(row=1, column=1)
    ## Start button
    start_button = tk.Button(
        gui, text='Start', command=lambda:daily3(
            args, month.get(), day.get(), year.get(), use_midday.get(),
            lookback_size.get(), [output_msg_col1, output_msg_col2]
        )
    )
    start_button.grid(row=5, columnspan=3)
    gui.mainloop()

if __name__ == "__main__":
    main()
