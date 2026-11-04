nal · PY
#exercice 1.1
 
import math
 
def vecteur(A, B):
    """Vecteur AB, de A vers B."""
    return (B[0] - A[0], B[1] - A[1])
 
def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]
 
def determinant(u, v):
    """Déterminant de (u, v), aire orientée du parallélogramme qu'ils engendrent."""
    return u[0] * v[1] - u[1] * v[0]
 
def norme(u):
    return math.hypot(u[0], u[1])
 
def angle(u, v):
    """Angle non orienté entre u et v, en degrés.
    atan2 évite l'erreur d'arrondi de acos pour deux vecteurs parallèles."""
    return math.degrees(math.atan2(abs(determinant(u, v)), produit_scalaire(u, v)))
 
print(norme((3, 4)), produit_scalaire((1, 2), (3, 4)))
print(angle((1, 0), (1, 1)), angle((1, 0), (0, 1)))
print(angle((2, 0), (2, 0)))
 
#exercice 1.2
 
def distance_point_droite(P, A, B):
    """Distance de P à la droite (AB) : |AB x AP| / ||AB||."""
    AB = vecteur(A, B)
    AP = vecteur(A, P)
    return abs(determinant(AB, AP)) / norme(AB)
 
print(distance_point_droite((0, 0), (0, 1), (1, 0)), math.sqrt(2) / 2)
print(distance_point_droite((3, 4), (0, 0), (1, 0)))
 
#exercice 2.1
 
def orientation(A, B, C, tolerance=1e-12):
    """1 si A -> B -> C tourne à gauche, -1 à droite, 0 si alignés (à la tolérance près)."""
    AB = vecteur(A, B)
    AC = vecteur(A, C)
    d = determinant(AB, AC)
    if abs(d) <= tolerance * norme(AB) * norme(AC):
        return 0
    return 1 if d > 0 else -1
 
print(orientation((0, 0), (1, 0), (1, 1)))
print(orientation((0, 0), (1, 0), (1, -1)))
print(orientation((0, 0), (1, 1), (2, 2)))
 
# trois points alignés sur y = 3x, mais en flottants le déterminant n'est pas nul
A, B, C = (0.1, 3 * 0.1), (0.2, 3 * 0.2), (0.3, 3 * 0.3)
print(determinant(vecteur(A, B), vecteur(A, C)), orientation(A, B, C))
 
#exercice 2.2
 
def aire_signee(polygone):
    """Formule du lacet, sans valeur absolue : positive si les sommets sont dans le sens direct."""
    somme = 0
    n = len(polygone)
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]       # (i + 1) % n : après le dernier sommet, on revient au premier
        somme = somme + (x1 * y2 - x2 * y1)
    return somme / 2
 
def aire(polygone):
    return abs(aire_signee(polygone))
 
carre = [(0, 0), (1, 0), (1, 1), (0, 1)]
triangle = [(0, 0), (4, 0), (0, 3)]
maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
print(aire(carre), aire(triangle), aire(maison))
print(aire_signee(maison), aire_signee(maison[::-1]))
 
#exercice 3.1
 
def se_coupent(A, B, C, D):
    """Vrai si les segments [AB] et [CD] se croisent franchement.
 
    Les cas dégénérés (trois points alignés) renvoient False.
    """
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    return o1 * o2 < 0 and o3 * o4 < 0
 
print(se_coupent((0, 0), (1, 1), (0, 1), (1, 0)))
print(se_coupent((0, 0), (1, 0), (0, 1), (1, 1)))
print(se_coupent((0, 0), (1, 1), (2, 2), (3, 3)))
 
#exercice 3.2
 
def intersection(A, B, C, D, tolerance=1e-12):
    """Point d'intersection des segments [AB] et [CD], ou None s'ils ne se coupent pas."""
    AB = vecteur(A, B)
    CD = vecteur(C, D)
    AC = vecteur(A, C)
    denominateur = determinant(AB, CD)
    if abs(denominateur) <= tolerance * norme(AB) * norme(CD):
        return None            # parallèles, alignés ou presque
    t = determinant(AC, CD) / denominateur
    u = determinant(AC, AB) / denominateur
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (A[0] + t * AB[0], A[1] + t * AB[1])
    return None
 
print(intersection((0, 0), (2, 2), (0, 2), (2, 0)))
print(intersection((0, 0), (1, 0), (0, 1), (1, 1)))
print(intersection((0, 0), (1, 1), (2, 2), (3, 3)))
 
#exercice 4.1
 
def dedans(P, polygone):
    """Vrai si P est à l'intérieur du polygone, par lancer de rayon horizontal vers la droite."""
    x, y = P
    n = len(polygone)
    traversees = 0
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        # le côté passe de part et d'autre de la hauteur de P
        # (strict d'un côté, large de l'autre : un sommet n'est compté que pour un seul côté)
        if (y1 > y) != (y2 > y):
            x_croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_croisement:
                traversees = traversees + 1
    return traversees % 2 == 1
 
for P in ((1, 1), (1, 2.4), (3, 1), (0.2, 2.2)):
    print(P, dedans(P, maison))
 
# cas limites : un point à la hauteur de sommets, puis des points sur le bord (résultat dépendant de la convention)
print(dedans((1, 1.5), maison), dedans((-1, 1.5), maison), dedans((2.5, 1.5), maison))
print(dedans((1, 0), maison), dedans((2, 1.5), maison))
 
#exercice 4.2
 
import random
 
random.seed(0)
tirages = 200_000
touches = 0
for _ in range(tirages):
    P = (random.uniform(0, 2), random.uniform(0, 2.5))
    if dedans(P, maison):
        touches = touches + 1
 
aire_rectangle = 2 * 2.5
print(aire_rectangle * touches / tirages)
 
#exercice 5.1
 
import matplotlib.pyplot as plt
 
def tracer_polygone(polygone, points=()):
    xs = [s[0] for s in polygone] + [polygone[0][0]]
    ys = [s[1] for s in polygone] + [polygone[0][1]]
    plt.figure(figsize=(5, 5))
    plt.plot(xs, ys, color="black")
    for P in points:
        couleur = "green" if dedans(P, polygone) else "red"
        plt.scatter([P[0]], [P[1]], color=couleur)
    plt.axis("equal")
    plt.title("Vert : dedans, rouge : dehors")
    plt.show()
 
random.seed(1)
nuage = [(random.uniform(-0.5, 2.5), random.uniform(-0.5, 3)) for _ in range(60)]
tracer_polygone(maison, nuage)
 
# une étoile à cinq branches : polygone non convexe
etoile = []
for k in range(10):
    rayon = 2 if k % 2 == 0 else 0.8
    theta = math.pi / 2 + k * math.pi / 5
    etoile.append((rayon * math.cos(theta), rayon * math.sin(theta)))
 
print(round(aire(etoile), 4), round(5 * 2 * 0.8 * math.sin(math.pi / 5), 4))   # lacet, puis formule exacte
print(dedans((0, 0), etoile), dedans((0, 1.5), etoile), dedans((1.2, 1.2), etoile))
tracer_polygone(etoile, [(0, 0), (0, 1.5), (1.2, 1.2), (0, 1.9)])
 
#exercice 6.1
 
def zone_de(P, zones):
    """Indice de la première zone qui contient P, ou None."""
    for indice, zone in enumerate(zones):
        if dedans(P, zone):
            return indice
    return None
 
zones = [maison, [(3, 0), (4, 0), (4, 1), (3, 1)]]
for P in ((1, 1), (3.5, 0.5), (2.5, 0.5)):
    print(P, zone_de(P, zones))
 
