
'''
Construct and return a Schedule CSP model.
'''

from cspbase import *
import itertools

def schedule_csp_model(profs, students, time_frame):
    '''
    profs - dictionary
    students - dictionary
    time_frame - tuple
    '''
    
    # CREATE THE DOMAIN    
    dom = []
    for hour in range(time_frame[0], time_frame[1], 1):
        dom.append(hour)
    
    
    # CREATE THE VARIABLES    
    var_array = []    
    for student in students:
        for prof in students[student][0]:
            name = '{}.{}'.format(student, prof)
            var_array.append(Variable(name,prof,dom))
            
    
    constraints = []
    
    # CREATE THE CONSTRAINTS [(1) - MUTUAL EXCLUSIVE TIME FOR EACH PROF]
    
    # construct the tuples for the constraint
    sat_tuples = []
    for t in itertools.combinations(dom,dom):
        sat_tuples.append(t)    
    
    # contruct the binary constraint of each student pair
    for i,student in enumerate(var_array):
        for j,student2 in enumerate(var_array[i:]):
            if student.prof_name == student2.prof_name:
                
                # construct the constraint
                name = "time_diff({},{})".format(student.name,student2.name)
                con = Constraint(name, [student, student2])
                con.add_satisfying_tuples(sat_tuples)
                constraints.append(con)
                
    
    # CREATE THE CONSTRAINTS [(2) - student.prof time == prof.avail]
    
    
    
    
    
    
if __name__ == '__main__':
    
    # 0 to 24 hours
    time_frame = (0, 24)
    
    
    # availability of profs
    profs = { 'prof1':[(0,2),(4,8)],
              'prof2':[(7,10),(11,14),(15,16)],
              'prof3':[(6,10),(15,17),(20,22)] }
    
    all_profs = tuple(profs.keys())
    
    # preferred prof and availability of students
    students = { 'student1':[('prof1'),          [time_frame]],
                 'student2':[('prof2'),          [(0,10),(10,2)]],
                 'student3':[('prof2','prof3'),  [time_frame]],
                 'student4':[('prof1','prof3'),  [(5,10),(20,24)]],
                 'student5':[all_profs        ,  [time_frame]]        }
     
    
    schedule_csp_model(profs, students, time_frame)