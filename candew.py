"""
CANDEW\n
v1.0.0\n
`Dialed Number Records (DNR) traffic analysis tool`\n
`Copyright (C) 2026 darkmattergit`\n
--------------------------------------------\n
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.\n

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.\n

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import datetime
import csv
import sqlite3
import argparse
import glob

# Const tuple containing the names of the days of the week
DAYS_OF_WEEK_TUPLE = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)

# Const tuple containing the hours of the day in 24-hr format
HOURS_OF_DAY_TUPLE = (
    "00", "01", "02",
    "03", "04", "05",
    "06", "07", "08",
    "09", "10", "11",
    "12", "13", "14",
    "15", "16", "17",
    "18", "19", "20",
    "21", "22", "23",
)

# CANDEW version number constant
CANDEW_VERSION = "1.0.0"

# Opening banner constant
CANDEW_BANNER = r"""   
   _______      ____       ___   ___   ______     ______   ____          ____    
  /   ___/     /    \     |   \ |  |  |      \   |   ___|  \   \   /\   /   /                     
 /   /        /  []  \    |    \|  |  |  | |  |  |      |   \   \_/  \_/   /                      
 \   \___    /  ____  \   |  |\    |  |  | |  |  |   ___|    \    _/\_    /
  \______\  /__/    \__\  |__| \___|  |______/   |______|     \__/    \__/
