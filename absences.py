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


def read_abs(LOG_FILE, LOGIN_FILE):
    presence = {}  # init the dictionary of the person which are present
    statistics = {}  # init the dictionnary of the persons which are absents
    connexion = {}

    try:
        open(LOGIN_FILE, "r")
        open(LOG_FILE, 'r')
    except:
        exit('One of those files doesn\'t exist')

    for login in open(LOGIN_FILE, "r"):
        statistics[login.strip()] = 0

    boucle = 0
    for line in open(LOG_FILE):
        if 'Auth: Login OK:' in line:
            res = line.split(' : ')

            dat = datetime.datetime.strptime(res[0], "%a %b %d %H:%M:%S %Y")
            day = dat.strftime("%d-%m-%Y")
            # Students are not supposed to be at school on week ends !
            if dat.strftime('%a') == "Sat" or dat.strftime('%a') == "Sun" or (
                    dat.strftime('%d') == "11" and dat.strftime('%m') == "11"):
                continue

            if day not in presence:
                presence[day] = []

            login = line[line.find("[") + 1:line.find("]")]
            if login not in presence[day] and login in statistics:
                presence[day].append(login)

            if boucle == 0:
                for login in statistics:
                    connexion[login] = 0
                boucle = 1
            if login in presence[day] and login in statistics:
                connexion[login] += 1

    for login in statistics:
        connexion[login] = round(connexion[login] / 2)

    for day in presence:
        for student in statistics:
            if student not in presence[day]:
                print('Student %s was absent on %s' % (student, day))
                statistics[student] += 1

    pause("Please press a button to continue")

    with open('stats.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Login', 'Name', 'Number of non-attendance', 'Number of connexion'])
        for login in sorted(statistics):
            print("%s => %d" % (login, statistics[login]))
            writer.writerow((login, login.replace(".", " ").title(), statistics[login], connexion[login]))
    pause("Please press a button to finish")
    blank(30)

def decoder_csv(file):
    f = open(file, 'r')

    reader = csv.reader(f)
    next(reader)
    for row in reader:
        print('The student', row[0], 'was absent', row[1], 'time(s)')
    f.close()
    pause("")
    blank(30)


def add_login(LOGIN_FILE):
    login = input("Please enter the login to add : ")
    with open(LOGIN_FILE, "a") as f:
        f.write("\n")
        f.write(login)
    print("Login", login, "for", login.replace(".", " ").title(), "is succesfully added")
    pause("")
    blank(30)
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
    try:
        mode = int(input(' CHOOSE THE MODE : '))
    except:
        print('An error occured during the process. Please choose the number 1 for DECODER or 2 for ENCODER')

    if mode == 1:
        file = input('Please enter the name of the csv file to decode : ')
        decoder_csv(file)
    elif mode == 2:
        try:
            LOG_FILE = "radius.log"  # file of the logs
            LOGIN_FILE = "login_1a_2015"  # all the login of the Students
            read_abs(LOG_FILE, LOGIN_FILE)
        except:
            print('An error occured while reading file')
    elif mode == 3:
        LOGIN_FILE = "login_1a_2015"  # all the login of the Students
        add_login(LOGIN_FILE)
    elif mode == 4:
        try:
            LOGIN_FILE = "login_1a_2015"
            f = open(LOGIN_FILE)
            for line in f:
                print(line)
            f.close()
        except:
            print("Error while loading the file")
        pause("Press any key")
        blank(30)
    elif mode == 0:
        exit('You ask to interrupt the program. GoodBye')
    else:
        print('An error occured')
