
'''
Run this file to test schedule_csp.py
'''

from schedule_csp import schedule_csp_model, print_soln, print_table
import file_parser
import cspbase
import propagators

FILE  = "sample_data/Prof-Sample.csv"
FILE2 = "sample_data/Location-Sample.csv"
FILE3 = "sample_data/Student-Sample.csv"
FILE4 = "sample_data/Distance-Sample.csv"
#distance = {}
#locaitons = {}

'''
Interactive test mode
'''
if __name__ == '__main__':
    # print status in the console
    print("Setting up variables...")

    # 0 to 24 hours
    time_frame = (0, 24)

    print("Reading sample data files...")
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

    csp, var_array = schedule_csp_model(profs, students, time_frame, locations, distance)
    solver = cspbase.BT(csp)

    # Menue
    while(1):
        print()
        print("Please choose which propagator you'd like to use?")
        print("Choices: BT, FT, GAC")

        propa = input()

        if propa == "GAC":
            print()
            print("======GAC=====")
            solver.bt_search(propagators.prop_GAC)
        elif propa == "FC":
            print()
            print("=======FC======")
            solver.bt_search(propagators.prop_FC)
        elif propa == "BT":
            print()
            print("======BT=====")
            solver.bt_search(propagators.prop_BT)
        else:
            print()
            print("======ERROR=====")
            print("ERROR: Your input is not valid.")
            print("NOTE: Please choose from BT, FC or GAC")
            continue

        print()
        print("=====Solution=====")
        print_soln(var_array)
        print_table(var_array)