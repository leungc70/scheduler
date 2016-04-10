
'''
Construct and return a Schedule CSP model.
'''

from cspbase import *
import math
import itertools

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
def schedule_csp_model(profs, students, time_frame, locations, distance):

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
                
                
    # CREATE THE CONSTRAINTS [(3) - STUDENT TRAVEL TIME BETWEEN PROFS]        
    for i,student in enumerate(var_array):
        for student2 in var_array[i+1:]:
            if student.stud_name == student2.stud_name:  
                
                # the commute time in hours
                c_time = get_commute_time(student.prof_name, student2.prof_name, locations, distance)
                c_time = c_time + 1
                
                # construct the tuples for the constraint
                sat_tuples = []
                for v1,v2 in itertools.product(student.dom,student2.dom):
                    if abs(v1 - v2) >= c_time:
                        sat_tuples.append((v1,v2))
                        
                # construct the constraint
                name = "travel({},{})".format(student.name,student2.name)
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


'''
Calculate the travle time between the locations of two professors

@param  prof1 professor
        prof2 professor
        locations locations read from locations file
        distance  distance read from distance file

return  time it takes to travel between prof1 and prof2
'''
def get_commute_time(prof1,prof2,locations,distance):
    prof1_loc = locations[prof1][0]
    prof2_loc = locations[prof2][0]
    d = distance[(prof1_loc,prof2_loc)]

    # distance is short enough
    if d < 800:
        return 0
    else:
        # 15000m is the regular walking distance.
        return math.ceil(d/15000)
    

'''
Print the solution in a nicer format.

(Student C is assigned to see Prof D at 12am to 1pm)
example: Var--Student C.Prof D = 12am to 1pm

'''
def print_soln(var_array):

    for var in var_array:
        start = var.get_assigned_value()    
        if not start:
            print("No Solution Found") 
            return

        end = start + 1
        
        if start > 12: start = "{}pm".format(start - 12)
        elif start == 12: start = "{}pm".format(start)
        else: start = "{}am".format(start)
        
        if end > 12: end = "{}pm".format(end - 12)
        elif end == 12: end = "{}pm".format(end)
        else: end = "{}am".format(end)  

        print("{} = {} to {}".format(var,start,end))


'''
Print the schedule with the solution of each student has been assigned to
    see his preferred professor in both his and the professor's free time.
'''
def print_table(var_array):
    #print(len(var_array))
    #print("\t\t| 9am to 10am |\t10am to 11am\t|\t11am to 12pm\t| \t12pm to  1pm\t|\t1pm to  2pm\t|\t2pm to  3pm\t|\t3pm to  4pm\t|\t4pm to  5pm\t|")
    print('\t\t|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}'.format\
          ('9am to 10am','10am to 11am','11am to 12pm','12pm to  1pm',\
                  '1pm to  2pm','2pm to  3pm','3pm to  4pm','4pm to  5pm'))
    print("-"*190)  #printing the header
    profs = set()
    for v in var_array:
        profs.add(v.prof_name)
    d = [" "+"-"*18+" "]      #print dash for empty slot
    s = [" "*20              ]#print space for empty slot
    time_slot = dict()
    for prof in profs:
        time_slot[prof] = s * 8
    
    map_time = { i+9:i for i in range(8)}
    for v in var_array:                          #filling up the table
        name = v.prof_name
        value = v.get_assigned_value()
        display_name = '{:^20.20}'.format(v.stud_name)
        time_slot[name][map_time[value]]= display_name
        
    for prof in sorted(profs) :
        print('{:<15.15}'.format(prof),end=" :")        #printing the table
        for t in time_slot[prof]:
            print(t,end="|")
 
        print()