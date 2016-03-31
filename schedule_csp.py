
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
    
    
    