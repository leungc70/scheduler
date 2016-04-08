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
    time_frame = None
    profs = None
    all_profs = None
    students = None

    while not time_frame:
        # Setting up the time fram
        print()
        print("Please setup the running environment...")
        print("Please Choose the time fram...")
        print("Choice: 12, 24")

        input_tf = input()

        if input_tf == "12":
            # 0 to 12 hours
            time_frame = (0, 12)
        elif input_tf == "24":
            # 0 to 24 hours
            time_frame = (0, 24)
        else:
            print()
            print("======ERROR=====")
            print("ERROR: Your input is not valid.")

    """
    format of profs
    profs = { 'prof1':[(0,2),(4,8)],
              'prof2':[(7,10),(11,14),(15,16)],
              'prof3':[(6,10),(15,17),(20,22)] }
    """
    while not all_profs:
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

        if profs:
            all_profs = list(profs.keys())


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
            print("FILE {} is not found".format(prof_file))

    print()
    print("======SUCCESS=====")
    print("Reading student's availabilities success...")

    # construct the interview scheduling CSP
    csp, var_array = schedule_csp_model(profs, students, time_frame)
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