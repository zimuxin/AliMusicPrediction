# -*- coding: utf-8 -*-
# @Author      : leeYandong,CaoWenqiang


import time
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

#--------stable-------------------
import os,sys
from numpy import fmax
path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)
import static_data as sd
CURRENT_PATH=sd.CURRENT_PATH
ARTIST_FOLDER=sd.ARTIST_FOLDER
ARTIST=sd.ARTIST
SONGS=sd.SONGS
SONG_P_D_C=sd.SONG_P_D_C
ARTIST_P_D_C=sd.ARTIST_P_D_C
SONG_FAN=sd.SONG_FAN
ARTIST_FAN=sd.ARTIST_FAN
DAYS=sd.DAYS
START_UNIX  =sd.START_UNIX
DAY_SECOND  =sd.DAY_SECOND
START_WEEK=sd.START_WEEK
#--------stable-------------------

'''
date:
    %Y%m%d 20150301
'''
def date2Num(date):
    return (int(time.mktime(time.strptime(date,'%Y%m%d')))-START_UNIX)//DAY_SECOND


"""
GOT THE 'PLAY','DOWNLOAD' AND 'COLLECT' TIMES IN 'mars_tianchi_user_action.csv' FILE FOR EVERY DAY.
THEN GOT A 'SONGS' STRUCTURE.
LAST WRITE 'SONGS' INTO SONG.TXT FILE.
SONGS={'SONGS_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]],'SONGS_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]],'SONGS_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]]...}
user={songs_id:[{},{},{},...,{}],songs_id:[{},{},{},...,{}],songs_id:[{},{},{},...,{}]}
"""
def ifNoSongTXT():
    user = {}
    songs = {}
    with open(SONGS) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            if row[1] not in songs:
                songs[row[1]] = [[0 for i in range(DAYS)] for j in range(3)]
            songs[row[1]][int(row[3])-1][date2Num(row[4])] += 1

            if row[3] == "1":
                if row[1] not in user:
                    user[row[1]] = [{} for i in range(DAYS)]
                user[row[1]][date2Num(row[4])][row[0]] = True

    with open(SONG_P_D_C, "w") as fw:
        for i in songs:
            fw.write(i+"\n")
            fw.write(",".join(str(x) for x in songs[i][0])+"\n")
            fw.write(",".join(str(x) for x in songs[i][1])+"\n")
            fw.write(",".join(str(x) for x in songs[i][2])+"\n")

    with open(SONG_FAN, "w") as fw:
        for i in user:
            fw.write(i+"\n")
            fw.write(",".join(str(len(x)) for x in user[i])+"\n")


"""
BEFORE RUN THIS CODE,PLEASE RUN 'ifNoSongTxt' FIRSTLY!
ARTIST={'ARTIST_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]],'ARTIST_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]],'ARTIST_ID':[[],[],[]...[]],[[],[],[]...[]],[[],[],[]...[]]...}
user={[{user_id:bool...},{user_id:bool...},...,{user_id:bool...}]}
"""
def ifNoArtistTXT():
    user={}
    artist={}
    index={}
    with open(ARTIST) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            index[row[0]] = row[1]
            if row[1] not in artist:
                artist[row[1]] = [[0 for i in range(DAYS)] for j in range(3)]
                user[row[1]] = [{} for i in range(DAYS)]

    with open(SONG_P_D_C, "r") as fr:
        songs_id=fr.readline().strip("\n")
        while songs_id:
            temp=[]
            play = list(map(int, fr.readline().strip("\n").split(",")))
            download = list(map(int, fr.readline().strip("\n").split(",")))
            collect = list(map(int, fr.readline().strip("\n").split(",")))
            temp.append(play)
            temp.append(download)
            temp.append(collect)
            t=artist[index[songs_id]]
            for i in range(3):
                for j in range(DAYS):
                    t[i][j]+=temp[i][j]
            artist[index[songs_id]]=t
            songs_id=fr.readline().strip("\n")

    with open(ARTIST_P_D_C, "w") as fw:
        for i in artist:
            fw.write(i+"\n")
            fw.write(",".join(str(x) for x in artist[i][0])+"\n")
            fw.write(",".join(str(x) for x in artist[i][1])+"\n")
            fw.write(",".join(str(x) for x in artist[i][2])+"\n")

    with open(SONGS) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            if row[1] in index:
                user[index[row[1]]][date2Num(row[4])][row[0]]=True

    with open(ARTIST_FAN, "w") as fw:
        for i in user:
            fw.write(i+"\n")
            fw.write(",".join(str(len(x)) for x in user[i])+"\n")

def testForSongTXT():
    count=0
    with open(SONG_P_D_C, "r") as fr:
        songs_id=fr.readline().strip("\n")
        while songs_id:
            temp=[]
            play=list(map(int, fr.readline().strip("\n").split(",")))
            download=list(map(int, fr.readline().strip("\n").split(",")))
            collect=list(map(int, fr.readline().strip("\n").split(",")))
            for i in play:
                count+=i
            for i in download:
                count+=i
            for i in collect:
                count+=i
            songs_id=fr.readline().strip("\n")
    print(count)    #5652232

def mean_artist_play(time,writer):
    with open(ARTIST_P_D_C, "r") as fr:
           
        artist_id = fr.readline().strip("\n")
        while artist_id:
            play = list(map(int, fr.readline().strip("\n").split(",")))
            download = list(map(int, fr.readline().strip("\n").split(",")))
            collect = list(map(int, fr.readline().strip("\n").split(",")))
            play1=np.array(play[174:183])
            #play1=np.array(play[176:183])
            play2=np.array(play[168:183])
            
            gradient = np.mean(play[176:183]) - np.mean(play[169:176])
            
            #mydownload = np.array(collect[169:183])
            #mycollect  = np.array(collect[169:183])
            mu1=np.mean(play1)
            mu2=np.mean(play2)
            col_in_download = np.mean(collect)/np.mean(download)           
            sigma1 = np.var(play1)
            sigma2 = np.var(play2)
            
            
            
            myplay =list( np.array(play[169:183]))
            #myplay =list(play1)
            if sigma1 <= sigma2:
                min1 = min(play1)
                max1 = max(play1)
                sum1 = (sum(play1) - min1 - max1) / 7
                myplay.append(sum1*((1+col_in_download)*(1+gradient/abs(gradient)*col_in_download)))               
            else:
                min2 = min(play2)
                max2 = max(play2)
                sum2 = (sum(play2) - min2 - max2) / 13
                myplay.append(sum2*((1+col_in_download)*(1+gradient/abs(gradient)*col_in_download)))   
            
            i = 1
            for t in time:
                subList = myplay[i:]
                finalmin = min(subList)
                finalmax = max(subList)
                finalsum = (sum(subList) - finalmin - finalmax) / 12
                myplay.append(finalsum)
                i = i + 1
                
                ans=[]
                ans.append(artist_id)
                ans.append(int(finalsum+0.5))
                ans.append(t)
                writer.writerow(ans)
           
            artist_id = fr.readline().strip("\n")
   

if __name__ == "__main__":
   
    timeList = []
    for j in range(1, 31):
        if j < 10:
            timeList.append('2015090' + str(j))
        else:
            timeList.append('201509' + str(j))

    for j in range(1, 31):
        if j < 10:
            timeList.append('2015100' + str(j))
        else:
            timeList.append('201510' + str(j))
    csvres = file('./mars_tianchi_artist_plays_predict.csv', 'wb')
    writer = csv.writer(csvres)
    
    mean_artist_play(timeList,writer)
    
    print 'finished'
    #total time 371.4s
