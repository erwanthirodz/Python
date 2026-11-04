#exercice 1.1

def lettre_vers_nombre(c):
    return ord(c) - ord("A")

def nombre_vers_lettre(n):
    return chr(n % 26 + ord("A"))

print(lettre_vers_nombre("C"), nombre_vers_lettre(2))
print([nombre_vers_lettre(lettre_vers_nombre(c)) == c for c in "ABCXYZ"])

#exercice 1.2

import unicodedata

def nettoyer(texte):
    decompose = unicodedata.normalize("NFD", texte.upper())   
    return "".join(c for c in decompose if "A" <= c <= "Z")   

print(nettoyer("Été, à Paris !"))

#exercice 2.1

def chiffrer(texte, a, b):
    return "".join(nombre_vers_lettre(a * lettre_vers_nombre(c) + b) for c in nettoyer(texte))

message = "ATTAQUEALAUBE"
print(chiffrer(message, 5, 8), chiffrer(message, 1, 3))

#exercice 3.1

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

valides = [a for a in range(1, 26) if pgcd(a, 26) == 1]
print(valides)
print(len(valides), "valeurs possibles pour a,", len(valides) * 26, "clés au total")

#exercice 3.2

def euclide_etendu(a, b):
    r0, r1 = a, b
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return r0, u0, v0

def inverse_modulaire(a, n):
    """Inverse de a modulo n (par Euclide étendu, comme au TP2), ou erreur s'il n'existe pas."""
    g, u, v = euclide_etendu(a % n, n)
    if g != 1:
        raise ValueError(f"{a} n'est pas inversible modulo {n}")
    return u % n

print(inverse_modulaire(5, 26), (5 * 21) % 26)
for a in (4, 13):
    try:
        inverse_modulaire(a, 26)
    except ValueError as erreur:
        print("erreur attendue :", erreur)

#exercice 4.1

def dechiffrer(texte, a, b):
    """Déchiffrement affine : x = a^-1 (y - b) mod 26. Refuse les clés non inversibles."""
    a_inverse = inverse_modulaire(a, 26)
    return "".join(nombre_vers_lettre(a_inverse * (lettre_vers_nombre(c) - b)) for c in nettoyer(texte))

message = nettoyer("Attaque a l'aube")
secret = chiffrer(message, 5, 8)
print(secret, dechiffrer(secret, 5, 8))

# test aller-retour sur toutes les clés valides (12 x 26 = 312)
print(all(dechiffrer(chiffrer(message, a, b), a, b) == message for a in valides for b in range(26)))

# une clé invalide est refusée au lieu de donner un résultat faux
try:
    dechiffrer(secret, 4, 7)
except ValueError as erreur:
    print("clé refusée :", erreur)

#exercice 5.1

def toutes_les_clefs(secret):
    """Tous les déchiffrements possibles, sous forme de triplets (a, b, texte)."""
    return [(a, b, dechiffrer(secret, a, b)) for a in valides for b in range(26)]

essais = toutes_les_clefs(secret)
print(len(essais), "clés essayées")
bonnes = [(a, b) for a, b, texte in essais if texte == message]
print("clé retrouvée :", bonnes)

#exercice 6.1

from collections import Counter

texte_long = nettoyer(
    "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
    "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
    "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
    "le code sans essayer toutes les clefs possibles. Pendant la seconde guerre "
    "mondiale, des equipes de mathematiciens et de linguistes reunies a Bletchley Park "
    "ont lu des milliers de messages ennemis grace a des regularites statistiques que "
    "les operateurs ne soupconnaient pas. Une langue n'est jamais distribuee au hasard : "
    "certaines lettres reviennent sans cesse, d'autres presque jamais, et un chiffrement "
    "qui conserve ces proportions laisse a l'adversaire une empreinte facile a reconnaitre. "
    "Les systemes modernes sont donc concus pour que le message chiffre ressemble a une "
    "suite de symboles tires au hasard, sans la moindre trace de la langue d'origine, "
    "de sorte qu'aucune analyse de frequences ne puisse plus guider la recherche. "
    "La securite repose alors sur la taille de l'espace des clefs et sur la solidite "
    "des operations mathematiques employees, pas sur le secret de la methode elle-meme."
)
secret_long = chiffrer(texte_long, 7, 12)

