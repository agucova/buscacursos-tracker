import pandas as pd
from os.path import exists
from os.path import getsize
import datetime
import pause
from helpers import writevacancies

semester = "2021-1"
storagep = "registro.csv"
targetsp = "ramos.csv"
inicio = datetime.datetime(2021, 1, 22, 4, 1)
granularidad = 1  # en minutos

# load target courses
targetsdf = pd.read_csv(targetsp)

if not exists(storagep) or getsize(storagep) == 0:
    storage = pd.DataFrame(
        columns=["time", "name", "section", "number", "nrc", "vacancies"]
    )
    storage.to_csv(storagep, index=False)


periodos = int((60 / granularidad) * 12)  # 12 horas en total
delta = datetime.timedelta(minutes=granularidad)

print("INFO: Waiting until", inicio)
pause.until(inicio)
for i in range(periodos):
    writevacancies(storagep, targetsdf, semester)
    inicio += delta
    print("INFO: Waiting until", inicio)
    pause.until(inicio)
