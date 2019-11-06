from bs4 import BeautifulSoup
import urllib2
import os
import json
import random
import time
import sys

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def main():

    WORKDIR = sys.argv[1]

    dic = open(WORKDIR + "/dictionary.wl", 'r') #Path of the used dictionary
    dick = dic.readlines()

    impossibility =  random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                                    2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
                                    4, 4, 4, 4, 1, 1, 1, 1, 1, 2])


    words = random.sample(dick, impossibility)

    query = ('+'.join(words)).replace("\n", '')
    image_type = (query.replace("'",'')).replace("+", '_')  #Name of the picture files
    url= "https://www.google.co.uk/search?q=" + query +\
         "&source=lnms&tbm=isch#q=" + query + "&tbs=isz:lt,islt:2mp&tbm=isch"


    #add the directory for your image here
    DIR= WORKDIR + "/backgrounds" #Directory for the pictures


    #Decides which image to take
    number = random.randrange(100)

    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    soup = get_soup(url,header)


    ActualImages=[]# contains the link for Large original images, type of  image
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImages.append((link,Type))


    ###print images
    for i , (img , Type) in enumerate( [ActualImages[number]]):
        try:
            req = urllib2.Request(img, headers={'User-Agent' : header})
            raw_img = urllib2.urlopen(req).read()

            cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1

            picpath = DIR + '/' + image_type + "_" + str(number)

            if len(Type)==0:
                picpath += ".jpg"
            else:
                picpath +=  "." + Type

            f = open(picpath, 'wb')
            f.write(raw_img)
            f.close()
        except Exception as e:
            print("could not load : "+img)
            print(e)



    # Create temporary file which stores the picture path
    f = open(WORKDIR + "/tempfile.wl", 'w')
    f.write(picpath)
    f.close()

main()
