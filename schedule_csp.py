
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
    
    VAR_TIME_SIZE = 0.5
    
    
    # CREATE THE VARIABLES
    var_array = []
    # create the vars
    # number of vars = sum( each student * student.profs )
    # the domain is the potential time to meet prof. this shud be within time_frame
    
    
    # CREATE THE CONSTRAINTS 1
    # prof avail == student avail
    
    # CREATE THE CONSTRAINTS 2
    
    
    
    
    
    
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
     
    
    pass