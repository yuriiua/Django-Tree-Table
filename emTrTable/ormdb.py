from emTrTable.models import EmployeeTreeModel
from .Names import *
import random


def randomdate():
    year = random.randint(2001, 2018)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return '{}-{}-{}'.format(year, month, day)

def filldb():
    first = EmployeeTreeModel(
        fullName=random.choice(FIRSTNAMES) + ' ' + random.choice(LASTNAMES),
        bossID=0,
        employeeDate='2001-01-01',
        position=POSITION[1][0],
        salary=50000,
        level=1,
        photo='',
        bossName='I`m Boss')
    first.save()

    for secondLevel in POSITION[2]:
        second = EmployeeTreeModel(
            fullName= random.choice(FIRSTNAMES)+' '+random.choice(LASTNAMES),
            bossID=first.id,
            employeeDate=randomdate(),
            position=secondLevel,
            salary=random.randrange(8000, 10000, 100),
            level=2,
            photo='',
            bossName=first.fullName)
        second.save()
        for thirdLevel in POSITION[3]:
            third = EmployeeTreeModel(
                fullName=random.choice(FIRSTNAMES)+' '+random.choice(LASTNAMES),
                bossID=second.id,
                employeeDate=randomdate(),
                position=thirdLevel,
                salary=random.randrange(4000, 5000, 100),
                level=3,
                photo='',
                bossName=second.fullName)
            third.save()
            for forthLevel in POSITION[4]:
                forth = EmployeeTreeModel(
                    fullName=random.choice(FIRSTNAMES) + ' ' + random.choice(LASTNAMES),
                    bossID=third.id,
                    employeeDate=randomdate(),
                    position=forthLevel,
                    salary=random.randrange(2000, 3000, 100),
                    level=4,
                    photo='',
                    bossName=third.fullName)
                forth.save()
                for i in range(1, 1500):
                    fives = EmployeeTreeModel(
                        fullName=random.choice(FIRSTNAMES) + ' ' + random.choice(LASTNAMES),
                        bossID=forth.id,
                        employeeDate=randomdate(),
                        position=random.choice(POSITION[5]),
                        salary=random.randrange(1000, 2000, 100),
                        level=5,
                        photo='',
                        bossName=forth.fullName)
                    fives.save()
