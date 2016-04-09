'''
Interactive running mode
'''

from schedule_csp import schedule_csp_model, print_soln
from os import listdir
import file_parser
import cspbase
import propagators


'''
Helper function to list all .csv files under the directory

 @param dir the directory of choice
 return: returns nothing
'''
def list_all_csvfiles(dir):
    flist = listdir(dir)

    print()
    print("Possible choice of .csv files under dir {}:".format(dir))
    # list all files under dir that with extension .csv
    for file in flist:
        if file.endswith(".csv"):
            print(file)


'''
Interactive running mode

Instruction:
    Please put files in the correct directory:
        student files in data/students/
        profs files in data/profs/
    Follow the message displayed in the console.

    After setting environment success, type 'exit' to exit
    Press ctrl + c any time to exit
'''
if __name__ == '__main__':
    # define variables
    profs = None
    students = None
    distance = None
    locations = None

    """
    format of profs
    profs = { 'prof1':[(0,2),(4,8)],
              'prof2':[(7,10),(11,14),(15,16)],
              'prof3':[(6,10),(15,17),(20,22)] }
    """
    while not profs:
        # availability of profs
        print()
        print("Readding professor's availabilities...")
        print("Please specify which file to read...")
        print("Please choose a file from data/profs/")

        # list .csv files under data/profs/
        prof_dir = "data/profs/"
        list_all_csvfiles(prof_dir)

        prof_input_fname = input()
        prof_file = prof_dir + prof_input_fname

        print("Reading from FILE {}...".format(prof_file))

        try:
            profs = file_parser.read_avail(prof_file)
        except FileNotFoundError as e:
            print()
            print("======ERROR=====")
            print("FILE {} is not found".format(prof_file))


    # message on console
    print()
    print("======SUCCESS=====")
    print("Reading professor's availabilities success...")


    """
    students = { 'student1':[['prof1'],          [time_frame]],
                 'student2':[['prof2'],          [(0,10),(10,2)]],
                 'student3':[['prof2','prof3'],  [time_frame]],
                 'student4':[['prof1','prof3'],  [(5,10),(20,24)]],
                 'student5':[all_profs        ,  [time_frame]]        }

    """
    while not students:
        # preferred prof and availability of students
        print()
        print("Readding student's availabilities...")
        print("Please specify which file to read...")
        print("Please choose a file from /data/students/")

        # list .csv files under data/profs/
        student_dir = "data/students/"
        list_all_csvfiles(student_dir)

        student_input_fname = input()
        student_file = student_dir + student_input_fname

        print("Reading from FILE {}...".format(student_file))
        try:
            students = file_parser.read_student(student_file)
        except FileNotFoundError as e:
            print()
            print("======ERROR=====")
            print("FILE {} is not found".format(student_file))

    print()
    print("======SUCCESS=====")
    print("Reading student's availabilities success...")


    """
        distance = { ('M5G 0A4', 'M5S 1A8'): 1200.0,
                     ('M5S 1A8', 'M5S 3E1'): 300.0,
                     ('M5S 3E1', 'M5S 3E1'): 1.0,
                     ('M5G 0A4', 'M5S 3E1'): 1000.0  }

    """
    while not distance:
        print()
        print("Readding distance...")
        print("Please specify which file to read...")
        print("Please choose a file from /data/distance/")

        distance_dir = "data/distance/"
        list_all_csvfiles(distance_dir)

        distance_input_fname = input()
        distance_file = distance_dir + distance_input_fname

        print("Reading from FILE {}...".format(distance_file))
        try:
            distance = file_parser.read_distance(distance_file)
        except FileNotFoundError as e:
            print()
            print("======ERROR=====")
            print("FILE {} is not found".format(distance_file))

    print()
    print("======SUCCESS=====")
    print("Reading distance success...")

    """
    locations = { 'Prof B': ['M5S 3E1'],
                  'Prof J': ['M5S 1A8'],
                  'Prof H': ['M5S 1A8'],
                  'Prof D': ['M5G 0A4'] }
    """
    while not locations:
        print()
        print("Readding location of the professors...")
        print("Please specify which file to read...")
        print("Please choose a file from /data/locations/")

        locations_dir = "data/locations/"
        list_all_csvfiles(locations_dir)

        locations_input_fname = input()
        locations_file = locations_dir + locations_input_fname

        print("Reading from FILE {}...".format(locations_file))
        try:
            locations = file_parser.read_location(locations_file)
        except FileNotFoundError as e:
            print()
            print("======ERROR=====")
            print("FILE {} is not found".format(locations_file))

    print()
    print("======SUCCESS=====")
    print("Reading locations success...")


    # construct the interview scheduling CSP
    csp, var_array = schedule_csp_model(profs, students, locations, distance)
    solver = cspbase.BT(csp)

    # Menue
    while(1):
        print()
        print("Running environment setup success...")
        print("Please choose which propagator you'd like to use?")
        print("Choices: BT, FC, GAC")

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
        elif propa == "exit":
            print()
            print("Exiting...")
            break
        else:
            print()
            print("======ERROR=====")
            print("ERROR: Your input is not valid.")
            print("NOTE: Please choose from BT, FC or GAC")
            continue

        print()
        print("=====Solution=====")
        print_soln(var_array)