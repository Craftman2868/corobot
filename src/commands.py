from src.utils import *

def depInfo(args : str):
    args = args.split(" ")
    try:
        departement = args[0]
        date = args[1]
    except IndexError:
        return [["message", ":x: Argument manquants"], ["react", "❌"]]

    result = getDepInfo(departement, date)

    date = date.replace(" ", "")
    date = date.replace("/", "-")

    splitDate = date.split("-")

    if len(splitDate) != 3 or len(splitDate[0]) != 4 or len(splitDate[1]) != 2 or len(splitDate[2]) != 2:
        return [["message", ":x: Date invalide !"], ["react", "❌"]]

    try:
        int(splitDate[0])
        int(splitDate[1])
        int(splitDate[2])
    except ValueError:
        return [["message", ":x: Date invalide !"], ["react", "❌"]]

    if result == False:
        return [["message", ":x: Le departement est invalide !"], ["react", "❌"]]
    elif result == True:
        return [["message", ":x: Erreur lors de la recuperation des information de l'api !"], ["react", "❌"]]
    elif result == None:
        return [["message", ":x: Aucune information trouvé a cette date !"], ["react", "❌"]]
    else:
        return [
            ["embed", [
                result["Date"],
                result["Departement"],
                "Hospitalisés : "+result["Hospitalisés"]+"\nEn réanimation"+result["EnReanimation"]+"\nNouvelles hospitalisation(s) : "+result["NouvellesHospitalisations"]+"\nNouvelles reanimation(s) : "+result["NouvellesReanimations"]+"\nDécès total : "+result["Décès"]+"\nGueris total : "+result["Gueris"],
                result["Source"]
                ]
            ],
            [
                "react", "✔"
            ]
        ]


commands = {
    "depInfo": depInfo
}