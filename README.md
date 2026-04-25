# CANDEW
CANDEW is a command line-based Dialed Number Records (DNR) traffic analysis tool written in Python. It analyzes the metadata 
of phone records to provide insights into a target's pattern-of-life and their possible relationships to those they are 
in contact with.

## Compatibility
CANDEW is compatible with Python 3.10 and upwards, and is also OS independent, meaning it can operate on Linux, Windows and 
Mac machines. Additionally, it relies only on Python's standard library and does not require any additional packages.

## Usage
CANDEW is used via the command line:
Linux and Mac:
`python3 candew.py -r "dnr_data.csv" -t "123-456-7890"`

Windows:
`py candew.py -r "dnr_data.csv" -t "123-456-7890"`

The following arguments are available:
* `-r, --record`: The absolute or relative path of the file containing the DNR data - REQUIRED 
* `-t, --target`: The number or name of the target of the DNR file (case sensitive) - REQUIRED
* `-h, --help`: Displays the help banner - OPTIONAL

## Formatting Requirements
For CANDEW to analyze the DNR data, it must follow certain formatting requirements:
* The DNR data must be in `Comma Separated Value (CSV)` format
* There must be 6 elements per entry in the following order:
  - Date (YYYY-MM-DD)
  - Time (HH) - (in 24-hr format)
  - Calling Number
  - Called Number
  - Tower Start Location
  - Tower End Location
  
The calling and called number fields can be represented by the actual phone numbers themselves or by names. However, it should 
be noted that if names are used, ensure that there are no duplicate names for contacts (ex. two different numbers whose owners 
both have the name "Alice") as this will mess with the analysis.

Furthermore, CANDEW does not check the quality of the data given to it. If it is given bad data, it will give a bad analysis, so 
the onus of quality control is on the user.

## Types of Analysis
CANDEW has 5 sections of analysis in the following order:
1. Hour of Day (HoD) Analysis
2. Day of Week (DoW) Analysis
3. Day of Year (DoY) Analysis
4. Tower Location Analysis
5. Contacts Analysis

Each section follows a standard format, consisting of a `total count analysis`, a `calling count analysis` and a 
`called count analysis` (and in the case of the Tower Location Analysis section, a `total location count analysis`, 
a `start location count analysis` and an `end location count analysis`). 

The results are displayed via text-based bars and the associated numerical data. The bars provide a visual represetation of 
the percentage counts, where each `=` is equivalent to 5%. Because of the way the bars work, the values displayed in them 
are rounded to the nearest multiple of 5.  

Below is an example of what the bars look like:
```
 Total events per DoW
 --------------------
 Monday:    [==                  ] 8.33% - (2/24)
 Tuesday:   [                    ] 0.0% - (0/24)
 Wednesday: [=                   ] 4.17% - (1/24)
 Thursday:  [==                  ] 8.33% - (2/24)
 Friday:    [=======             ] 37.5% - (9/24)
 Saturday:  [======              ] 29.17% - (7/24)
 Sunday:    [==                  ] 12.5% - (3/24)
```

The analysis is conducted by importing the DNR data into a SQLite file that CANDEW creates called `.candew_dnr.db`. Once the 
analysis is complete, CANDEW clears the data from the file. It also clears the file before importing data from the CSV, in case
anything was left over from the previous analysis, ensuring that only data the user meant to analyze is used.

> [!NOTE]
> Larger data sets may require more time to fully analyze.

### Hour of Day (HoD) Analysis
The Hour of Day analysis section focuses on analyzing the event data based on the hour that they occurred. The results are displayed
from 00-23 and is useful for gaining insight into the hourly activity pattern of the target, which can help determine what times
they are most active/inactive (ex. what time they go to sleep and what time they wake up).   

### Day of Week (DoW) Analysis
The Day of Week (DoW) analysis section analyzes the DNR data based on the DoW that they occurred. The results can help in
understanding a target's weekly activity pattern, showing which days of the week they might be more/less active.  

### Day of Year (DoY) Analysis
The Day of Year (DoY) analysis section is meant to act as a slightly more granular version of the DoW analysis section. Here,
the data is analyzed based on the DoY that it occurred. This can be useful for detecting communication frequency patterns that
fall outside of a target's norm (ex. if a target normally makes/receives ~30 calls per day, but then one day makes/receives over 
100, or they only made/received less than 5 calls that day). This can then be correlated with additional data sources to 
determine why the spike/drop occurred.

