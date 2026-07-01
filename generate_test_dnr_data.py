import csv

# This script will generate a set of example DNR data to use to test CANDEW during development as well as to provide
# users a way to learn how to use CANDEW

# Test data
test_data_list = [
    ["2004-11-29", "21:39:21", "carol", "alice", "0", "house", "house",],
    ["2004-10-06", "21:44:46", "alice", "eve", "15", "house", "house",],
    ["2004-10-07", "17:34:55", "alice", "bob", "12", "house", "house",],
    ["2004-10-07", "18:02:27", "carol", "alice", "15", "house", "random street 1",],
    ["2004-10-08", "00:59:12", "carol", "alice", "28", "random street 2", "random street 2",],
    ["2004-10-08", "11:28:44", "bob", "alice", "9", "house", "house",],
    ["2004-10-08", "11:43:09", "alice", "carol", "364", "random street 3", "random street 3",],
    ["2004-10-08", "11:51:02", "alice", "dave", "200", "random street 3", "random street 3",],
    ["2004-10-08", "12:27:24", "dave", "alice", "1782", "house", "house",],
    ["2004-10-08", "14:52:41", "alice", "carol", "90", "warehouse", "warehouse",],
    ["2004-10-08", "15:59:59", "dave", "alice", "8", "house", "house",],
    ["2004-10-08", "18:29:45", "bob", "alice", "19", "warehouse", "warehouse",],
    ["2004-10-08", "23:28:09", "bob", "alice", "0", "airport", "airport",],
    ["2004-10-09", "11:09:09", "dave", "alice", "0", "house", "house",],
    ["2004-10-09", "11:32:14", "alice", "carol", "0", "shop", "shop",],
    ["2004-10-09", "12:15:55", "carol", "alice", "0", "shop", "shop",],
    ["2004-10-09", "14:44:01", "alice", "bob", "0", "warehouse", "warehouse"],
    ["2004-10-09", "17:17:17", "alice", "dave", "0", "random street 4", "random street 4",],
    ["2004-10-09", "19:02:54", "dave", "alice", "0", "warehouse", "warehouse",],
    ["2004-10-09", "21:18:33", "alice", "carol", "0", "random street 3", "random street 3",],
    ["2004-10-10", "00:12:24", "alice", "bob", "0", "house", "house",],
    ["2004-10-10", "00:44:01", "alice", "bob", "0", "house", "house",],
    ["2004-10-10", "01:17:57", "alice", "bob", "0", "house", "house",],
    ["2004-10-11", "12:12:17", "alice", "superlongname", "0", "house", "house",],
    ["2004-10-11", "12:14:34", "alice", "carol", "0", "house", "house",],
    ["2004-10-11", "19:19:04", "bob", "alice", "0", "house", "house",],
# Uncomment below to test targetCountMismatchError
    # ["2004-10-11", "12:15:34", "alice", "alice", "0", "house", "house",],
# Uncomment below to test callDurationNegativeError
    # ["2004-10-11", "12:12:12", "alice", "bob", "-12", "house", "house"],
# Uncomment below to test eventElementCountError
    # # ["2004-10-07", "18:02:27", "carol", "alice", "house",],
]

# Write test data to file
with open("test_data.csv", "w") as wx:
    wxc = csv.writer(wx)
    wxc.writerows(test_data_list)

