
'''
Construct and return a Schedule CSP model.
'''

from cspbase import *
from propagators import *
import file_parser
import math
import itertools
FILE  = "sample_data/Prof-Sample.csv"
FILE2 = "sample_data/Location-Sample.csv"
FILE3 = "sample_data/Student-Sample.csv"
FILE4 = "sample_data/Distance-Sample.csv"
def schedule_csp_model(profs, students, time_frame):
    '''
    profs - dictionary
    students - dictionary
    time_frame - tuple
    '''
        
    # CREATE THE VARIABLES    
    var_array = []    
    for student in students:
        
        availabilities = students[student][1]
        
        # create the domain of each student
        dom = []
        for start,finish in availabilities:
            dom.extend(list(range(start,finish,1)))     
            
        # create the variable for student.prof
        for prof in students[student][0]:
            
            # restrict the domain given the prof availability
            final_dom = set(dom)
            prof_avail = set()
            for start,finish in profs[prof]:
                prof_avail.update(list(range(start,finish,1))) 

            # the intersection of availabilities
            final_dom = final_dom & set(prof_avail)
            
            # probably want to do something else then exiting
            if len(final_dom) == 0:
                print("{} can never meet {}!".format(student,prof))
                exit()
            
            name = '{}.{}'.format(student, prof)
            var_array.append(Variable(name,prof,list(final_dom)))
            
    
    constraints = []
    
    # CREATE THE CONSTRAINTS [(1) - MUTUAL EXCLUSIVE TIME FOR EACH PROF]   
    
    # contruct the binary constraint of each student pair
    for i,student in enumerate(var_array):
        for student2 in var_array[i+1:]:
            if student.prof_name == student2.prof_name:
                
                # construct the tuples for the constraint
                sat_tuples = []
                for v1,v2 in itertools.product(student.dom,student2.dom):
                    if v1 != v2:
                        sat_tuples.append((v1,v2))                 
                
                # construct the constraint
                name = "time_diff({},{})".format(student.name,student2.name)
                con = Constraint(name, [student, student2])
                con.add_satisfying_tuples(sat_tuples)
                constraints.append(con)       
    
    
    
    # CONSTRUCT THE SCHEDULING CSP
    schedule_csp = CSP("SCHEDULE")
    for var in var_array:
        schedule_csp.add_var(var)
    for con in constraints:
        schedule_csp.add_constraint(con)
        
        
    return schedule_csp,var_array

def get_travel_time(loc1,loc2,distance):
    d = distance[(loc1,loc2)]
    if d < 800:
        return 0
    else:
        return math.ceil(d/15000)
    

def print_soln(var_array):
    for var in var_array:
        start = var.get_assigned_value()        
        end = start + 1
        
        if start > 12: start = "{}pm".format(start - 12) 
        else: start = "{}am".format(start)
        
        if end > 12: end = "{}pm".format(end - 12) 
        else: end = "{}am".format(end)  
        
        print("{} = {} to {}".format(var,start,end))



if __name__ == '__main__':
    
    # 0 to 24 hours
    time_frame = (0, 24)
    
    
    # availability of profs
    """
    profs = { 'prof1':[(0,2),(4,8)],
              'prof2':[(7,10),(11,14),(15,16)],
              'prof3':[(6,10),(15,17),(20,22)] }
    """
    profs = file_parser.read_avail(FILE)
    
    all_profs = list(profs.keys())
    
    # preferred prof and availability of students
    """
    students = { 'student1':[['prof1'],          [time_frame]],
                 'student2':[['prof2'],          [(0,10),(10,2)]],
                 'student3':[['prof2','prof3'],  [time_frame]],
                 'student4':[['prof1','prof3'],  [(5,10),(20,24)]],
                 'student5':[all_profs        ,  [time_frame]]        }
     
    """
    students = file_parser.read_student(FILE3)
    
    """
    distance = { ('M5G 0A4', 'M5S 1A8'): 1200.0,
                 ('M5S 1A8', 'M5S 3E1'): 300.0,
                 ('M5S 3E1', 'M5S 3E1'): 1.0,
                 ('M5G 0A4', 'M5S 3E1'): 1000.0  }

    """
    distance = file_parser.read_distance(FILE4)
    
    """
    locations = { 'Prof B': ['M5S 3E1'],
                  'Prof J': ['M5S 1A8'],
                  'Prof H': ['M5S 1A8'], 
                  'Prof D': ['M5G 0A4'] }
    """
    locations = file_parser.read_location(FILE2)
    
    csp,var_array = schedule_csp_model(profs, students, time_frame)
    
    solver = BT(csp)
    print()
    print("======GAC=====")
    solver.bt_search(prop_GAC)
    
    print()
    print("=====Solution=====")
    print_soln(var_array)