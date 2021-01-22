import requests
from bs4 import BeautifulSoup


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
