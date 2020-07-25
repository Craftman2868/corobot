from src.utils import *

def depInfo(args : str):
    args = args.split(" ")
    try:
        departement = args[0].capitalize()
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

def frInfo(args : str):
    result = getFrInfo()

    if result == False:
        return [["message", ":x: Le departement est invalide !"], ["react", "❌"]]
    elif result == True:
        return [["message", ":x: Erreur lors de la recuperation des information de l'api !"], ["react", "❌"]]
    elif result == None:
        return [["message", ":x: Aucune information trouvé a cette date !"], ["react", "❌"]]
    else:
        return [
            ["embed", [
                result["date"],
                result["nom"],
                "Hospitalisés : "+str(result["hospitalises"])+"\nEn réanimation : "+str(result["reanimation"])+"\nCas confirmé(s) en éhpad : "+str(result["casConfirmesEhpad"])+"\nCas possible(s) en éhpad : "+str(result["casPossiblesEhpad"])+"\nDécès total : "+str(result["deces"])+"\nGueris total : "+str(result["gueris"])+"\nDécès total éhpad : "+str(result["decesEhpad"])+"\nCas confirmés : "+str(result["casConfirmes"]),
                "Source : "+result["source"]
                ]
            ],
            [
                "react", "✅"
            ]
        ]

def helpCommand(args):
    if args != "":
        command = args.split(" ")[0].lower()
        if command == "depinfo":
            return [["message", "La commande `"+config["prefix"]+"depInfo` sert a avoir des informations sur un departement en question à une date précise.\nUsage : `"+config["prefix"]+"depInfo <departement> <data>`\n\nLa date est au format : `DD/MM/YYYY`"], ["react", "❔"]]
        elif command == "frinfo":
            return [["message", "La commande `"+config["prefix"]+"frInfo` sert a avoir les informations les plus récentes sur toute la France.\nUsage : `"+config["prefix"]+"frInfo`"], ["react", "❔"]]
        else:
            return [["message", "`"+config["prefix"]+"frInfo`  : Avoir les informations sur toute la France.\n`"+config["prefix"]+"depInfo` : Avoir des informations sur un departement à une date précise.\n\nPour plus d'informations sur une commande, faites : `"+config["prefix"]+"help <commande>`"], ["react", "❔"]]
    else:
        return [["message", "`"+config["prefix"]+"frInfo`   : Avoir les informations sur toute la France.\n`"+config["prefix"]+"depInfo` : Avoir des informations sur un departement à une date précise.\n\nPour plus d'informations sur une commande, faites : `"+config["prefix"]+"help <commande>`"], ["react", "❔"]]

commands = {
    "depinfo": depInfo,
    "frinfo": frInfo,
    "help": helpCommand
}