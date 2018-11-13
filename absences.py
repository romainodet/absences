import datetime
import csv

ofile = open('stats.csv', "w")
writer = csv.writer(ofile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_ALL)
writer.writerow(['Login', 'abs'])

LOG_FILE = "radius.log"  # file of the logs
LOGIN_FILE = "login_1a_2015"  # all the login of the Students

presence = {}  # init the dictionary of the person which are present
statistics = {}  # init rhe dictionnary of the persons which are absents


for login in open(LOGIN_FILE, "r"):
    statistics[login.strip()] = 0

for line in open(LOG_FILE):
    if 'Auth: Login OK:' in line:
        res = line.split(' : ')

        dat = datetime.datetime.strptime(res[0], "%a %b %d %H:%M:%S %Y")
        day = dat.strftime("%d-%m-%Y")
        # Students are not supposed to be at school on week ends !
        if dat.strftime('%a') == "Sat" or dat.strftime('%a') == "Sun":
            continue

        if day not in presence:
            presence[day] = []

        login = line[line.find("[") + 1:line.find("]")]
        if login not in presence[day] and login in statistics:
            presence[day].append(login)


for day in presence:
    for student in statistics:
        if student not in presence[day]:
            print('Student %s was absent on %s' % (student, day))
            statistics[student] += 1

for login in sorted(statistics):
    print("%s => %d" % (login, statistics[login]))
    writer.writerow((login, statistics[login]))

ofile.close()
