import math
import random

LIGNES = 6
COLONNES = 7
SYMBOLES = {0: ".", 1: "X", 2: "O"}

DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]


def nouvelle_grille():
    grille = []
    for i in range(LIGNES):
        grille.append([0] * COLONNES)
    return grille


def afficher(grille):
    print()
    for ligne in grille:
        texte = ""
        for case in ligne:
            texte = texte + SYMBOLES[case] + " "
        print(texte)
    print("1 2 3 4 5 6 7")


def coup_possible(grille, colonne):
    return 0 <= colonne < COLONNES and grille[0][colonne] == 0


def jouer(grille, colonne, joueur):
    for ligne in range(LIGNES - 1, -1, -1):
        if grille[ligne][colonne] == 0:
            grille[ligne][colonne] = joueur
            return ligne


def retirer(grille, ligne, colonne):
    grille[ligne][colonne] = 0


def compter(grille, ligne, colonne, vecteur, joueur):
    dl, dc = vecteur
    nombre = 0
    l = ligne + dl
    c = colonne + dc
    while 0 <= l < LIGNES and 0 <= c < COLONNES and grille[l][c] == joueur:
        nombre = nombre + 1
        l = l + dl
        c = c + dc
    return nombre


def victoire(grille, ligne, colonne, joueur):
    for (dl, dc) in DIRECTIONS:
        total = 1 + compter(grille, ligne, colonne, (dl, dc), joueur) \
                  + compter(grille, ligne, colonne, (-dl, -dc), joueur)
        if total >= 4:
            return True
    return False


def grille_pleine(grille):
    for colonne in range(COLONNES):
        if grille[0][colonne] == 0:
            return False
    return True


def demander_colonne(grille):
    while True:
        texte = input("Colonne (1 à 7) : ")
        if texte.isdigit() and coup_possible(grille, int(texte) - 1):
            return int(texte) - 1
        print("Coup impossible, recommence.")


def copier(grille):
    copie = []
    for ligne in grille:
        copie.append(list(ligne))
    return copie


def partie_au_hasard(grille, joueur):
    while True:
        libres = []
        for colonne in range(COLONNES):
            if coup_possible(grille, colonne):
                libres.append(colonne)
        if len(libres) == 0:
            return 0
        colonne = random.choice(libres)
        ligne = jouer(grille, colonne, joueur)
        if victoire(grille, ligne, colonne, joueur):
            return joueur
        joueur = 3 - joueur


def taux_de_reussite(grille, colonne, joueur, simulations):
    total = 0.0
    for i in range(simulations):
        copie = copier(grille)
        ligne = jouer(copie, colonne, joueur)
        if victoire(copie, ligne, colonne, joueur):
            gagnant = joueur
        else:
            gagnant = partie_au_hasard(copie, 3 - joueur)
        if gagnant == joueur:
            total = total + 1.0
        elif gagnant == 0:
            total = total + 0.5
    return total / simulations


def coup_ia(grille, joueur, simulations):
    adversaire = 3 - joueur
    for essai in [joueur, adversaire]:
        for colonne in range(COLONNES):
            if coup_possible(grille, colonne):
                ligne = jouer(grille, colonne, essai)
                gagne = victoire(grille, ligne, colonne, essai)
                retirer(grille, ligne, colonne)
                if gagne:
                    return colonne

    marge = 1 / math.sqrt(simulations)
    taux = {}
    for colonne in range(COLONNES):
        if coup_possible(grille, colonne):
            taux[colonne] = taux_de_reussite(grille, colonne, joueur, simulations)
    print("Estimations de l'IA (marge d'erreur environ", round(marge, 2), ") :")
    for colonne in taux:
        print("  colonne", colonne + 1, ":", round(taux[colonne], 2))

    meilleur = max(taux.values())
    choix = None
    for colonne in taux:
        if math.isclose(taux[colonne], meilleur, abs_tol=marge):
            if choix is None or abs(colonne - 3) < abs(choix - 3):
                choix = colonne      
    return choix


def demander_niveau():
    print("Niveau de l'IA : 1 facile   2 moyen   3 difficile")
    texte = input("Niveau : ")
    if texte == "1":
        marge = 0.2
    elif texte == "3":
        marge = 0.05
    else:
        marge = 0.1
    return round(1 / marge ** 2)


def partie():
    print("Puissance 4")
    print("1 : deux joueurs   2 : contre l'IA")
    mode = input("Mode : ")
    simulations = 0
    if mode == "2":
        simulations = demander_niveau()
    grille = nouvelle_grille()
    joueur = 1
    while True:
        afficher(grille)
        if mode == "2" and joueur == 2:
            print("L'IA réfléchit (" + str(simulations) + " simulations par colonne)...")
            colonne = coup_ia(grille, joueur, simulations)
            print("L'IA joue la colonne", colonne + 1)
        else:
            print("Joueur", joueur, "(" + SYMBOLES[joueur] + ")")
            colonne = demander_colonne(grille)
        ligne = jouer(grille, colonne, joueur)
        if victoire(grille, ligne, colonne, joueur):
            afficher(grille)
            print("Le joueur", joueur, "gagne !")
            return
        if grille_pleine(grille):
            afficher(grille)
            print("Match nul.")
            return
        joueur = 3 - joueur


try:
    partie()
except EOFError:
    print("\nFin de la saisie.")