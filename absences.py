import datetime

LOG_FILE = "radius.log"
LOGIN_FILE = "login_1a_2015"

presence = {}
statistics = {}


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
