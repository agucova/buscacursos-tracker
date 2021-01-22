import requests
from bs4 import BeautifulSoup


def CrawlWords(url):
    resource = requests.get(url).text
    souped_resource = BeautifulSoup(resource, "html.parser")

    all_td = souped_resource.find_all("td")
    lista = []
    for each_result in all_td:
        # elimina los tags de cada td
        each_result_str = each_result.string
        lista.append(each_result_str)
    for i in range(len(lista)):
        if lista[i] == "Laboratorio de Termodinámica":
            print("Total:", lista[i - 3], "Libres:", lista[i + 5])


CrawlWords(
    r"http://buscacursos.uc.cl/?cxml_semestre=2020-1&cxml_sigla=FIS0152#resultados"
)