"""

# Small GPLv3 blurb constant
GPL_BLURB = """This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.\n
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.\n"""


def _create_bar(calculate_value: int = None, count_total:int = None) -> str:
    """
    Creates a text-based bar that acts as a visual representation of a percentage calculation. Each '=' represents
    5%.
    :param calculate_value: The value to divide by
    :param count_total: The total count to divide by
    :return: None
    """
    # Convert the two int values into floats to get the percentage
    value_total_percent = float(calculate_value) / float(count_total)

    # Convert the percentage calculation into an int
    total_int = int(value_total_percent * 100)

    # Determine how close or far the value is from being a multiple of 5
    check_rounding = total_int % 5

    rounded_value = 0

    # If the rounding is <= 2 and != 0, subtract the modulus (ex. 16 -> 15)
    if check_rounding <= 2 and check_rounding != 0:
        rounded_value = total_int - check_rounding

    # The value is already a multiple of 5, so there is no extra calculation needed
    elif check_rounding == 0:
        rounded_value = total_int

    # If the rounding >= 3, add the remainder needed to reach a multiple of 5 (ex. 18 -> 20)
    elif check_rounding >= 3:
        rounded_value = total_int + (5 - check_rounding)

    # Calculate the number of '=' required by dividing the newly rounded value by 5
    bar_length = rounded_value // 5

    # Create the bar
    calculated_bar = f"[{'=' * bar_length:20}]"

    return calculated_bar


def display_results(results_to_display: list | dict = None, total_count: int = None) -> None:
    """
    Function to display results so that the whole display process does not need to be repeatedly recreated for each
    section.
    :param results_to_display: The list or dict containing the results names and their counts to display.
    :param total_count: The total number of DNR events
    :return: None
    """
    # Initialize int to hold len of longest name
    longest_name_len = 0

    # Results display process if results_to_display is type list
    if type(results_to_display) is list:

        # Get the len of the longest name in the list
        for results_lens in results_to_display:
            if len(results_lens[0]) > longest_name_len:
                longest_name_len = len(results_lens[0])

        # Display results
        for list_names, list_nums in results_to_display:
            # Create the percentage bar
            percentage_bar = _create_bar(list_nums, total_count)
            # Calculate the percentage count
            percentage_count = round((list_nums / total_count * 100), 2)

            # Format and display results
            print(f" {list_names}:{'':{longest_name_len - len(list_names)}} {percentage_bar} {percentage_count}% - "
                  f"({list_nums}/{total_count})")

    # Results display process if results_to_display is type dict
    elif type(results_to_display) is dict:

        # Get the len of the longest name in the dict
        for dict_lens in results_to_display:
            if len(dict_lens) > longest_name_len:
                longest_name_len = len(dict_lens)

        # Display results
        for dict_names in results_to_display:
            # Create the percentage bar
            percentage_bar = _create_bar(results_to_display[dict_names], total_count)
            # Calculate the percentage count
            percentage_count = round((results_to_display[dict_names] / total_count * 100), 2)

            # Format and display results
            print(f" {dict_names}:{'':{longest_name_len - len(dict_names)}} {percentage_bar} {percentage_count}% - "
                  f"({results_to_display[dict_names]}/{total_count})")

    print()


def create_total_dict(list1: list = None, list2: list = None) -> dict:
    """
    Creates a dict by combining the results from two different lists of tuples. The tuples must be in the following
    format: (name, value).
    :param list1: The first list.
    :param list2: The second list.
    :return: dict
    """
    # Initialize dict
    total_dict = {}

    # Add the names and values from the first list to the dict
    for name1, value1 in list1:
        total_dict[name1] = value1

    # Add the names and values from the second list to the dict
    for name2, value2 in list2:
        # If the name is already present in the dict, add value2 to the existing value
        if name2 in total_dict:
            total_dict[name2] += value2

        else:
            total_dict[name2] = value2

    return total_dict


def order_dict(dict_to_order: dict = None) -> dict:
    """
    Order a dict from highest to lowest values.
    :param dict_to_order: The dict that is to be ordered
    :return: dict
    """
    # Initialize dict that will hold the ordered key-value pairs
    ordered_dict = {}

    # Iterate through the unordered dict the number of times equal to the number of key-value pairs
    for _ in range(len(dict_to_order)):
        highest_key = None
        highest_key_val = 0

        # Iterate through the values of the unordered dict to determine which key has the highest value
        for vals in dict_to_order:
            if dict_to_order[vals] >= highest_key_val:
                highest_key = vals
                highest_key_val = dict_to_order[vals]

        # Add the key-value pair to the ordered dict and delete the respective key-value pair from the unordered dict
        ordered_dict[highest_key] = highest_key_val
        del dict_to_order[highest_key]

    return ordered_dict


def zero_dict(dict_to_zero: dict = None) -> None:
    """
    Sets all values in a dict to zero.
    :param dict_to_zero: The dict to set the values to zero.
    :return: None
    """
    # Iterate through the dict and set the values to 0
    for values in dict_to_zero:
        dict_to_zero[values] = 0


def add_to_dict(dict_to_use: dict = None, results_to_add: list = None) -> None:
    """
    Add the elements from a list to a dict. The list must be in the following format: [(name, value),]
    :param dict_to_use: The dict to add the elements to.
    :param results_to_add: The list that contains the elements that are to be added to the dict.
    :return: None
    """
    # Iterate through the list and add the elements to the dict
    for result_names, result_values in results_to_add:
        dict_to_use[result_names] = result_values


def count_total_events_dict(dict_to_count: dict = None, total_count: int = None) -> None:
    """
    Calculcate the total count of the values in a dict.
    :param dict_to_count: The dict to calculate the total from.
    :param total_count: The total number of DNR events.
    :return: None
    """
    # Initialize int to hold total
    dict_total = 0

    # Calculate the total from the values of the dict
    for values in dict_to_count:
        dict_total += dict_to_count[values]

    # Display counts
    print(f" [*] Total events: {dict_total}/{total_count}")
    print()


def count_hours(hours_list: list = None, total_count:int = None) -> None:
    """
    Conducts analysis of DNR event data based on the times, specifically the hour, the events occurred.
    :param hours_list: The list containing the count total of each hour
    :param total_count: The total number of DNR events
    :return: None
    """
    # Initialize count to keep track of the total value of the hours_list param
    total_events_count = 0

    # Iterate through the HOURS_OF_DAY_LIST and the hours_list param to display time analysis
    for hours_day, event_hours in zip(HOURS_OF_DAY_TUPLE, hours_list):
        # Add the current value of event hours to the total event count
        total_events_count += event_hours

        # Calculate the percentage of the event_hour count to decimal places
        hour_percentage = round((event_hours / total_count * 100), 2)

        # Display results
        print(f" {hours_day}: {_create_bar(event_hours, total_count)} {hour_percentage}% - "
              f"({event_hours}/{total_count})")

    print()
    print(f" [*] Total events: {total_events_count}/{total_count}")


def count_days_of_week(dow_list: list = None, total_count: int = None) -> None:
    """
    Conducts analysis of DNR data based on the Days of Week (DoW) that the events occurred.
    :param dow_list: The list containing the count associated to each DoW
    :param total_count: The total number of DNR events
    :return: None
    """
    # Initialize variable to keep count of the number of events
    total_events_count = 0

    # Iterate through the dow_list param and the DAYS_OF_WEEK_LIST const
    for dow_names, dow_counts in zip(DAYS_OF_WEEK_TUPLE, dow_list):
        # Add the current element of the dow_list to the total_events_count variable
        total_events_count += dow_counts

        # Format the name of the DoW as trying to do it in the print statement results in wonky alignment
        formatted_dow_name = f"{dow_names}:"

        # Calculate the percentage of the current element count
        dow_percentage_count = round((dow_counts / total_count * 100), 2)

        # Display results
        print(f" {formatted_dow_name :{10}} {_create_bar(dow_counts, total_count)} {dow_percentage_count}% - "
              f"({dow_counts}/{total_count})")

    print()
    print(f" [*] Total events: {total_events_count}/{total_count}")


def count_days_of_year(unique_days_dict: dict = None, total_count: int = None) -> None:
    """
    Conducts analysis of DNR event data based on the Day of Year (DoY) that the events occurred.
    :param unique_days_dict: The dict containing the DoY dates and their counts
    :param total_count: The total number of DNR events
    :return: None
    """
    # Initialize variable to keep track of total events that occurred as there may be more calling events than called
    # and vice versa
    total_events = 0

    # Iterate through the dict that contains the DoY counts
    for days_dict in unique_days_dict:
        # Calculate the percentage of the DoY
        day_dict_percentage = round((unique_days_dict[days_dict] / total_count * 100), 2)

        # Split the date into the year, month and day to get the DoW of the DoY
        split_date = days_dict.split("-")
        split_date_year = int(split_date[0])
        split_date_month = int(split_date[1])
        split_date_day = int(split_date[2])

        # Get int representation of DoW
        doy_dow_name = datetime.date(split_date_year, split_date_month, split_date_day).weekday()

        # Specify the maximum length of the DoY plus the name of the DoW can be for alignment
        max_doy_len = 24

        # Format the DoY DoW
        dow_date_and_name = f"{days_dict} ({DAYS_OF_WEEK_TUPLE[doy_dow_name]}): "

        # Initialize variable to determine how much spacing is required for alignment
        spacing_length = 0

        # Calculate alignment spacing
        if len(dow_date_and_name) < max_doy_len:
            spacing_length = max_doy_len - len(dow_date_and_name)

        # Display results for DoY
        print(f" {dow_date_and_name}{'':{spacing_length}}{_create_bar(unique_days_dict[days_dict], total_count)} "
              f"{day_dict_percentage}% - ({unique_days_dict[days_dict]}/{total_count})")

        # Add event count to total
        total_events += unique_days_dict[days_dict]

    print()
    print(f" [*] Total events: {total_events}/{total_count}")


# Display the opening banner
print(CANDEW_BANNER)
print("  DNR Traffic Analysis Tool")
print(f"  Version: {CANDEW_VERSION}")
print("  License: GPLv3\n")

parser = argparse.ArgumentParser(description="Dialed Number Records (DNR) traffic analysis tool.")

parser.add_argument("-r", "--record", help="The absolute or relative path of the CSV file containing "
                                           "the DNR event data", required=True)
parser.add_argument("-t", "--target", help="The name or number of the target (case sensitive)",
                    required=True)
parser.add_argument("-g", "--gpl", help="Print GPLv3 blurb and exit", action="store_true")

args = parser.parse_args()

# Display GPLv3 blurb if specified by user and exit
if args.gpl:
    print(GPL_BLURB)
    exit()

dnr_record = args.record.strip()
dnr_target = args.target.strip()

# Check if -r, --record arg is blank
if dnr_record == "" or dnr_record.isspace():
    print("[!] emptyPathError :: -r, --record arg is empty, no path specified")
    exit()

# Check if -t, --target arg is blank
if dnr_target == "" or dnr_target.isspace():
    print("[!] noTargetSpecifiedError :: -t, --target arg is empty, no target specified")
    exit()

# Check if -r, --record path exists
if not glob.glob(dnr_record):
    print(f"[!] pathError :: Could not find '{dnr_record}', check path and try again")
    exit()

print(f"[+] Found '{dnr_record}', preparing to load data")

# Set up SQLite file
conn = sqlite3.connect(".candew_dnr.db")
crsr = conn.cursor()

# Create table if it does not exist
crsr.execute("CREATE TABLE IF NOT EXISTS dnr_records (call_date TEXT, call_dow TEXT, call_time TEXT, call_init "
             "TEXT, call_recv TEXT, start_location TEXT, end_location TEXT)")
conn.commit()

# Clear any data that may have been left over from previous analysis
crsr.execute("DELETE FROM dnr_records WHERE call_date LIKE '%%'")
conn.commit()

# Initialize variables to hold counts of the total number of DNR events, events that occurred during the weekday and
# events that occurred during the weekend
total_call_count = 0
weekday_count = 0
weekend_count = 0

# Initialize variable to keep track of current event number being imported from CSV to SQLite file
event_line_count = 0

# Initialize variable to keep track of number of times the target appears in DNR data
target_number_count = 0

# Import data from CSV file
with (open(dnr_record, "r") as dr):
    dnr_read = csv.reader(dr)

    for event_data in dnr_read:
        # For each entry, add 1 to indicate current entry line number being imported
        event_line_count += 1

        # Check to make sure that only 6 elements are present in the entry
        if len(event_data) != 6:
            print(f"[!] eventElementCountError :: DNR event line {event_line_count} has incorrect number of "
                  f"elements: {len(event_data)} (required: 6)")

            # Element count was not equal to 6, clean up and exit
            crsr.execute("DELETE FROM dnr_records WHERE call_date LIKE '%%'")
            conn.commit()
            exit()

        # Assign elements of entry to variables to make it easier to understand which is which
        call_date = event_data[0].strip()
        call_time = event_data[1].strip()
        call_init = event_data[2].strip()
        call_recv = event_data[3].strip()
        call_start_location = event_data[4].strip()
        call_end_location = event_data[5].strip()

        # Special check to catch any entries where both the calling and called numbers belong to the target
        if call_init == dnr_target and call_recv == dnr_target:
            target_number_count += 1

        # Count number of times target appears in data
        if call_init == dnr_target or call_recv == dnr_target:
            target_number_count += 1

        # Split the call date entry into a tuple
        call_date_dow_tuple = call_date.split("-")

        # Assign tuple values to variables to make understanding what is going on easier
        call_date_dow_tuple_year = int(call_date_dow_tuple[0])
        call_date_dow_tuple_month = int(call_date_dow_tuple[1])
        call_date_dow_tuple_day = int(call_date_dow_tuple[2])

        # Determine Day of Week (DoW)
        call_date_dow_int = datetime.date(call_date_dow_tuple_year, call_date_dow_tuple_month,
                                          call_date_dow_tuple_day).weekday()

        # Count the total number of records
        total_call_count += 1

        # Count number of records that occurred on weekdays
        if call_date_dow_int <= 4:
            weekday_count += 1

        # Count number of records that occurred on weekends
        else:
            weekend_count += 1

        # Insert data to SQLite file
        crsr.execute("INSERT INTO dnr_records VALUES (?, ?, ?, ?, ?, ?, ?)", (call_date,
                                                                      DAYS_OF_WEEK_TUPLE[call_date_dow_int],
                                                                      call_time[:2], call_init, call_recv,
                                                                      call_start_location, call_end_location))
        conn.commit()

print("[*] Running checks to ensure data was loaded correctly")

# Get the number entries present in SQLite file
crsr.execute("SELECT COUNT(*) FROM dnr_records")
confirm_load_count = crsr.fetchall()[0][0]

if confirm_load_count != total_call_count:
    print("[!] loadCountError :: Not all event data was loaded into SQLite file, try again")

    # Count of SQLite file entries does not match read-in count, clean up and exit
    crsr.execute("DELETE FROM dnr_records WHERE call_date LIKE '%%'")
    conn.commit()

    crsr.close()
    conn.close()
    exit()

print("    [+] Load count check: OKAY")

if target_number_count <= 0:
    print(f"[!] targetNotFoundError :: Target '{dnr_target}' was not found in DNR event data, double check and try "
          f"again")

    # Target is not present in the DNR data, clean up and exit
    crsr.execute("DELETE FROM dnr_records WHERE call_date LIKE '%%'")
    conn.commit()

    crsr.close()
    conn.close()
    exit()

print("    [+] Target check: OKAY")

if target_number_count != total_call_count:
    print(f"[!] targetCountMismatchError :: Target occurrence count does not match number of DNR events: "
          f"{target_number_count}/{total_call_count}")

    # Target appears too many/too few times in DNR data, clean up and exit
    crsr.execute("DELETE FROM dnr_records WHERE call_date LIKE '%%'")
    conn.commit()

    crsr.close()
    conn.close()
    exit()

print("    [+] Target count check: OKAY")
print()

print("[+] DNR event data successfully loaded into SQLite file, preparing to analyze")
print("[*] NOTE: Larger data sets may require more time to fully analyze")

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ HoD ANALYSIS //////////////////////////////////

# Initialize lists to hold hourly counts
hours_of_day_total_count = []
hours_of_day_init_count = []
hours_of_day_recv_count = []

# Iterate through the HOURS_OF_DAY_TUPLE const
for day_hours in HOURS_OF_DAY_TUPLE:
    # Get total counts based on hour of day
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_time = ?", (day_hours,))
    hours_of_day_total_count.append(crsr.fetchall()[0][0])

    # Get counts based on hour of day and where target is calling number
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_time = ? AND call_init = ?",
                 (day_hours, dnr_target))
    hours_of_day_init_count.append(crsr.fetchall()[0][0])

    # Get counts based on hour of day and where target is called number
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_time = ? AND call_recv = ?",
                 (day_hours, dnr_target))
    hours_of_day_recv_count.append(crsr.fetchall()[0][0])

print()
print("=================================== HoD ANALYSIS ===================================")

# Display results
print()
print(" Total events per hour")
print(" ---------------------")
count_hours(hours_of_day_total_count, total_call_count)
print()

print(" Total CALLING events per hour")
print(" -----------------------------")
count_hours(hours_of_day_init_count, total_call_count)
print()

print(" Total CALLED events per hour")
print(" ----------------------------")
count_hours(hours_of_day_recv_count, total_call_count)
print()

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ DoW ANALYSIS //////////////////////////////////
# Initialize lists to hold DoW counts
dow_total_count = []
dow_init_count = []
dow_recv_count = []

# Iterate through the DAYS_OF_WEEK_TUPLE const
for dow in DAYS_OF_WEEK_TUPLE:
    # Get total counts based on DoW
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_dow = ?", (dow,))
    dow_total_count.append(crsr.fetchall()[0][0])

    # Get counts based on DoW and where target is calling number
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_dow = ? AND call_init = ?",
                 (dow, dnr_target))
    dow_init_count.append(crsr.fetchall()[0][0])

    # Get counts based on DoW and where target is called number
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_dow = ? AND call_recv = ?",
                 (dow, dnr_target))
    dow_recv_count.append(crsr.fetchall()[0][0])

print("=================================== DoW ANALYSIS ===================================")
print()

# Display results
print(f" [*] Total events during weekdays: {weekday_count}/{total_call_count}")
print(f" [*] Total events during weekends: {weekend_count}/{total_call_count}")
print()

print(" Total events per DoW")
print(" --------------------")
count_days_of_week(dow_total_count, total_call_count)
print()

print(" Total CALLING events per DoW")
print(" ----------------------------")
count_days_of_week(dow_init_count, total_call_count)
print()

print(" Total CALLED events per DoW")
print(" ---------------------------")
count_days_of_week(dow_recv_count, total_call_count)
print()

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ DoY ANALYSIS //////////////////////////////////

# Get DoY from DNR data
crsr.execute("SELECT DISTINCT call_date FROM dnr_records")
unique_days = crsr.fetchall()

# Initialize dicts to hold DoY counts
unique_days_dict_total = {}
unique_days_dict_init = {}
unique_days_dict_recv = {}

# Iterate through the DoY in DNR data
for unique in unique_days:

    # Get total counts per DoY
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_date = ?", (unique[0],))
    unique_days_dict_total[unique[0]] = crsr.fetchall()[0][0]

    # Get counts per DoY and where target is calling number
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_date = ? AND call_init = ?",
                 (unique[0], dnr_target))
    unique_days_dict_init[unique[0]] = crsr.fetchall()[0][0]

    # Get counts per DoY and where target is called number
    crsr.execute("SELECT COUNT(*) FROM dnr_records WHERE call_date = ? AND call_recv = ?",
                 (unique[0], dnr_target))
    unique_days_dict_recv[unique[0]] = crsr.fetchall()[0][0]

print("=================================== DoY ANALYSIS ===================================")
print()

# Display results
print(f" [*] Number of unique days: {len(unique_days_dict_total)}")
print()

print(" Total events per DoY")
print(" --------------------")
count_days_of_year(unique_days_dict_total, total_call_count)
print()

print(" Total CALLING events per DoY")
print(" ----------------------------")
count_days_of_year(unique_days_dict_init, total_call_count)
print()

print(" Total CALLED events per DoY")
print(" ---------------------------")
count_days_of_year(unique_days_dict_recv, total_call_count)
print()

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ LOCATION ANALYSIS //////////////////////////////////

# Get counts of start locations
crsr.execute("SELECT DISTINCT start_location, COUNT(*) FROM dnr_records GROUP BY 1 ORDER BY 2 DESC")
start_location_counts = crsr.fetchall()

# Get counts of end locations
crsr.execute("SELECT DISTINCT end_location, COUNT(*) FROM dnr_records GROUP BY 1 ORDER BY 2 DESC")
end_location_counts = crsr.fetchall()

# Create dict that contains all tower locations and their counts
total_location_count = create_total_dict(start_location_counts, end_location_counts)

# Order the dict from highest to lowest
ordered_total_location_dict = order_dict(total_location_count)

# Display results
print("=================================== TOWER LOCATION ANALYSIS ===================================")
print()

print(f" [*] Total number of unique tower locations: {len(ordered_total_location_dict)}")
print()

print(" Total counts per tower location")
print(" -------------------------------")
display_results(ordered_total_location_dict, (total_call_count * 2))

# Zero the master dict
zero_dict(ordered_total_location_dict)
# Add the start location data to the dict
add_to_dict(ordered_total_location_dict, start_location_counts)
# Sort the dict
start_location_ordered = order_dict(ordered_total_location_dict)

print(" Counts per START tower location")
print(" -------------------------------")
display_results(start_location_ordered, total_call_count)

# Zero the master dict
zero_dict(ordered_total_location_dict)
# Add the end location data to the dict
add_to_dict(ordered_total_location_dict, end_location_counts)
# Sort the dict
end_location_ordered = order_dict(ordered_total_location_dict)

print(" Counts per END tower location")
print(" -----------------------------")
display_results(end_location_ordered, total_call_count)

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ CONTACTS ANALYSIS //////////////////////////////////

crsr.execute("SELECT DISTINCT call_init, COUNT(*) FROM dnr_records WHERE call_init != ? GROUP BY 1 ORDER BY 2 "
             "DESC",(args.target,))
unique_call_init_contacts = crsr.fetchall()

crsr.execute("SELECT DISTINCT call_recv, COUNT(*) FROM dnr_records WHERE call_recv != ? GROUP BY 1 ORDER BY 2 "
             "DESC",(args.target,))
unique_call_recv_contacts = crsr.fetchall()

total_unique_contacts_dict = create_total_dict(unique_call_init_contacts, unique_call_recv_contacts)

ordered_total_unique_contacts_dict = order_dict(total_unique_contacts_dict)

print("=================================== CONTACTS ANALYSIS ===================================")
print()

print(f" [*] Total number of unique contacts: {len(ordered_total_unique_contacts_dict)}")
print()

print(" Total events per contact")
print(" ------------------------")
display_results(ordered_total_unique_contacts_dict, total_call_count)
count_total_events_dict(ordered_total_unique_contacts_dict, total_call_count)

# ************************************* TARGET IS CALLING CONTACTS *************************************
# Zero the master dict
zero_dict(ordered_total_unique_contacts_dict)
# Add the call init data to the dict
add_to_dict(ordered_total_unique_contacts_dict, unique_call_init_contacts)
# Sort the dict
call_init_ordered = order_dict(ordered_total_unique_contacts_dict)

print(" Total CALLING events per contact")
print(" --------------------------------")
display_results(call_init_ordered, total_call_count)
count_total_events_dict(call_init_ordered, total_call_count)

# ************************************* TARGET IS BEING CALLED BY CONTACTS *************************************
# Zero the master dict
zero_dict(ordered_total_unique_contacts_dict)
# Add the call recv data to the dict
add_to_dict(ordered_total_unique_contacts_dict, unique_call_recv_contacts)
# Sort the dict
call_recv_ordered = order_dict(ordered_total_unique_contacts_dict)

print(" Total CALLED events per contact")
print(" -------------------------------")
display_results(call_recv_ordered, total_call_count)
count_total_events_dict(call_recv_ordered, total_call_count)

# Clear out DNR data
crsr.execute("DELETE FROM dnr_records WHERE call_date LIKE '%%'")
conn.commit()

# Close SQLite file
crsr.close()
conn.close()

print("[+] Done")
