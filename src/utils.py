import urllib.parse
import urllib.request
import json
import datetime
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

with open("src/config.json") as cfgFile:
    config = json.load(cfgFile)

departements = config["departements"]

def sayNumber(number : int):
    if number == "?":
        return ["null"]
    snumber = str(number)
    if len(snumber) == 1:
        return [number]
    if len(snumber) == 2:
        if number <= 16:
            return [number]
        if number < 60:
            if number%10 == 0:
                return [number]
            else:
                chiffre = 0
                while number%10 != 0:
                    chiffre += 1
                    number -= 1
                if chiffre == 1:
                    return [number, "et", 1]
                else:
                    return [number, chiffre]
        if number >= 60 and number < 70:
            if number-60 == 0:
                return [60]
            return [60, number-60]
        if number >= 70 and number < 80:
            result = [60]
            number2 = sayNumber(10 + number-70)
            for n in number2:
                result.append(n)
            return result
        if number >= 80 and number < 90:
            if number-80 == 0:
                return [80]
            return [80, number-80]
        if number >= 90 and number < 100:
            result = [80]
            number2 = sayNumber(10 + number-90)
            for n in number2:
                result.append(n)
            return result
    if len(snumber) == 3:
        centaine = int(snumber[0])
        if centaine != 1:
            result = [centaine, 100]
        else:
            result = [100]
        if sayNumber(number - (centaine * 100)) != [0]:
            number2 = sayNumber(number - (centaine * 100))
            for n in number2:
                result.append(n)
        return result
    if len(snumber) == 4:
        millier = int(snumber[0])
        if millier != 1:
            result = [millier, 1000]
        else:
            result = [1000]
        if sayNumber(number - millier * 1000) != [0]:
            number2 = sayNumber(number - millier * 1000)
            for n in number2:
                result.append(n)
        return result
    if len(snumber) == 5:
        dizainedemillier = int(snumber[0])
        if dizainedemillier != 1:
            result = []
            for n in sayNumber((dizainedemillier * 10) + int(snumber[1])):
                result.append(n)
            result.append(1000)
        else:
            result = [10 + int(snumber[1]), 1000]
        if sayNumber(number - (dizainedemillier * 10000) - (int(snumber[1]) * 1000)) != [0]:
            number2 = sayNumber(number - (dizainedemillier * 10000) - (int(snumber[1]) * 1000))
            for n in number2:
                result.append(n)
        return result
    if len(snumber) == 6:
        centainedemillier = int(snumber[0])
        result = []
        if sayNumber(number - ((centainedemillier * 100000) + (int(snumber[1]) * 10000) + (int(snumber[2]) * 1000))) != [0]:
            number2 = sayNumber(number - ((centainedemillier * 100000) + (int(snumber[1]) * 10000) + (int(snumber[2]) * 1000)))
            for n in sayNumber((centainedemillier * 100) + (int(snumber[1]) * 10) + int(snumber[2])):
                result.append(n)
        result.append(1000)
        for n in number2:
            result.append(n)
        return result

def getFrInfo():
    url = 'https://coronavirusapi-france.now.sh/FranceLiveGlobalData'
    resp = urllib.request.urlopen(url)
    try:
        originalData = json.loads(resp.read())["FranceGlobalLiveData"][0]
    except IndexError:
        return None

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

    for k in data:
        if data[k] == None:
            data[k] = "?"

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