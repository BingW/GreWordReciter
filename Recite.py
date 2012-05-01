#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# coding: utf-8 
# recite GRE words
# version: 0.01
# author: bing wang

import json
import time
import random
import os
import numpy as np

def initial():
    def blast(w1,w2):
        w_match = 2
        w_mismatch = -1
        w_gap = -1
        score_matrix = np.zeros((len(w1)+1,len(w2)+1))
        for i in range(len(w1)):
            for j in range(len(w2)):
                s = w_match if w1[i] == w2[j] else w_mismatch
                score_matrix[i+1,j+1] = max(0,score_matrix[i,j]+s,\
                                            score_matrix[i+1,j]+s+w_gap,\
                                            score_matrix[i,j+1]+s+w_gap)
        return score_matrix[len(w1),len(w2)]

    GRE_book = {}
    f = open(BOOK_PATH+"GRE.txt")
    for i,line in enumerate(f):
        line = line.strip()
        word = line[:line.find("[")-1]
        GRE_book[word] = {}
        GRE_book[word]["meaning"] = line[line.find("]")+2:]
        GRE_book[word]["recite_count"] = 0
        GRE_book[word]["remember_rate"] = 0.
        GRE_book[word]["last_recite_time"] = 0.
        GRE_book[word]["strength"] = 0
        GRE_book[word]["difficulty"] = 1.0
        GRE_book[word]["time_used"] = 0
        GRE_book[word]["group_words"] = []
        GRE_book["_total_time"] = 0.0
        GRE_book["_total_review_time"] = 0.0
        GRE_book["_total_new_time"] = 0.0
        group_words = [a for a in GRE_book if blast(a,word) > 7 and (a != word)]
        for a in group_words:
            if word not in GRE_book[a]["group_words"]:
                GRE_book[a]["group_words"].append(word)
            if a not in GRE_book[word]["group_words"]:
                GRE_book[word]["group_words"].append(a)
        print i*1.0/8395
    encode = json.dumps(GRE_book)
    f = open(BOOK_PATH+"GRE_book","w")
    f.write(encode)
    f.close()

def word_handle(word,stastus,t):
    GRE_book[word]["time_used"] += t
    GRE_book["_this_time"] += t
    if GRE_book[word]["recite_count"] == 0:
        GRE_book["_new_time"] += t
    elif GRE_book[word]["recite_count"] > 0:
        GRE_book["_review_time"] += t
    if GRE_book["_this_time"] - GRE_book["_auto_save"] > 60:
        if save():
            GRE_book["_auto_save"] = GRE_book["_this_time"]
            print "**auto saved**"
            time.sleep(1)

    if stastus == False:
        GRE_book[word]["difficulty"] += 1
    elif stastus == True:
        GRE_book[word]["recite_count"] += 1
        GRE_book[word]["strength"] += 0.5 
        GRE_book[word]["remember_rate"] = 1.0
        GRE_book[word]["last_recite_time"] = time.time()

def show_stastus():
    word_reviewed = len([word for word in reviewed if \
        GRE_book[word]["remember_rate"] > remember_threshold and \
        GRE_book[word]["strength"] % 1 == 0])
    word_newed = len([word for word in newed if \
        GRE_book[word]["remember_rate"] > remember_threshold])
    word_total = len([word for word in GRE_book if word[0] != "_" and \
        GRE_book[word]["remember_rate"] > remember_threshold])

    new_time = int(GRE_book["_new_time"])
    review_time = int(GRE_book["_review_time"])
    study_time = int(GRE_book["_this_time"] + GRE_book["_preview_time"])
    print "#########################"
    print "you sepend:\t\t",study_time/3600,"h",(study_time%3600)/60,"min"
    print "words reviewed:\t\t",word_reviewed,"words"
    print "review speed:\t\t",word_reviewed*1./((review_time+1)*1./3600),"words/h"
    print "review percentage\t\t",word_reviewed*1.0/(len(reviewed)+1)
    print "words newed:\t\t",word_newed,"words"
    print "new word speed:\t\t",word_newed*1.0/((new_time+1)*1./3600),"words/h"
    print "total percent:\t\t",round(word_total*100.0/len(GRE_book),2),"%"

