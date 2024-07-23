import datetime

def currentTime():
        dateNow=datetime.datetime.now()
        return f"{dateNow.year}_{dateNow.month}_{dateNow.day}-{dateNow.hour}_{dateNow.minute}"