### Tower Location Analysis
The Tower Location analysis section focuses on the tower locations that appear in the DNR data. It will provide the
user a complete list of all the unique tower locations present in the records as well as the frequency at which they are
used, with the results being displayed in a highest-to-lowest order. This is useful for determining areas that a target 
frequents and can give insight into things such as where they may live, where they work/what kind of job they have, if they 
traveled outside of their normal areas of activity, etc. Correlation with additional pieces of information can help shed more
light on the relevance of the locations to the target.  

> [!NOTE]
> In the total count analysis, the total number count is always doubled (ex. 24 events will show as 48). This is because the
> total count combines both the start and end tower location columns and because the same tower can appear as both the
> start and end location in a single event.

### Contacts Analysis
The Contacts Analysis section focuses on the contacts found within the DNR data. It will show the user a complete list
of all unique contacts along with their frequency of communication, with the results being displayed in a highest-to-lowest 
order. This section can assist in gaining insight into the social circle of the target, helping narrow down the list to a few 
key contacts to focus on. Moreover, correlation with additional data can further the understanding of their relationships 
to the target (ex. the target calls a number frequently during the late evenings and speaks with them for extended times, 
suggesting a close personal relationship to that contact). 

> [!TIP]
> To make it easier to identify contacts in the Contacts Analysis section, it is recommended to combine
> numbers and names where possible (ex. `999-999-9999 (Alice)`, `Bob (123-456-7890)`, etc.). Additionally,
> this alleviates the drawback of using only names, as it will ensure that every contact is unique and recognizable.

## Errors
The following is a list of all error names, their descriptions and what might cause them:
* `emptyPathError`: `-r, --record arg is empty, no path specified`: This error occurs when the `-r, --record` argument is given blank spaces or nothing at all (ex. `""`, `"     "`).
* `noTargetSpecifiedError`: `-t, --target arg is empty, no target specified`: This error occurs when the `-t, --target` argument is given blank spaces or nothing at all (ex. `""`, `"     "`).
* `pathError`: `Could not find 'FILE PATH', check path and try again`: This error occurs when CANDEW cannot find the file/path provided to it via the `-r, --record` argument. Double check that you have the entered the file name/path correctly and try again. 
* `eventElementCountError`: `DNR event line 'LINE NUMBER' has incorrect number of elements: 'ENTRY ELEMENT COUNT' (required: 6)`: This error occurs when CANDEW comes across a DNR event that does not have exactly 6 elements in it. To resolve this issue, check the entry line number provided by the error to see which entry in the CSV file is causing the problem.
* `loadCountError`: `Not all event data was loaded into SQLite file, try again`. This error occurs if not all of the DNR event data was loaded from the CSV file into the SQLite file `.candew_dnr.db`. If this happens, simply try again.
* `targetNotFoundError`: `Target 'NAME' was not found in DNR event data, double check and try again`. This occurs if CANDEW cannot find the target specified via the `-t, --target` argument. Double check that you entered the number/name correctly and try again. If that does not work, check the file specified via `-r, --records` and try again. 
* `targetCountMismatchError`: `Target occurrence count does not match number of DNR events: 'TARGET COUNT/TOTAL EVENT COUNT'`. This error occurs if the number of times the target's number/name shows up in the DNR data is not equal to the number of events. This could be because either the target occurs too many times in the event data (ex. an entry shows the calling and called number both to belong to the target) or occurs too few times (ex. an entry shows the calling and called number to belong to two different contacts, neither one being the target). To resolve this issue, you will need to go through the DNR data file and determine which entries are causing the error. Once fixed, try again. 

## Terminology
This section provides a list of terminology used in CANDEW and their definitions:
* `Dialed Number Records (DNR)`: A file containing the phone record metadata.
* `Event`: A single entry in the DNR file.
* `Target`: The individual that the DNR data pertains to.
* `Contact`: Any numbers/individuals that the target communicates with. 
* `Calling Number`: The number that initiated the event.
* `Called Number`: The number that recieved the event.
* `Start Tower Location`: The location of the telecommunications tower where the event was initiated.
* `End Tower Location`: The location of the telecommunications tower where the event ended.

## Branches
This repository has 2 branches: `master` and `dev`. The `master` branch holds all the stable code and is updated
whenever a new stable version of CANDEW is released. The `dev` branch on the other hand is updated more often, with
new changes being committed to it first.

## License
CANDEW is licensed under GPLv3. The full license can be found in the `LICENSE` file.

## Contributing
Interested in contributing to CANDEW? Check out the `CONTRIBUTING.md` file to learn how.