def save():
    from datetime import date
    day = str(date.today().day)
    month = str(date.today().month)
    year = str(date.today().year)
    filetime = year + "_" + month + "_" + day
    encode = json.dumps(GRE_book)
    f = open(BOOK_PATH+"History/GRE_book_"+filetime,"w")
    f.write(encode)
    f.close()
    f = open(BOOK_PATH+"GRE_book","w")
    f.write(encode)
    f.close()
    return True

def recite(word,up = None):
    os.system("clear")
    if up:
        print (len(word) + 12)*"#"
        print "#    ",word.upper(),"    #"#,'\t',GRE_book[word]["remember_rate"]
        print (len(word) + 12)*"#"
    else:
        print (len(word) + 12)*"#"
        print "#    ",word,"    #",'\t',GRE_book[word]["remember_rate"]
        print (len(word) + 12)*"#"
    word_start = time.time()
    cmd = getch()

    if cmd.upper() == "N":
        print GRE_book[word]["meaning"]
        print "........................press any to continue"
        print "\nhttp://en.wiktionary.org/wiki/"+word+"#Etymology\n"
        if getch():
            word_time_used = int(time.time()-word_start)
            word_handle(word,False,word_time_used)
            return False

    elif cmd.upper() == "Y":
        word_time_used = int(time.time()-word_start)
        print GRE_book[word]["meaning"]
        print "........................press \"y\" if right"
        if getch().upper() == "Y":
            word_handle(word,True,word_time_used)
            return True
        else:
            print "........................press any to continue"
            print "\nhttp://en.wiktionary.org/wiki/"+word+"#Etymology\n"
            if getch():
                word_time_used = int(time.time()-word_start)
                word_handle(word,False,word_time_used)
                return False

    elif cmd.upper() == "X":
        GRE_book[word]["strength"] = 10
        return True

    elif cmd.upper() == "S":
        if save():
            print "saved!"
        print "press any to continue:"
        if getch():
            return None

    elif cmd.upper() == "P":
        show_stastus()
        print "press any to continue:"
        if getch():
            return None

    elif cmd.upper() == "Q":
        show_stastus()
        save()
        return "Q"

    else:
        print "#########################"
        print "y\t\t\tI remember"
        print "n\t\t\tI forget"
        print "h\t\t\tshow this message"
        print "p\t\t\tshow stastus"
        print "s\t\t\tsave"
        print "x\t\t\tnever appear again"
        print "q\t\t\tquit"
        print "press any to continue:"
        if getch():
            return None

def calculte_remember_rate():
    import math
    for word in GRE_book:
        if word[0] != "_" and GRE_book[word]["recite_count"] > 0:
            t = int((time.time()-GRE_book[word]["last_recite_time"])/60)*1.0/60
            GRE_book[word]["remember_rate"] = math.e ** \
            ((-t*GRE_book[word]["difficulty"])/(24*GRE_book[word]["strength"]))
        else:
            continue

def review(review_list):
    while True:
        for i,word in enumerate(review_list):
            if GRE_book[word]["remember_rate"] == 1:
                continue
            else:
                cmd = recite(word)
                if cmd == True:
                    continue
                elif cmd == "Q":
                    return "Q"
                while cmd == None:
                    cmd = recite(word)
        if len([word for word in review_list if GRE_book[word]["remember_rate"]<1])==0:
            break


    print "######################################"
    print "# OK! Let's do it UPPER and randomly #"
    print "######################################"
    random.shuffle(review_list)
    while True:
        for i,word in enumerate(review_list):
            if GRE_book[word]["strength"] % 1 == 0:
                continue
            else:
                cmd = recite(word,True)
                if cmd == True:
                    continue
                elif cmd == "Q":
                    return "Q"
                while cmd == None:
                    cmd = recite(word,True)
        if len([word for word in review_list if GRE_book[word]["strength"] % 1 != 0])==0:
            break

