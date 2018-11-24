import datetime
import csv


def read_abs(LOG_FILE, LOGIN_FILE):
    presence = {}  # init the dictionary of the person which are present
    statistics = {}  # init rhe dictionnary of the persons which are absents
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
            login_complet = login.replace(".", " ").title()
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
    with open('stats.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Login', 'Name', 'Number of non-attendance', 'Number of connexion'])
        for login in sorted(statistics):
            print("%s => %d" % (login, statistics[login]))
            writer.writerow((login, login.replace(".", " ").title(), statistics[login], connexion[login]))


def decoder_csv(file):
    f = open(file, 'r')

    reader = csv.reader(f)
    next(reader)
    for row in reader:
        print('The student', row[0], 'was absent', row[1], 'time(s)')
    f.close()


while True:
    print('''
     _      _  _____ _    ____  _____ ____  ____  ____  _____ ____ 
    / \  /|/ \/    // \  /  _ \/  __//   _\/  _ \/  _ \/  __//  __\\
    | |  ||| ||  __\| |  | | \||  \  |  /  | / \|| | \||  \  |  \/|
    | |/\||| || |   | |  | |_/||  /_ |  \_ | \_/|| |_/||  /_ |    /
    \_/  \|\_/\_/   \_/  \____/\____\\\\____/\____/\____/\____\\\\_/\_\\

    Welcome in the wifi decoder/encoder :

    2 modes are available :
     TYPE 1 FOR THE DECODER
     TYPE 2 FOR THE ENCODER

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
        # try
        LOG_FILE = "radius.log"  # file of the logs
        LOGIN_FILE = "login_1a_2015"  # all the login of the Students
        read_abs(LOG_FILE, LOGIN_FILE)
        # except:
        # print('An error occured')
    elif mode == 0:
        exit('You ask to interrupt the program. GoodBye')
