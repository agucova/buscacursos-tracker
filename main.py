import pandas as pd
from os.path import exists
from os.path import getsize
import datetime
import pause
from helpers import writevacancies

semester = "2021-1"
storagep = "registro.csv"
targetsp = "ramos.csv"
inicio = datetime.datetime(2021, 1, 22, 7, 45)
granularidad = 20  # en minutos

# load target courses
targetsdf = pd.read_csv(targetsp)

if not exists(storagep) or getsize(storagep) == 0:
    storage = pd.DataFrame(
        columns=["time", "name", "section", "number", "nrc", "vacancies"]
    )
    storage.to_csv(storagep, index=False)


periods = int(
    (60 / granularidad) * 13
)  # 13 horas en total (son 12, pero para estar seguro)
print("INFO: A total of", periods, "cycles will be run.")
delta = datetime.timedelta(minutes=granularidad)

print("INFO: Waiting until", inicio, "(Cycle 0)")
pause.until(inicio)
for i in range(periods):
    writevacancies(storagep, targetsdf, semester)
    inicio += delta
    print("INFO: Waiting until", inicio, "(Cycle" + str(i + 1) + ")")
    pause.until(inicio)
print("INFO: No more cycles left. Stopping program...")
