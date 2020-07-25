import urllib.parse
import urllib.request
import json
import datetime

with open("src/config.json") as cfgFile:
    config = json.load(cfgFile)

departements = config["departements"]

def getFrInfo():
    url = 'https://coronavirusapi-france.now.sh/FranceLiveGlobalData'
    resp = urllib.request.urlopen(url)
    originalData = json.loads(resp.read())["FranceGlobalLiveData"][0]

    # data = {
    #     "Nom": config["null"],
    #     "Date": config["null"],
    #     "Hospitalisés": config["null"],
    #     "EnReanimation": config["null"],
    #     "DécèsEhpad": config["null"],
    #     "CasEhpad": config["null"],
    #     "CasConfirmés": config["null"],
    #     "CasConfirmésEhpad": config["null"],
    #     "CasPossiblesEhpad": config["null"],
    #     "Décès": config["null"],
    #     "Gueris": config["null"],
    #     "Source": config["null"]
    # }

    data = {}

    try:
        data["nom"] = originalData["nom"]
    except KeyError:
        data["nom"] = config["null"]

    try:
        data["date"] = originalData["date"]
    except KeyError:
        data["date"] = config["null"]

    try:
        data["hospitalises"] = originalData["hospitalises"]
    except KeyError:
        data["hospitalises"] = config["null"]

    try:
        data["reanimation"] = originalData["reanimation"]
    except KeyError:
        data["reanimation"] = config["null"]

    try:
        data["decesEhpad"] = originalData["decesEhpad"]
    except KeyError:
        data["decesEhpad"] = config["null"]

    try:
        data["casEhpad"] = originalData["casEhpad"]
    except KeyError:
        data["casEhpad"] = config["null"]

    try:
        data["casConfirmes"] = originalData["casConfirmes"]
    except KeyError:
        data["casConfirmes"] = config["null"]

    try:
        data["casConfirmesEhpad"] = originalData["casConfirmesEhpad"]
    except KeyError:
        data["casConfirmesEhpad"] = config["null"]

    try:
        data["casPossiblesEhpad"] = originalData["casPossiblesEhpad"]
    except KeyError:
        data["casPossiblesEhpad"] = config["null"]

    try:
        data["deces"] = originalData["deces"]
    except KeyError:
        data["deces"] = config["null"]

    try:
        data["gueris"] = originalData["gueris"]
    except KeyError:
        data["gueris"] = config["null"]

    try:
        data["source"] = originalData["source"]["nom"]
    except KeyError:
        data["source"] = config["null"]

    return data

def getDepInfo(departement, date : str):
    if departement in departements.keys():
        departement = departements[departement]
    elif departement in departements.values():
        pass
    else:
        return False

    url = 'https://coronavirusapi-france.now.sh/AllDataByDepartement'
    args = {
        "Departement":departement
    }
    args = urllib.parse.urlencode(args)
    url = url + '?' + args
    resp = urllib.request.urlopen(url)
    data = json.loads(resp.read())["allDataByDepartement"]

    goodData = None

    for x in data:
        if x["date"] == date:
            goodData = x

    if goodData == None:
        return

    try:
        data = {
            "Departement": goodData["nom"],
            "Date": goodData["date"],
            "Hospitalisés": goodData["hospitalises"],
            "EnReanimation": goodData["reanimation"],
            "NouvellesHospitalisations": goodData["nouvellesHospitalisations"],
            "NouvellesReanimations": goodData["nouvellesHospitalisations"],
            "Décès": goodData["deces"],
            "Gueris": goodData["gueris"],
            "Source": goodData["source"]["nom"]
        }
    except KeyError:
        return True

    return data

if __name__ == "__main__":
    while True:
        try:
            departement = input("Departement >")
            date = input("Date >")
        except KeyboardInterrupt:
            print("\nAu revoir")
            exit()
        splitDate = date.split("-")

        if len(splitDate) != 3 or len(splitDate[0]) != 4 or len(splitDate[1]) != 2 or len(splitDate[2]) != 2:
            print("Date invalide !")

        try:
            int(splitDate[0])
            int(splitDate[1])
            int(splitDate[2])
        except ValueError:
            print("Date invalide !")

        departement = departement.lower().capitalize()

        try:
            result = getDepInfo(departement, date)
        except KeyboardInterrupt:
            print("Au revoir")
            exit()

        if result == False:
            print("Le departement est invalide !")
        elif result == True:
            print("Erreur lors de la recuperation des information de l'api")
        elif result == None:
            print("Aucune information trouvé a cette date")
        else:
            print(json.dumps(result,indent=4,ensure_ascii=False).replace("null", config["null"]))