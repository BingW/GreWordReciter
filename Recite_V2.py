# coding: utf-8
# version: 0.01
# author: bing wang

import json
import time
import random
import os
import numpy as np

def initial():
    GRE_book = {}
    GRE_book["_total_time"] = 0.0
    for first_letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        GRE_book["_"+first_letter] = []
    f = open(BOOK_PATH+"GRE.txt")
    for i,line in enumerate(f):
        line = line.strip()
        word = line[:line.find("[")-1]
        first_letter = word[0].upper()
        GRE_book[word] = {}
        GRE_book[word]["meaning"] = line[line.find("]")+2:]
        GRE_book[word]["recite_count"] = 0
        GRE_book[word]["remember_rate"] = 0.
        GRE_book[word]["last_recite_time"] = 0.
        GRE_book[word]["strength"] = 0
        GRE_book[word]["difficulty"] = 1.0
        GRE_book[word]["time_used"] = 0
        GRE_book["_"+first_letter].append(word)
    encode = json.dumps(GRE_book)
    f = open(BOOK_PATH+"GRE_book_V2","w")
    f.write(encode)
    f.close()

def recite(word,up = None):
    #return value = {True, False, None, "Q"}
    #True means remember
    #False means forget
    #None means continue
    #Q means quit
    os.system("clear")
    if up:
        print (len(word) + 12)*"#"
        print "#    ",word.upper(),"    #"#,'\t',GRE_book[word]["remember_rate"]
        print (len(word) + 12)*"#"
    else:
        print (len(word) + 12)*"#"
        print "#    ",word,"    #"#,'\t',GRE_book[word]["remember_rate"]
        print (lens(word) + 12)*"#"
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
        print "q\t\t\tquit"
        print "press any to continue:"
        if getch():
            return None

def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
#TODO
def show_stastus():
    pass

#main
BOOK_PATH = "/Users/bingwang/VimWork/GreWordReciter/"
unit_length = 30
total_words_num = 8395

letter_rank = "ZYXQJKUVWNOLFGITHMBDERCPSA"

f = open(BOOK_PATH+"GRE_book_V2")
encode = f.read()
GRE_book = json.loads(encode)

for first_letter in letter_rank:
    for word in GRE_book["_"+first_letter]:
        if GRE_book[word]["recite_count"] == 0:
            for i in xrange(unit_length):


        
