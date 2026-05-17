import csv

test_data_list = [
    ["2004-10-06", "21:44:46", "alice", "eve", "house", "house",],
    ["2004-10-07", "17:34:55", "alice", "bob", "house", "house",],
    ["2004-10-07", "18:02:27", "carol", "alice", "house", "random street 1",],
    # ["2004-10-07", "18:02:27", "carol", "alice", "house",],
    ["2004-10-08", "00:59:12", "carol", "alice", "random street 2", "random street 2",],
    ["2004-10-08", "11:28:44", "bob", "alice", "house", "house",],
    ["2004-10-08", "11:43:09", "alice", "carol", "random street 3", "random street 3",],
    ["2004-10-08", "11:51:02", "alice", "dave", "random street 3", "random street 3",],
    ["2004-10-08", "12:27:24", "dave", "alice", "house", "house",],
    ["2004-10-08", "14:52:41", "alice", "carol", "warehouse", "warehouse",],
    ["2004-10-08", "15:59:59", "dave", "alice", "house", "house",],
    ["2004-10-08", "18:29:45", "bob", "alice", "warehouse", "warehouse",],
    ["2004-10-08", "23:28:09", "bob", "alice", "airport", "airport",],
    ["2004-10-09", "11:09:09", "dave", "alice", "house", "house",],
    ["2004-10-09", "11:32:14", "alice", "carol", "shop", "shop",],
    ["2004-10-09", "12:15:55", "carol", "alice", "shop", "shop",],
    ["2004-10-09", "14:44:01", "alice", "bob", "warehouse", "warehouse"],
    ["2004-10-09", "17:17:17", "alice", "dave", "random street 4", "random street 4",],
    ["2004-10-09", "19:02:54", "dave", "alice", "warehouse", "warehouse",],
    ["2004-10-09", "21:18:33", "alice", "carol", "random street 3", "random street 3",],
    ["2004-10-10", "00:12:24", "alice", "bob", "house", "house",],
    ["2004-10-10", "00:44:01", "alice", "bob", "house", "house",],
    ["2004-10-10", "01:17:57", "alice", "bob", "house", "house",],
    ["2004-10-11", "12:12:17", "alice", "superlongname", "house", "house",],
    ["2004-10-11", "12:14:34", "alice", "carol", "house", "house",],
    # ["2004-10-11", "12:15:34", "alice", "alice", "house", "house",],
]

with open("test_data.csv", "w") as wx:
    wxc = csv.writer(wx)
    wxc.writerows(test_data_list)

