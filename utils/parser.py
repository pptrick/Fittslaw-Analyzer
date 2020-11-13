import csv
import os
import copy

def getFiles(dir):
    file_list = []
    for root, _, files in os.walk(dir):
        for f in files:
            file_list.append(root + '/' + f)
    return file_list

def _isSameGroup(groupInfo, row, mapping_table):
    for index in mapping_table:
        if row[index] != groupInfo[mapping_table[index]]:
            if index<4:
                return False
    return True

def _setGroupInfo(groupInfo, row, mapping_table):
    for index in mapping_table:
        groupInfo[mapping_table[index]] = row[index]

def _avg(l):
    if len(l)==0:
        return -1
    else:
        return sum(l)/len(l)

def parseFile(path):
    data = []
    mapping_table = {0:'name', 1:'device', 2:'width', 3:'distance', 4:'trial', 5:'time', 6:'correct'}
    try:
        input_csv = open(path, "r", newline='')
        csv_reader = csv.reader(input_csv)
        isFirst = True
        groupInfo = {'name':'', 'device':'', 'width':'', 'distance':'', 'trial':'', 'time':'', 'correct':''}
        time = []
        for row in csv_reader:
            if(isFirst):
                # confirm csv in correct format
                assert(row[0]=='Name')
                assert(row[1]=='Device')
                assert(row[2]=='Width(cm)')
                assert(row[3]=='Distance(cm)')
                assert(row[4]=='Trial')
                assert(row[5]=='Time(ms)')
                assert(row[6]=='Correct')
                isFirst = False
            else:
                if not _isSameGroup(groupInfo, row, mapping_table):
                    # save previous group
                    if groupInfo['name'] != '' and groupInfo['device'] != '' :
                        groupInfo['trial'] = len(time)
                        groupInfo['time'] = _avg(time)
                        groupInfo['width'] = float(groupInfo['width'])
                        groupInfo['distance'] = float(groupInfo['distance'])
                        if groupInfo['time'] >= 0: # append legal data
                            data.append(copy.deepcopy(groupInfo))
                    # set new group according to current row
                    _setGroupInfo(groupInfo, row, mapping_table)
                    time = []
                if row[6] == 'true': # count correct hit only
                    time.append(int(row[5]))
    except IOError:
        print("can not open ", path, " as a csv file")
    except AssertionError:
        print("csv file is not in correct format! the head should be: \nName,Device,Width(cm),Distance(cm),Trial,Time(ms),Correct" )
    except TypeError:
        print("csv file data format error!")
    else:
        input_csv.close()
        return data
