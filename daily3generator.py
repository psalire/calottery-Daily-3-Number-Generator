import argparse
import itertools
import re
import requests
import sys
import tkinter as tk
from datetime import datetime, timedelta

LATEST_DRAW_DATE = None

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lookback', type=int, nargs=1, default=[10], help='Number of previous draws to calculate from. Default: 10')
    parser.add_argument('--tothotnumbers', type=int, nargs=1, default=[4], help='Number of "hot numbers" to use in generating playable numbers. Max: 10 Default: 4')
    parser.add_argument('--usedate', type=str, nargs=1, default=[None], help='Date to lookback from in format "%%b %%d, %%Y". Default: today\'s date')
    parser.add_argument('--middaydraw', action='store_true', default=False, help='Use midday draw. Default: False')
    parser.add_argument('--includetriples', action='store_true', default=False, help='Include triples in playable numbers. Default: False')
    parser.add_argument('--showhistogram', action='store_true', default=False, help='Print the frequency histogram. Default: False')
    parser.add_argument('--savefile', action='store_true', default=False, help='Save the calottery .txt file as daily3results.txt. Default: False')
    parser.add_argument('--uselocal', action='store_true', default=False, help='Use local daily3results.txt file from --savefile, instead of fetch. Default: False')
    return parser.parse_args()

def get_daily3_file(save_file, use_local):
    if use_local == False:
        print('Fetching...')
        page = requests.get('https://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=daily-3&Order=No')
        print('\033[A\033[K', end='')
        # Fix line endings
        content = str(page.content).replace(r'\r', '\r').replace(r'\n', '\n')
    else:
        content = open('daily3results.txt', 'r').read()
    if save_file == True:
        out_file = open('daily3results.txt', 'wb')
        out_file.write(content.encode())
        out_file.close()
    return content

def get_line_num_by_date(date_to_use, lines, lookback_size, use_midday_draw):
    date_line_num = 0
    if date_to_use == None:
        date_to_use = LATEST_DRAW_DATE
    elif date_to_use != LATEST_DRAW_DATE:
        diff = LATEST_DRAW_DATE - date_to_use
        if diff.days < 0:
            print('Error: Date ({}) is in the future. Exiting...'.format(date_to_use.strftime('%b %d, %Y')))
            sys.exit()
        date_line_num = diff.days * 2
    if date_line_num + lookback_size > len(lines):
        print('Error: Date ({}) + lookback_size ({}) is out of range. Exiting...'.format(date_to_use.strftime('%b %d, %Y'), lookback_size))
        sys.exit()
    if use_midday_draw == True and lines[date_line_num][15:27] == lines[date_line_num+1][15:27]:
        date_line_num += 1
    elif use_midday_draw == False and date_line_num != 0 and lines[date_line_num][15:27] == lines[date_line_num-1][15:27]:
        date_line_num -= 1
    return date_to_use, date_line_num

def get_hot_numbers(lines, tot_hotnumbers, print_histogram):
    # Initialize histogram
    histogram = {}
    for i in range(10):
        histogram[str(i)] = 0
    # Count frequencies
    for line in lines:
        numbers = re.findall(r'\d+', line)[3:]
        for number in numbers:
            histogram[number] += 1
    if print_histogram == True:
        print('Frequency Histogram:')
        for num in histogram:
            print('{}: {}'.format(num, histogram[num]))
        print('')
    return sorted(histogram, key=histogram.get)[:tot_hotnumbers]

def print_playable_sets(hot_numbers, include_triples):
    print('Numbers to play ({}):'.format(','.join(hot_numbers)))
    i = 1
    if include_triples == False:
        # Print all combinations
        for set in itertools.combinations_with_replacement(hot_numbers, 3):
            if all(x == set[0] for x in set) == False:
                print('{:>2}. {}'.format(i, ''.join(set)))
                i += 1
    else:
        # Print all combinations
        for set in itertools.combinations_with_replacement(hot_numbers, 3):
            print('{:>2}. {}'.format(i, ''.join(set)))
            i += 1

