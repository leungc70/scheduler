import csv

FILE = "sample_data\Prof-Sample.csv"

def read(file):
    """ file -> dict
    Reading a csv file and parse into an pyhton dictionary
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

def print_avail(availability):
    for i in availability:
        print(i ,end=": ")
        print (availability[i]) 
    
if __name__ == "__main__": 
    d = read(FILE)
    print_avail(d)