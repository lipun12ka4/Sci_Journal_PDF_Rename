#!/usr/bin/env python
'''
Created on Sep 28, 2013

@author: dataq <http://stackoverflow.com/users/2585246/dataq>

This is a simple code to rename the paper based on the ORIGINAL FILENAME and their website.
Your are free to use this code, but don't blame me for the error.
I am not writing any documentation, so please read my mind in this code.
USE ON YOUR OWN RISK *evil smirk*
'''
import urllib.request, urllib.error, urllib.parse, re, time, random
from os import listdir, rename
from os.path import isfile, join
from bs4 import BeautifulSoup
import mechanicalsoup
import sys

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='MyBot/0.1: mysite.example.com/bot_info',
)

# Define Raw String Function
escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}


def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string


# for every publisher we have different way of scraping
IEEE = 1
SCIENCEDIRECT = 2

# yes, I know, this very bad and stupid web scraping. But it's work at least.

# get title for IEEE paper
# the IEEE paper filename is looks like this '06089032.pdf'
def getIEEETitle(fname):
    # get url
    number = int(fname.split('.')[0])
    targeturl = 'http://ieeexplore.ieee.org/document/'+str(number)
    # open and read from those url
    browser.open(targeturl)
    # print(browser.get_current_page().find_all('title'))
    title = browser.get_current_page().title.string
    print(title)
    return title.strip()[:150]

# get title for Science Direct paper
# the Science Direct paper filename is looks like this '1-s2.0-0031320375900217-main.pdf'
def getScienceDirectTittle(fname):
    # get url
    number = fname.split('-')[2]
    targeturl = 'http://www.sciencedirect.com/science/article/pii/'+number
    # open and read from those url
    browser.open(targeturl)
    title = browser.get_current_page().title.string
    print(title)
    return title.strip()[:150]

def batchRename(workingdir, site):
    # list all file in working directory
    files = [ fInput for fInput in listdir(workingdir) if isfile(join(workingdir,fInput)) ]
    # compiled regular expression for illegal filename character
    reIlegalChar = re.compile(r'([<>:"/\\|?*])')
    # rename all files
    for f in files:
        try:
            # find title
            if site == IEEE:
                title = getIEEETitle(f)
            elif site == SCIENCEDIRECT:
                title = getScienceDirectTittle(f)
            else:
                title = None

            if title:
                # remove illegal file name character
                fnew = reIlegalChar.sub(r' ', title) + '.pdf'
                print('{} --> {}'.format(f, fnew))
                # rename file
                rename((workingdir + f), (workingdir + fnew))
                print('Success')
            else:
                print('{}\nFailed'.format(f))
        except:
            print('{}\nERROR'.format(f))
        # give some random delay, so we will not be blocked (hopefully) :p
        time.sleep(random.randrange(10))

if __name__ == '__main__':
    print('Please be patient, it takes time depending on your internet connection speed...')
    working_dir = input("Please enter the path of the directory which contains the PDF Articles \n"
                        "Copy the folder path from Windows Explorer : ")
    # working_dir = 'C:\\Codes\\PycharmProjects\\Scraps\\PDF_Titles\\PDFs_bc\\'
    working_dir = raw(working_dir)+"\\"
    site = int(input("Please Enter type of Articles, i.e. 1 for IEEE or 2 for SCIENCEDIRECT : "))
    batchRename(working_dir, site)