def daily3(args):
    date_to_use = args.usedate[0]
    if date_to_use != None:
        try:
            date_to_use = datetime.strptime(date_to_use, '%b %d, %Y')
        except ValueError:
            print('Error: Date must be format "%b %d, %Y"')
            sys.exit()
    lookback_size = args.lookback[0]
    tot_hotnumbers = args.tothotnumbers[0]
    if tot_hotnumbers > 10:
        print('Error: must be 0 < tot_hotnumbers <= 10')
        sys.exit()
    use_local = args.uselocal
    show_histogram = args.showhistogram
    use_midday_draw = args.middaydraw
    include_triples = args.includetriples
    save_file = args.savefile

    # Get txt file
    lotto_file = get_daily3_file(save_file, use_local)
    lines = lotto_file.split('\n')[5:]

    # Get latest draw date
    global LATEST_DRAW_DATE
    LATEST_DRAW_DATE = datetime.strptime(lines[0][15:27], '%b %d, %Y')
    print('')

    # Get line number by date
    date_to_use, date_line_num = get_line_num_by_date(date_to_use, lines, lookback_size, use_midday_draw)

    print('{:<17}: '.format('Lookback-size') + str(lookback_size))
    print('{:<17}: '.format('Include Triples') + str(include_triples))
    print('{:<17}: {}'.format('Using Midday Draw', use_midday_draw))
    print('{:<17}: {} (Draw #{})'.format('Using Date', date_to_use.strftime('%b %d, %Y'), int(lines[date_line_num][:5])))
    print('')
    hot_numbers = get_hot_numbers(
        lines[date_line_num:date_line_num+lookback_size],
        tot_hotnumbers,
        show_histogram
    )
    print_playable_sets(hot_numbers, include_triples)


########### MAIN ###########
def main():
    # Get args
    args = get_args()
    # date_to_use = args.usedate[0]
    # if date_to_use != None:
        # try:
            # date_to_use = datetime.strptime(date_to_use, '%b %d, %Y')
        # except ValueError:
            # print('Error: Date must be format "%b %d, %Y"')
            # sys.exit()
    # lookback_size = args.lookback[0]
    # tot_hotnumbers = args.tothotnumbers[0]
    # if tot_hotnumbers > 10:
        # print('Error: must be 0 < tot_hotnumbers <= 10')
        # sys.exit()
    # use_local = args.uselocal
    # show_histogram = args.showhistogram
    # use_midday_draw = args.middaydraw
    # include_triples = args.includetriples
    # save_file = args.savefile

    # Start GUI
    gui = tk.Tk()
    gui.grid_columnconfigure((0, 1, 2), weight=1)
    gui.title('CA Daily 3 Generator')
    ## Date to use
    month_frame = tk.Frame(gui)
    month_frame.grid_columnconfigure((0, 1), weight=1)
    month_frame.grid(row=0, column=0)
    month = tk.StringVar()
    month.set(datetime.today().strftime('%b'))
    months = tk.Listbox(month_frame)
    for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        months.insert(tk.END, m)
    months_scroll = tk.Scrollbar(month_frame)
    months_scroll.configure(command=months.yview, orient=tk.VERTICAL)
    months.grid(row=0, column=0)
    months_scroll.grid(row=0, column=1, sticky='NS')

    day_frame = tk.Frame(gui)
    day_frame.grid_columnconfigure((0, 1), weight=1)
    day_frame.grid(row=0, column=1)
    day = tk.StringVar()
    day.set(datetime.today().strftime('%d'))
    numerical_month  = int(datetime.today().strftime('%m'))
    if numerical_month in [1,3,5,7,8,10,12]:
        total_days = range(1,32)
    elif numerical_month != 2:
        total_days = range(1,31)
    else:
        total_days = range(1,29)
    days = tk.Listbox(day_frame)
    for d in total_days:
        days.insert(tk.END, d)
    days_scroll = tk.Scrollbar(day_frame)
    days_scroll.configure(command=days.yview, orient=tk.VERTICAL)
    days.grid(row=0, column=0)
    days_scroll.grid(row=0, column=1, sticky='NS')

    year_frame = tk.Frame(gui)
    year_frame.grid_columnconfigure((0, 1), weight=1)
    year_frame.grid(row=0, column=2)
    year = tk.StringVar()
    current_year = datetime.today().strftime('%Y')
    year.set(current_year)
    years = tk.Listbox(year_frame)
    for y in range(1992, int(current_year)+1):
        years.insert(0, y)
    years_scroll = tk.Scrollbar(year_frame)
    years_scroll.configure(command=years.yview, orient=tk.VERTICAL)
    years.grid(row=0, column=0)
    years_scroll.grid(row=0, column=1, sticky='NS')

    ## Start button
    start_button = tk.Button(gui, text='Start', width=15, command=lambda:daily3(args))
    start_button.grid(row=2)
    gui.mainloop()

if __name__ == "__main__":
    main()
