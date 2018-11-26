import datetime
import csv

# Function permit to clear the screen with the number of line which are indicate in the attribute
def blank(lignes):
    for i in range(lignes):
        print("")
    return 0


# Function reproduce the pause() function in C
def pause(message):
    input(message)
    return 0


def read_abs(LOG_FILE, LOGIN_FILE):  # function to read a log file
    presence = {}  # init the dictionary of the person which are present
    statistics = {}  # init the dictionnary of the persons which are absents
    connexion = {}  # init the dictionnary of the number of connetion per students

    try:  # Try to open the files of login and logs
        open(LOGIN_FILE, "r")
        open(LOG_FILE, 'r')
    except:  # else disp a message
        exit('One of those files doesn\'t exist')

    for login in open(LOGIN_FILE, "r"):  # add the logins to the dictionary with the value 0
        statistics[login.strip()] = 0

    boucle = 0
    for line in open(LOG_FILE):  # for each line of the log file
        if 'Auth: Login OK:' in line:  # when the authentication is OK
            res = line.split(' : ')  # Split the line in " : "
            # convert the dates
            dat = datetime.datetime.strptime(res[0], "%a %b %d %H:%M:%S %Y")
            day = dat.strftime("%d-%m-%Y")
            # Students are not supposed to be at school on week ends and the 11/11!
            if dat.strftime('%a') == "Sat" or dat.strftime('%a') == "Sun" or (
                    dat.strftime('%d') == "11" and dat.strftime('%m') == "11"):
                continue
            # if the day of the line is not in the presence dictionary, create them
            if day not in presence:
                presence[day] = []

            login = line[line.find("[") + 1:line.find("]")]  # Extract the login
            if login not in presence[
                day] and login in statistics:  # if the login is not in the presence day and the login is in the login file, add the login
                presence[day].append(login)

            if boucle == 0:  # if it isn't enter in the condition
                for login in statistics:  # add the login of the students and the var to 0
                    connexion[login] = 0
                boucle = 1  # pass the boucle to 1 to disallow the condition
            if login in presence[day] and login in statistics:  # if the student connect to wifi, and is in the list
                connexion[login] += 1  # add one to the list

    for login in statistics:  # for all the login in the login list divide by 2 because in the log there is 2 lines when auth is ok for each student
        connexion[login] = round(connexion[login] / 2)

    for day in presence:  # Print all the students absences and add 1 to statistics for the student
        for student in statistics:
            if student not in presence[day]:
                print('Student %s was absent on %s' % (student, day))
                statistics[student] += 1

    pause("Please press a button to continue")  # pause

    with open('stats.csv', 'w', newline='') as outfile:  # write into the csv
        writer = csv.writer(outfile)
        writer.writerow(['Login', 'Name', 'Number of non-attendance', 'Number of connexion'])  # head of the CSV
        for login in sorted(statistics):  # print in the csv and at the screen the number of absences for each students
            print("%s => %d" % (login, statistics[login]))  # print on the screen
            writer.writerow(
                (login, login.replace(".", " ").title(), statistics[login], connexion[login]))  # Add in the csv
    pause("Please press a button to finish")  # pause
    blank(30)  # clean the screen


def decoder_csv(file):  # function to decode the csv file
    try:
        f = open(file, 'r')  # only open the file

        reader = csv.reader(f)  # open the file as a CSV
        next(reader)  # pass the header
        for row in reader:  # for each row of the file ...
            print('The login', row[0], 'for the student', row[0].replace(".", " ").title(), 'was absent', row[2],
                  'time(s)')  # print the login and the number of time he/she was absent
        f.close()  # close the file
    except:
        print("Error while loading the file...")
    pause("")  # pause
    blank(30)  # clean the screen


def add_login(LOGIN_FILE):  # Add the login to the login file
    login = input("Please enter the login to add : ")  # input of the new login
    with open(LOGIN_FILE, "a") as f:  # Open the login file
        f.write("\n")  # carriage return from the last login
        f.write(login)  # write the into the file
    print("Login", login, "for", login.replace(".", " ").title(),
          "is succesfully added")  # display the login is succesfuly added
    pause("")  # pause
    blank(30)  # clean the screen

while True:
    print('''
     _      _  _____ _    ____  _____ ____  ____  ____  _____ ____ 
    / \  /|/ \/    // \  /  _ \/  __//   _\/  _ \/  _ \/  __//  __\\
    | |  ||| ||  __\| |  | | \||  \  |  /  | / \|| | \||  \  |  \/|
    | |/\||| || |   | |  | |_/||  /_ |  \_ | \_/|| |_/||  /_ |    /
    \_/  \|\_/\_/   \_/  \____/\____\\\\____/\____/\____/\____\\\\_/\_\\

    Welcome in the wifi decoder/encoder :

    3 modes are available :
     TYPE 1 FOR THE DECODER
     TYPE 2 FOR THE ENCODER
     TYPE 3 ADD A LOGIN TO THE LOG FILE
     TYPE 4 TO VIEW THE LOGIN FILE

    If you want to exit type 0

     Please select one :                                                              
    ''')
    mode = None
    try:  # try choose a mode
        mode = int(input(' CHOOSE THE MODE : '))
    except:  # if error print error
        print('An error occured during the process. Please choose the number')

    if mode == 1:  # call the function 1
        file = input('Please enter the name of the csv file to decode : ')
        decoder_csv(file)
    elif mode == 2:  # call the function 2
        try:
            LOG_FILE = "radius.log"  # file of the logs
            LOGIN_FILE = "login_1a_2015"  # all the login of the Students
            read_abs(LOG_FILE, LOGIN_FILE)
        except:
            print('An error occured while reading file')
    elif mode == 3:  # call the function 3
        LOGIN_FILE = "login_1a_2015"  # all the login of the Students
        add_login(LOGIN_FILE)
    elif mode == 4:  # call the function 4
        try:
            LOGIN_FILE = "login_1a_2015"
            f = open(LOGIN_FILE)  # open the login file
            for line in f:  # print each line of the file
                print(line)
            f.close()  # close the file
        except:
            print("Error while loading the file")
        pause("Press any key")  # pause
        blank(30)  # clean the screen
    elif mode == 0:  # call the exit
        exit('You ask to interrupt the program. GoodBye')
    else:
        print('An error occured')
