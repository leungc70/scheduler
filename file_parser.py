import csv
import googlemaps
import json
import time
from datetime import datetime
FILE  = "sample_data\Prof-Sample.csv"
FILE2 = "sample_data\Location-Sample.csv"
FILE3 = "sample_data\Student-Sample.csv"
gmaps = googlemaps.Client(key='AIzaSyA8vRIsxHzhbY113NJpQqomQmBVd6zLswE')

def read_avail(file):
    """ file -> dict
    Reading a  csv file and parse into an pyhton dictionary
    """
    f = open(file, 'rt')
    reader = csv.reader(f)
    next(reader)        #skipping unrelated rows
    next(reader)
    next(reader)
    next(reader)
    next(reader)
    time = next(reader)
    avail = dict()
    for row in reader: #parsing
        avail[row[0]] = [formatTime(time[i])for i in range(len(row)) if row[i] == 'OK']
        #print(row)
    del avail['Count']


    #print_avail(avail)
   
    f.close()
    
    return avail

def read_location(file):
    f = open(file,'rt')
    reader = csv.reader(f)
    location = dict()
    for row in reader:
        location[row[0]] = row[1:]
    f.close()
    

    return distance(location)

def distance(location):
    
    l =  {location[loc][0] for loc in location}
    dist = dict.fromkeys(l,list(l))
    
    t= dict(dist)
    for key in t:
        temp = []
        for loc in t[key]: 
            temp.append(gmaps.directions(key, loc,mode="walking")[0]['legs'][0]['distance']['text'])
        t[key] = temp
    return t

def formatTime(time):
    """     str -> tuple
    convert a time string into a tuple with (s,e)
    s : the starting time
    e : the ending time
    """
    
    time  = time.split()
    start = int(time[0][:time[0].index(":")])
    end   = int(time[3][:time[3].index(":")])
    
    if time[1] == 'PM':
        if start != 12:
            start += 12
        end += 12    
        
    return (start,end)

def read_student(file):
    f = open(file,'rt')
    reader = csv.reader(f)
    student = dict()
    for row in reader:
        student[row[0]] = [row[1:],[(9,17)]]
    f.close()
    

    return student
     
def print_avail(availability):
    for i in availability:
        print(i ,end=": ")
        print (availability[i]) 

    
if __name__ == "__main__": 
    stime = time.process_time()
    d = read_avail(FILE)
    l = read_location(FILE2)
    s = read_student(FILE3)
    print("Setup Time = {}".format(time.process_time()-stime))
    #o = distance(l)
    #print_avail(o)
    print_avail(s)

    # Replace the API key below with a valid API key.
    '''
    stime = time.process_time()
    
    # Geocoding and address
    geocode_result = gmaps.geocode('1121 Bay Street, Toronto,Ontario, Canada')
    
    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
    
    # Request directions 
    directions_result = gmaps.directions("M4L 1Y5",
                                         "M5S 2E4",
                                         mode="walking")
    print("Setup Time = {}".format(time.process_time()-stime))
    print(json.dumps(directions_result, sort_keys=True, indent=4))
    '''

