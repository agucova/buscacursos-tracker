from bs4 import BeautifulSoup
import requests
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException
import datetime


def requests_retry_session(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_vacancies(nrc: str, semester: str):
    url = (
        f"http://buscacursos.uc.cl/informacionVacReserva"
        + f".ajax.php?nrc={nrc}&termcode={semester}"
    )
    resp = requests_retry_session().get(url).text

    soup = BeautifulSoup(resp, "lxml")
    name_box = soup.find_all("tr", attrs={"class": "resultadosRowPar"})
    name_box1 = soup.find_all("tr", attrs={"class": "resultadosRowImpar"})
    result = []

    for i in range((len(name_box) + len(name_box1))):
        if name_box and i % 2 == 0:
            result.append(name_box.pop(0))
        elif name_box1 and i % 2 != 0:
            result.append(name_box1.pop(0))

    results = []
    for line in result:
        seccion_html = line.get_text().split("\n")
        remove = []
        for i in range(len(seccion_html)):
            seccion_html[i] = seccion_html[i].replace("\t", "")
            if seccion_html[i] == "":
                remove.append(i - len(remove))
        for i in remove:
            seccion_html.pop(i)
        # mod: deleted number in academic unit
        ua = seccion_html[0].split("-")
        ua = ua[1].strip() if len(ua) >= 2 else ua[0].strip("")
        seccion_html = [ua] + seccion_html[1:]
        results.append(seccion_html)

    results = results[1:] if len(results) > 0 else []
    matrix = []
    for esc in results:
        if len(esc) < 3:
            continue
        matrix.append(esc)
    return matrix


def fallback_get_vacancies(nrc, name, semester):
    url = (
        f"http://buscacursos.uc.cl/?cxml_semestre={semester}&cxml_nrc={nrc}#resultados"
    )
    resource = requests.get(url).text
    souped_resource = BeautifulSoup(resource, "html.parser")

    all_td = souped_resource.find_all("td")
    lista = []
    for each_result in all_td:
        # elimina los tags de cada td
        each_result_str = each_result.string
        lista.append(each_result_str)
    for i in range(len(lista)):
        if lista[i] == name:
            total = lista[i + 4]
            disponibles = lista[i + 5]
            ocupadas = str(int(total) - int(disponibles))
    return [["Vacantes libres", total, ocupadas, disponibles]]


def writevacancies(storagep, targetsdf, semester):
    print("INFO: Starting cycle...")
    with open(storagep, "a", buffering=1) as register:
        writer = csv.writer(register)
        targets = targetsdf["NRC"]
        for i, nrc in enumerate(targets):
            name = targetsdf["Nombre"][i]
            section = int(targetsdf["Sección"][i])
            number = targetsdf["Sigla"][i]

            try:
                vacancies = get_vacancies(nrc, semester)
            except RequestException:
                print("WARNING:", "Skiping", nrc, "due to unrecoverable error.")
                continue

            if vacancies == []:
                vacancies = fallback_get_vacancies(nrc, name, semester)

            time = datetime.datetime.now(datetime.timezone.utc)
            writer.writerow([time, name, section, number, nrc, vacancies])
    print("INFO: Finished this cycle.")
