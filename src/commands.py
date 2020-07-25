from src.utils import *

def depInfo(args : str):
    args = args.split(" ")
    try:
        departement = args[0]
        date = args[1]
    except IndexError:
        return [["message", ":x: Argument manquants"], ["react", "❌"]]

    date = date.replace(" ", "")
    originalDate = date
    date = date.replace("/", "-")

    splitDate = date.split("-")

    if len(splitDate) != 3 or len(splitDate[0]) != 2 or len(splitDate[1]) != 2 or len(splitDate[2]) != 4:
        return [["message", ":x: Date invalide !"], ["react", "❌"]]

    try:
        int(splitDate[0])
        int(splitDate[1])
        int(splitDate[2])
    except ValueError:
        return [["message", ":x: Date invalide !"], ["react", "❌"]]
    else:
        date = splitDate[2]+"-"+splitDate[1]+"-"+splitDate[0]

    result = getDepInfo(departement, date)

    if result == False:
        return [["message", ":x: Le departement est invalide !"], ["react", "❌"]]
    elif result == True:
        return [["message", ":x: Erreur lors de la recuperation des information de l'api !"], ["react", "❌"]]
    elif result == None:
        return [["message", ":x: Aucune information trouvé a cette date !"], ["react", "❌"]]
    else:
        return [
            ["embed", [
                originalDate,
                result["Departement"],
                "Hospitalisés : "+str(result["Hospitalisés"])+"\nEn réanimation : "+str(result["EnReanimation"])+"\nNouvelles hospitalisation(s) : "+str(result["NouvellesHospitalisations"])+"\nNouvelles reanimation(s) : "+str(result["NouvellesReanimations"])+"\nDécès total : "+str(result["Décès"])+"\nGueris total : "+str(result["Gueris"]),
                "Source : "+result["Source"]
                ]
            ],
            [
                "react", "✅"
            ]
        ]


commands = {
    "depInfo": depInfo
}