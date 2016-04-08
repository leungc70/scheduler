'''
Generate samples that are solvable for the scheduler
'''

import csv
import random
from file_parser import read_distance

########################################################
# ULTIMATE SOLVABLE TEST INPUT GENERATOR               #
########################################################

'''
represent a professor
'''
class Prof:
    def __init__(self, name, location):
        self.name = name

        # the availability of the prof
        self.schedule = [random.randrange(0,2) for i in range(0,8)]
        self.location = location


'''
represent a student
'''
class Student:
    def __init__(self, name):
        self.name = name

        # the student is always available
        self.schedule = [1 for i in range(0,8)]
        self.interviewed_profs = list()


'''
Read a .cvs file and return a list of its values
Used to read locations and names

file -> [str]
'''
def list_value_of_file(file):

    f = open(file, 'rt')
    reader = csv.reader(f)
    results = [row for row in reader]

    return results


'''
Generate nprofs of random professors

int -> [Prof]
'''
def random_profs_generator(nprofs, location_file, name_file):
    locations = list_value_of_file(location_file)

    # a list of unique random names
    names = random.sample(list_value_of_file(name_file), nprofs)
    prof_list = list()

    for i in range(0, nprofs):
        name = names.pop()[0]
        # name of the Prof is unique, but the location is not
        prof_list.append(Prof("Prof " + name, random.choice(locations)[0]))

    return prof_list

'''
Generate a list of  random Student object

@param  nstudents number of students need to be generated
        name_file file that stores names
'''
def random_students_generator(nstudents, name_file):
    names = random.sample(list_value_of_file(name_file), nstudents)
    student_list = list()

    for i in range(0, nstudents):
        name = names.pop()[0]
        student_list.append(Student("Student " + name))

    return student_list


'''
Randomly assign students to profs

@param prof_list a list of object Prof
'''
def random_assign_student_to_prof(prof_list, student_list, distance_file):
    distance = read_distance(distance_file)

    for prof in prof_list:

        for i in range(0, len(prof.schedule)):
            # the prof is free
            if prof.schedule[i] == 1:
                free_time_index = i
                student_list_copy = list(student_list)

                while prof.schedule[free_time_index] == 1:
                    if not student_list_copy:
                        raise Exception("Data Generation Failed. Ran Out of Students...")

                    random.shuffle(student_list_copy)
                    random_student = student_list_copy.pop()

                    if prof not in random_student.interviewed_profs:
                        # student is free when the prof is free
                        if random_student.schedule[free_time_index] == 1:
                            previous_prof = None
                            next_prof = None

                            if free_time_index + 1 < 8:
                                previous_prof = random_student.schedule[free_time_index + 1]
                            elif free_time_index - 1 >= 0:
                                next_prof = random_student.schedule[free_time_index - 1]

                            if isinstance(previous_prof, Prof):
                                # case: distance between the two profs is too long
                                if distance[(previous_prof.location, prof.location)] > 800:
                                    continue

                            if isinstance(next_prof, Prof):
                                if distance[(next_prof.location, prof.location)] > 800:
                                    continue

                            # schedule the appointment
                            prof.schedule[free_time_index] = random_student
                            random_student.schedule[free_time_index] = prof
                            random_student.interviewed_profs.append(prof)


'''
Given the number of profs and students, and generate valid test input.
And write thoese input into .csv files

int, int -> void
'''
def test_input_generator(nprof, nstudent, name_file, location_file, distance_file, file_num):

    profs = random_profs_generator(nprof, location_file, name_file)
    students = random_students_generator(nstudent, name_file)

    random_assign_student_to_prof(profs, students, distance_file)

    prof_file = open('data/generate/random_data_profs_{}.csv'.format(file_num), 'w+', newline='')
    student_file = open('data/generate/random_data_students_{}.csv'.format(file_num), 'w+', newline='')
    location_file = open('data/generate/random_data_locations_{}.csv'.format(file_num), 'w+', newline='')
    sample_prof_file = open("data/sample_data/Prof-Sample.csv", "r")

    prof_writer = csv.writer(prof_file, )
    student_writer = csv.writer(student_file)
    location_writer = csv.writer(location_file)

    sample_prof_reader = csv.reader(sample_prof_file)
    # write in porfs file to format
    for i in range(0, 6):
        format_row = next(sample_prof_reader)
        prof_writer.writerow(format_row)


    # write sample_data_profs.csv
    for prof in profs:
        schedule_write_list = []
        schedule_write_list.append(prof.name)

        location_write_list = []
        location_write_list.append(prof.name)
        location_write_list.append(prof.location)

        # check if there is an interview with student
        for inter in prof.schedule:
            if inter == 0 or inter == 1:
                schedule_write_list.append(None)
            elif isinstance(inter, Student):
                schedule_write_list.append("OK")

        prof_writer.writerow(schedule_write_list)
        location_writer.writerow(location_write_list)

    # write sample_data_students.csv
    for student in students:
        schedule_write_list = []
        schedule_write_list.append(student.name)

        for inter in student.schedule:
            if isinstance(inter, Prof):
                schedule_write_list.append(inter.name)

        student_writer.writerow(schedule_write_list)

'''
Run 'python sample_generator.py' in commandline to generate the test input file
The files will be located in data/generate/

The script read the .csv files from the data/generate/souce

if the program keeps failling to schedule. please adjust the number of students
    and professors. Usually, the number of students should be more than that of professors.
'''
if __name__ == "__main__":

    while(1):
        # Setting up the environment
        num_of_profs = None
        num_of_students = None
        file_num = None

        while not num_of_profs:
            print()
            print("Please setup the variables...")
            print("Please enter the number of professors want to generate")

            input_num = int(input())
            if input_num <= 0:
                print()
                print("======ERROR=====")
                print("ERROR: Your input is not valid.")
                print("Please enter a positive number")
            else:
                num_of_profs = input_num

        while not num_of_students:
            print()
            print("Please setup the variables...")
            print("Please enter the number of students want to generate")
            print("Note: The number of students better be greater than the number of professors")

            input_num = int(input())
            if input_num < 0:
                print()
                print("======ERROR=====")
                print("ERROR: Your input is not valid.")
                print("Please enter a positive number")
            else:
                num_of_students = input_num

        print()
        print("You want to generate {} Professors and {} Students\n".format(num_of_profs, num_of_students))


        print("Reading from source files in data/generate/source/ ...\n")

        location_file = "data/generate/source/Location-Sample.csv"
        distance_file = "data/generate/source/Distance-Sample.csv"
        name_file = "data/generate/source/Name-Sample.csv"

        print("======SUCCESS=====")
        print("Reading source files success...\n")

        print("Keep a log of number of sets of data created...\n")
        # keep a log of how many sets of files the program has generated
        log_file = open("data/generate/source/log", "r")
        file_generated = log_file.read()
        log_file.close()

        if not file_generated:
            file_num = 1
        else:
            file_num = int(file_generated) + 1


        print("Read Log success...\n")
        print("Generating data for you...\n")

        try:
            test_input_generator(num_of_profs, num_of_students, name_file, location_file, distance_file, file_num)
        except Exception as e:
            print("Error: " + repr(e) + "\n")
            continue

        print("======SUCCESS=====")
        print("Data generation success...\n")
        print("Please find this set of data here: data/generate/random_data_xx_{}\n".format(file_num))

        print("Logging...\n")
        log_file = open("data/generate/source/log", "w")
        log_file.write(str(file_num))
        log_file.close()

        print("Exiting...")
        exit()


