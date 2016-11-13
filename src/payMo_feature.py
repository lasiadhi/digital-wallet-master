
# coding: utf-8

# In[2]:

# Feature 01/02/03 implementation
# by Lasith Adhikari
# University of California, Merced
# 2016/11/12

# load required packages

import numpy as np
import csv   # this code is handled to use csv files. but it works with comma separated text files as well.
import os, errno
import sys
import time

degree              = int(sys.argv[-4])  # e.g.: degree = 1: 1st degree friendship, degree = 4: 4th degree, etc.
filename_history    = sys.argv[-3] # file contains infomation to build the network
filename_payments   = sys.argv[-2] # file contains ids with new transcations to be done
output_file  	    = sys.argv[-1] # output file name


# Generalized function to work with any degree of friendship
# This function check whether the receiver is a friend of sender's friends (i.e. oldlist)

def IsdegNfriend(sender, reciver, deg1friends, oldlist):
    newList=[]
    for i in oldlist:
        if reciver in deg1friends[i]:
            return True, newList       # if receiver is in, return true
        else:
            newList = newList + ([x for x in deg1friends[i] if x != sender])   
    return False, np.unique(list(set(newList) - set(oldlist)))     # if receiver is not in, return the next degree friendlist


# this function is to delete the existing file before create a new file
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: #
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured

print('wait...')

start_time = time.time()  # start to time

#maxInt = sys.maxsize
#csv.field_size_limit(sys.maxsize)


silentremove(output_file)

# create an empty dictionary to hold user id (key) and his/her friend list (values)
deg1_friends = {}

# read new sender and receiver id row by row from filename_payments file
with open(filename_payments,'rt', encoding='ISO-8859-1') as csvfile_pay:
    datareader_pay = csv.reader(csvfile_pay, delimiter=',')
    next(csvfile_pay)    # skip the header
    for row_pay in datareader_pay:
        id1_send_pay = int(row_pay[1]) # read sender id
        id2_rece_pay = int(row_pay[2]) # read receiver id
        

        ###### for the given sender, find his/her friends  #####
        
        # creating a list to hold all senders friends
        deg1_friends[id1_send_pay] = []
        
        trust = False;  # set trust to false until we detect receiver is a deg-N friend

       # now read the filename_history file row by row to find friends of new sender
        with open(filename_history,'rt', encoding='ISO-8859-1') as csvfile_hist:
            datareader_hist = csv.reader(csvfile_hist, delimiter=',')
            next(csvfile_hist)  # skip the header
            try:
                for row_hist in datareader_hist:
                    id1_send_hist = int(row_hist[1]) # read sender id
                    id2_rece_hist = int(row_hist[2]) # read receiver id
                    
                    if not id1_send_hist in deg1_friends:   # check old sender has a key in the dictionary
                        deg1_friends[id1_send_hist] = []   # create an empty list for old sender
                    if not id2_rece_hist in deg1_friends:  # check old receiver has a key in the dictionary
                        deg1_friends[id2_rece_hist] = []   # create an empty list for old receiver

                    # append degree 1 friends each other to the dictionary
                    deg1_friends[id1_send_hist].append(id2_rece_hist)
                    deg1_friends[id2_rece_hist].append(id1_send_hist)

                    
            except:  # to handle any error in the datareader
                print('Error in datareader\n')

            
        if id2_rece_pay in deg1_friends[id1_send_pay]:   # if new receiver is a deg-1 friend of new sender, done!
            trust = True
        else: # if not, read generate next degree friend list
            FriList = deg1_friends[id1_send_pay]
            for i in range(1,degree):
                isFriend, degNFri = IsdegNfriend(id1_send_pay, id2_rece_pay, deg1_friends, FriList)
                if isFriend == True:
                    trust = True
                    break
                else:
                    FriList = degNFri   # bring friend-list to next level
                
        # open the output file to write results for each transactions
        with open(output_file, "a") as myfile:
            if trust:
                myfile.write("trusted\n")
            else:
                myfile.write("unverified\n")
        deg1_friends = {}  #clear the friend list for the current sender
print("--- %s seconds ---" % (time.time() - start_time))
print('Done! Please check the paymo_output/output<feature#>.txt for the results.')