def preview(preview_list):
    count = len(preview_list)
    for word in preview_list:
        print word
        time.sleep(1)
        print GRE_book[word]["meaning"]
        time.sleep(1)
        print word
        time.sleep(1)
        print GRE_book[word]["meaning"]
        time.sleep(1)
    random.shuffle(preview_list)
    print "######################################"
    print "# OK! let's do it UPPER and randomly #"
    print "######################################"
    for word in preview_list:
        print word.upper()
        time.sleep(1)
        print GRE_book[word]["meaning"]
        time.sleep(1)
    print "#################"
    print "# Again ? (y/n) #"
    print "#################"
    if getch().upper() == "Y":
        return True
    else:
        return False

def check_redundance():
    for word in GRE_book:
        if word[0] != "_":
            for group in GRE_book[word]["group_words"]:
                if group == word:
                    GRE_book[word]["group_words"].remove(group)
                    print "remove\t",group,"\tfrom\t",word
                elif GRE_book[word]["group_words"].count(group) > 1:
                    GRE_book[word]["group_words"].remove(group)
                    print "remove\t",group,"\tfrom\t",word

def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

####################  main  ######################
BOOK_PATH = "/Users/bingwang/VimWork/GreWordReciter/"
remember_threshold = 0.6
unit_length = 20
review_unit_length = 40
f = open(BOOK_PATH+"GRE_book")
encode = f.read()
GRE_book = json.loads(encode)

print GRE_book["_total_time"]/3600,"h",(GRE_book["_total_time"]%3600)/60,"min"
print len([word for word in GRE_book if word[0] != "_" and GRE_book[word]["recite_count"]>0])

GRE_book["_this_time"] = 0
GRE_book["_auto_save"] = 0
GRE_book["_review_time"] = 0
GRE_book["_preview_time"] = 0
GRE_book["_new_time"] = 0
newed = []
reviewed = []
cmd = ""
while cmd != "Q":
    calculte_remember_rate()
    review_list = [word for word in GRE_book if word[0] != "_" \
                    and GRE_book[word]["recite_count"] > 0 \
                    and (GRE_book[word]["remember_rate"] < remember_threshold \
                     or GRE_book[word]["strength"]%1 != 0)]

    for word in review_list:
        if word not in reviewed:
            reviewed.append(word)
    
    if len(review_list) > 0:
        print "#############################"
        print "#         Reviewing         #"
        print "#############################"
        print "You have\t",len(review_list),"words to review."
        time.sleep(1)

        c = len(review_list) / review_unit_length
        if c == 0:
            cmd = review(review_list)
        else:
            for i in range(c):
                cmd = review(review_list[i*review_unit_length:(i+1)*review_unit_length])
                if cmd == "Q":
                    break
            if cmd == "Q":
                break
            cmd = review(review_list[(i+1)*review_unit_length:])

    if cmd == "Q":
        break

    temp_list = []
    stop_flag = False
    for word in GRE_book:
        if word[0] != "_" and GRE_book[word]["recite_count"] == 0:
            temp_list.append(word)
            newed.append(word)
            for group in GRE_book[word]["group_words"]:
                if GRE_book[group]["recite_count"] == 0 and group not in newed:
                    temp_list.append(group)
                    newed.append(group)
                    if len(temp_list) > unit_length:
                        stop_flag = True
                        print "#############################"
                        print "#         New Word          #"
                        print "#############################"

                        while preview(temp_list):
                            pass
                            GRE_book["_preview_time"] += len(temp_list) * 6
                        GRE_book["_preview_time"] += len(temp_list) * 6

                        print "#############################"
                        print "#           Ready           #"
                        print "#############################"
                        time.sleep(1)
                        print "#############################"
                        print "#           Go!!            #"
                        print "#############################"
                        cmd = review(temp_list)
                        if cmd == "Q":
                            break
                        break
            if stop_flag:
                break

GRE_book["_total_time"] += GRE_book["_this_time"] + GRE_book["_preview_time"]
GRE_book["_total_review_time"] += GRE_book["_review_time"]
GRE_book["_total_new_time"] += GRE_book["_new_time"]
if save():
    print "saved"

