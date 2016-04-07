
'''
Construct and return a Schedule CSP model.
'''

from cspbase import *
import math
import itertools

def schedule_csp_model(profs, students, time_frame):
    '''
    return a csp object of the schedule problem, a list of variables.


    profs - dictionary  
              key:  prof name; 
            value:  availability of the prof;

    students - dictionary
              key:  student name;
         value[0]:  student preferred prof name;
         value[1]:  availability of the student;

    time_frame - tuple
              (0, 24)

    '''
        
    # CREATE THE VARIABLES    
    var_array = []    
    for student in students:
        
        availabilities = students[student][1]
        
        # create the domain of each student
        # free time of the student will be saved, time is separated by 1 hour.
        dom = []
        for start,finish in availabilities:
            dom.extend(list(range(start,finish,1)))     
            
        # create the variable for student.prof
        for prof in students[student][0]:
            
            # restrict the domain given the prof availability
            final_dom = set(dom)
            prof_avail = set()

            # time availability for each prof preferred by the student
            for start,finish in profs[prof]:
                prof_avail.update(list(range(start,finish,1))) 

            # the intersection of availabilities between the prof and the student
            final_dom = final_dom & set(prof_avail)
            
            # probably want to do something else then exiting
            if len(final_dom) == 0:
                print("{} can never meet {}!".format(student,prof))
                exit()
            
            name = '{}.{}'.format(student, prof)
            var_array.append(Variable(name,student,prof,list(final_dom)))
            
    
    constraints = []
    
    # CREATE THE CONSTRAINTS [(1) - PROF CAN ONLY MEET 1 STUDENT PER HOUR]
    
    # construct the binary constraint of each student pair
    for i,student in enumerate(var_array):
        for student2 in var_array[i+1:]:
            if student.prof_name == student2.prof_name:
                
                # construct the tuples for the constraint
                sat_tuples = []
                for v1,v2 in itertools.product(student.dom,student2.dom):
                    if v1 != v2:
                        sat_tuples.append((v1,v2))                 
                
                # construct the constraint
                name = "prof_diff({},{})".format(student.name,student2.name)
                con = Constraint(name, [student, student2])
                con.add_satisfying_tuples(sat_tuples)
                constraints.append(con)       
    
    
    # CREATE THE CONSTRAINTS [(2) - STUDENT CAN ONLY MEET 1 PROF PER HOUR]
    for i,student in enumerate(var_array):
        for student2 in var_array[i+1:]:
            if student.stud_name == student2.stud_name:
                
                # construct the tuples for the constraint
                sat_tuples = []
                for v1,v2 in itertools.product(student.dom,student2.dom):
                    if v1 != v2:
                        sat_tuples.append((v1,v2))                 
                
                # construct the constraint
                name = "student_diff({},{})".format(student.name,student2.name)
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

def get_commute_time(prof1,prof2):
    global locations
    global distance
    prof1_loc = locations[prof1][0]
    prof2_loc = locations[prof2][0]
    d = distance[(prof1_loc,prof2_loc)]
    print(d)
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


def print_table(var_array):
    print(len(var_array))
    print("         | 9am to 10am | 10am to 11am | 11am to 12pm | \
12pm to  1pm | 1pm to 2pm | 2pm to 3pm | 3pm to 4pm | 4pm to 5pm |")
    p = set()
    for v in var_array:
        p.add(v.prof_name)
    
    for n in p:
        print(n)
