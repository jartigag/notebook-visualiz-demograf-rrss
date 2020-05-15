import requests
import csv
import sys
import re

## GET RAW TEXT ##
#raw_text = requests.get("https://www.briansolis.com/2009/10/revealing-the-people-defining-social-networks/", headers={'User-Agent': 'anything, who cares'}).text
raw_text = open('raw_text').read()
lines = raw_text.splitlines()

## GET CATEGORIES ##
sites = [l.split('logo')[0].split('/')[-1][:-1].lower() for l in lines if '2009/10' in l and 'logo' in l and not 'script' in l]
sites.append('youtube')

## GET DATA OF INTEREST ##
# default value: '-'
visitors_us = ['-']*len(sites)
visitors_world = ['-']*len(sites)
visits_us = ['-']*len(sites)
visits_world = ['-']*len(sites)
edu_categs = ['no college','college', 'grad. school']
education = {categ: ['-']*len(sites) for categ in edu_categs }
no_children = ['-']*len(sites)

def engineeringNotation2int(num):
    if num[-1]=="B": return int(float(num[:-1])*1000000000)
    if num[-1]=="M": return int(float(num[:-1])*1000000)
    if num[-1]=="K": return int((float(num[:-1])*1000))

def percent(html_line):
    line = re.sub(re.compile('<.*?>'), '', html_line)
    return int(line.split()[-1][:-1])

i=-1

for n,l in enumerate(lines):
    if 'Visitors' in l:
        i+=1
        l = l.replace("&#8211;","") # bad char
        line_visitors = [ engineeringNotation2int(word) for word in re.findall("\d+\.*\d*\ ?\w", l) ]
        if len(line_visitors)==2:
            visitors_us[i] =  line_visitors[0]
            visitors_world[i] = line_visitors[1]
        else:
            visitors_world[i] = line_visitors[0]
    elif 'total visits' in l.lower():
        line_visits = [ engineeringNotation2int(word) for word in re.findall("\d+\.*\d*\ ?\w", l) ]
        if len(line_visits)==2:
            visits_us[i] = line_visits[0]
            visits_world[i] = line_visits[1]
        else:
            visits_world[i] = line_visits[0]
    elif 'Education' in l:
        if 'no college' in lines[n+1].lower():
            a,b,c = [lines[n+x] for x in range(1,4)]
            education['no college'][i] = percent(a)
            education['college'][i] = percent(b)
            education['grad. school'][i] = percent(c)
        elif 'less than hs diploma' in lines[n+1].lower():
            a,b,c,d,e = [lines[n+x] for x in range(1,6)]
            education['no college'][i] = percent(a) + percent(b)
            education['college'][i] = percent(c) + percent(d)
            education['grad. school'][i] = percent(e)
    elif 'Children in Household' in l:
        no = lines[n+2]
        no_children[i] = percent(no)

#f = sys.stdout
f = open("data.csv","w")
writer = csv.writer(f, lineterminator="\n")
writer.writerow(sites)
writer.writerow(visitors_us)
writer.writerow(visitors_world)
writer.writerow(visits_us)
writer.writerow(visits_world)
for categ in education: writer.writerow(education[categ])
writer.writerow(no_children)