def candidats(secret, lettres_chiffre, lettre_clair="E"):
    """Clés (a, b, texte) qui envoient lettre_clair sur l'une des lettres_chiffre."""
    x = lettre_vers_nombre(lettre_clair)
    resultat = []
    for lettre in lettres_chiffre:
        cible = lettre_vers_nombre(lettre)
        for a in valides:
            b = (cible - a * x) % 26          # a x + b = cible
            resultat.append((a, b, dechiffrer(secret, a, b)))
    return resultat

plus_frequente = Counter(secret_long).most_common(1)[0][0]
print("lettre la plus fréquente du chiffré :", plus_frequente)
cands = candidats(secret_long, plus_frequente)
print(len(cands), "candidats au lieu de 312")
print("clé trouvée :", [(a, b) for a, b, texte in cands if texte == texte_long])

# sur le message court, la lettre la plus fréquente n'est pas l'image de E :
# avec si peu de lettres (13), les fréquences observées n'ont rien à voir avec celles du français
secret_court = chiffrer("ATTAQUEALAUBE", 5, 8)
frequente_court = Counter(secret_court).most_common(1)[0][0]
print(secret_court, "lettre la plus fréquente :", frequente_court)
print((5, 8) in [(a, b) for a, b, texte in candidats(secret_court, frequente_court)])

# on teste alors les 3 lettres les plus fréquentes du chiffré contre E, A et S : 9 hypothèses
trois = [lettre for lettre, n in Counter(secret_court).most_common(3)]
neuf = []
for lettre_clair in "EAS":
    neuf = neuf + candidats(secret_court, trois, lettre_clair)
print((5, 8) in [(a, b) for a, b, texte in neuf], len(neuf), "candidats")

# pour aller plus loin : on note chaque candidat par sa ressemblance avec le français
FREQ_FR = [7.64, 0.90, 3.26, 3.67, 14.72, 1.07, 0.87, 0.74, 7.53, 0.55, 0.05, 5.46, 2.97,
           7.10, 5.80, 2.52, 1.36, 6.69, 7.95, 7.24, 6.31, 1.84, 0.04, 0.43, 0.13, 0.33]

def score(texte):
    """Moyenne des fréquences françaises des lettres du texte : plus c'est haut, plus ça ressemble."""
    return sum(FREQ_FR[lettre_vers_nombre(c)] for c in texte) / len(texte)

meilleur = max(cands, key=lambda cand: score(cand[2]))
print("meilleur candidat :", meilleur[0], meilleur[1], meilleur[2][:40])

#exercice 7.1

import random

def indice_coincidence(texte):
    """Probabilité que deux lettres tirées au hasard dans le texte coïncident."""
    N = len(texte)
    return sum(n * (n - 1) for n in Counter(texte).values()) / (N * (N - 1))

random.seed(1)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
hasard = "".join(random.choice(alphabet) for _ in range(len(texte_long)))
print(f"clair  : {indice_coincidence(texte_long):.4f}")
print(f"affine : {indice_coincidence(secret_long):.4f}")
print(f"hasard : {indice_coincidence(hasard):.4f}")

#exercice 8.1

def vigenere(texte, cle):
    """Chaque lettre est décalée du rang de la lettre de la clé en face."""
    return "".join(nombre_vers_lettre(lettre_vers_nombre(c) + lettre_vers_nombre(cle[i % len(cle)]))
                   for i, c in enumerate(nettoyer(texte)))

secret_vigenere = vigenere(texte_long, "CLE")
print(secret_vigenere[:40])
print(f"IC vigenère : {indice_coincidence(secret_vigenere):.4f}")

#exercice 8.2

for L in range(1, 8):
    colonnes = [secret_vigenere[i::L] for i in range(L)]
    moyenne = sum(indice_coincidence(col) for col in colonnes) / L
    print(f"L = {L} : indice moyen {moyenne:.4f}")

