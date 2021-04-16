from datetime import date, datetime
from random import randint

def getRandomDate():
    startDate = datetime(2010, 1, 1).toordinal()
    endDate = date.today().toordinal()
    return date.fromordinal(randint(startDate, endDate)).strftime('%m/%d/%Y')