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

def sayFrInfo(args : str):
    result = getFrInfo()

    if result == None:
        return [["say", ["no-info"]], ["react", "❌"]]

    toSay = [
        "information-coronavirus",
        "france"
    ]

    for x in sayNumber(result["hospitalises"]):
        toSay.append(x)
    toSay.append("hospitalises")

    for x in sayNumber(result["reannimation"]):
        toSay.append(x)
    toSay.append("en-reanimation")

    for x in sayNumber(result["casConfirmesEhpad"]):
        toSay.append(x)
    toSay.append("cas")
    toSay.append("confirmes")
    toSay.append("en")
    toSay.append("ehpad")

    for x in sayNumber(result["casPossiblesEhpad"]):
        toSay.append(x)
    toSay.append("cas")
    toSay.append("possible")
    toSay.append("en")
    toSay.append("ehpad")

    for x in sayNumber(result["deces"]):
        toSay.append(x)
    toSay.append("deces")
    toSay.append("total")

    for x in sayNumber(result["gueris"]):
        toSay.append(x)
    toSay.append("gueris")
    toSay.append("total")

    for x in sayNumber(result["decesEhpad"]):
        toSay.append(x)
    toSay.append("deces")
    toSay.append("total")
    toSay.append("en")
    toSay.append("ehpad")

    for x in sayNumber(result["casConfirmes"]):
        toSay.append(x)
    toSay.append("cas")
    toSay.append("confirmes")
    return [
        [
            "say",
            toSay
        ],
        [
            "react", "✅"
        ]
    ]

def sayDepInfo(args : str):
    args = args.split(" ")
    try:
        departement = args[0].capitalize()
        date = args[1]
    except IndexError:
        return [["say", ["missing-args"]], ["react", "❌"]]

    date = date.replace(" ", "")
    originalDate = date
    date = date.replace("/", "-")

    splitDate = date.split("-")

    if len(splitDate) != 3 or len(splitDate[0]) != 2 or len(splitDate[1]) != 2 or len(splitDate[2]) != 4:
        return [["say", ["invalid-date"]], ["react", "❌"]]

    try:
        int(splitDate[0])
        int(splitDate[1])
        int(splitDate[2])
    except ValueError:
        return [["say", ["invalid-date"]], ["react", "❌"]]
    else:
        date = splitDate[2]+"-"+splitDate[1]+"-"+splitDate[0]

    if not int(splitDate[0]) in range(1, 32):
        return [["say", ["invalid-date"]], ["react", "❌"]]
    if not int(splitDate[1]) in range(1, 13):
        return [["say", ["invalid-date"]], ["react", "❌"]]
    if not int(splitDate[2]) in [2019, 2020]:
        return [["say", ["invalid-date"]], ["react", "❌"]]

    print(departement)

    result = getDepInfo(departement, date)

    if result == False:
        return [["say", ["invalid-dep"]], ["react", "❌"]]
    elif result == True:
        return [["say", ["api-error"]], ["react", "❌"]]
    elif result == None:
        return [["say", ["no-info", "a-date"]], ["react", "❌"]]

    toSay = [
        "information-coronavirus"
    ]

    print(result)

    for x in sayNumber(result["Hospitalisés"]):
        toSay.append(x)
    toSay.append("hospitalises")

    for x in sayNumber(result["EnReanimation"]):
        toSay.append(x)
    toSay.append("en-reanimation")

    for x in sayNumber(result["NouvellesHospitalisations"]):
        toSay.append(x)
    toSay.append("nouvelle")
    toSay.append("hospitalisation")

    for x in sayNumber(result["NouvellesReanimations"]):
        toSay.append(x)
    toSay.append("nouvelle")
    toSay.append("reanimation")

    for x in sayNumber(result["Décès"]):
        toSay.append(x)
    toSay.append("deces")
    toSay.append("total")

    for x in sayNumber(result["Gueris"]):
        toSay.append(x)
    toSay.append("gueris")
    toSay.append("total")

    print(toSay)
    return [
        [
            "say",
            toSay
        ],
        [
            "react", "✅"
        ]
    ]

def helpCommand(args : str):
    if args != "":
        command = args.split(" ")[0].lower()
        if command == "depinfo":
            return [["message", "La commande `"+config["prefix"]+"depInfo` sert a avoir des informations sur un departement en question à une date précise.\nUsage : `"+config["prefix"]+"depInfo <departement> <data>`\n\nLa date est au format : `DD/MM/YYYY`"], ["react", "❔"]]
        elif command == "frinfo":
            return [["message", "La commande `"+config["prefix"]+"frInfo` sert a avoir les informations les plus récentes sur toute la France.\nUsage : `"+config["prefix"]+"frInfo`"], ["react", "❔"]]
        if command == "saydepinfo":
            return [["message", "La commande `"+config["prefix"]+"sayDepInfo` sert a avoir des informations sur un departement en question à une date précise vocalement.\nUsage : `"+config["prefix"]+"sayDepInfo <departement> <data>`\n\nLa date est au format : `DD/MM/YYYY`"], ["react", "❔"]]
        elif command == "sayfrinfo":
            return [["message", "La commande `"+config["prefix"]+"sayFrInfo` sert a avoir les informations les plus récentes sur toute la France vocalement.\nUsage : `"+config["prefix"]+"sayFrInfo`"], ["react", "❔"]]
        else:
            return [
                [
                    "message",
                    "`"+config["prefix"]+"frInfo`  : Avoir les informations sur toute la France.\n`"+config["prefix"]+"depInfo` : Avoir des informations sur un departement à une date précise.\n`"+config["prefix"]+"sayFrInfo` : Avoir les informations sur toute la France vocalement.\n`"+config["prefix"]+"sayDepInfo` : Avoir des informations sur un departement à une date précise vocalement.\n\nPour plus d'informations sur une commande, faites : `"+config["prefix"]+"help <commande>`"],
                    ["react", "❔"]
                ]
    else:
        return [
            [
                "message",
                "`"+config["prefix"]+"frInfo`  : Avoir les informations sur toute la France.\n`"+config["prefix"]+"depInfo` : Avoir des informations sur un departement à une date précise.\n`"+config["prefix"]+"sayFrInfo` : Avoir les informations sur toute la France vocalement.\n`"+config["prefix"]+"sayDepInfo` : Avoir des informations sur un departement à une date précise vocalement.\n\nPour plus d'informations sur une commande, faites : `"+config["prefix"]+"help <commande>`"],
                ["react", "❔"]
            ]

def frInfo(args : str):
    result = getFrInfo()

    if result == False:
        return [["message", ":x: Le departement est invalide !"], ["react", "❌"]]
    elif result == True:
        return [["message", ":x: Erreur lors de la recuperation des information de l'api !"], ["react", "❌"]]
    elif result == None:
        return [["message", ":x: Aucune information trouvé"], ["react", "❌"]]
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

def test(args : str):
    try:
        args = int(args)
    except ValueError:
        toSay = []
        for word in args.split(" "):
            try:
                if sayNumber(int(word)) == None:
                    toSay.append(word)
                else:
                    for n in sayNumber(int(word)):
                        toSay.append(n)
            except:
                toSay.append(word)
        return [["say", toSay], ["react", "✅"]]
    return [["say", sayNumber(args)], ["react", "✅"]]

def exitCommand(args : str):
    return [["exit", None]]

commands = {
    "depinfo": depInfo,
    "frinfo": frInfo,
    "sayfrinfo": sayFrInfo,
    "saydepinfo":sayDepInfo,
    "help": helpCommand,
    "say": test,
    "exit": exitCommand
}