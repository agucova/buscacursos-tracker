def request_vacancy(nrc: str, semester: str):
    """Make the requests for vacancies to BuscaCursos serves and format the
    info into the API response format to vancany.

    Args:
        nrc (str): The nrc code from a specific section of a course. This
        need to be a valid nrc from the semestre requested.
        semester (str): Semester code of interes.

    Returns:
        dict: Dict with the vacancy information of the section given in the API
        response format.
    """
    url = (
        f"http://buscacursos.uc.cl/informacionVacReserva"
        + f".ajax.php?nrc={nrc}&termcode={semester}"
    )
    try:
        search = request_url(url)
    except HTTPError:
        search = []

    results = []
    for line in search:
        seccion_html = line.get_text().split("\n")
        remove = []
        for i in range(len(seccion_html)):
            seccion_html[i] = seccion_html[i].replace("\t", "")
            if seccion_html[i] == "":
                remove.append(i - len(remove))
        for i in remove:
            seccion_html.pop(i)
        seccion_html = [
            s.strip(" ") for s in seccion_html[0].split("-")
        ] + seccion_html[1:]
        results.append(seccion_html)
    results = results[1:] if len(results) > 0 else []
    finals = {"Disponibles": 0}
    for esc in results:
        if len(esc) < 3:
            continue
        print(esc)
        if esc[0] == "Vacantes libres" or esc[0] == "Vacantes Libres":
            if len(esc) == 4:
                finals["Libres"] = [int(i) for i in esc[-3:]]
            else:
                aux = [int(i) for i in esc[len(esc) - 3 :]]
                for i in range(3):
                    if finals.get("Libre"):
                        finals["Libres"][i] += aux[i]
                    else:
                        finals["Libres"] = aux[i]
            continue
        elif "TOTAL DISPONIBLES" in esc[0]:
            finals["Disponibles"] = int(esc[1])
            continue
        finals[esc[0]] = [int(i) for i in esc[-3:]]
    return finals
