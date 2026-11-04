#exercice 1.1
 
def transposee(A):
    resultat = []
    for j in range(len(A[0])):
        colonne = []
        for i in range(len(A)):
            colonne.append(A[i][j])
        resultat.append(colonne)
    return resultat
 
 
print(transposee([[1, 2, 3], [4, 5, 6]]))
 
#exercice 2.1
 
def produit(A, B):
    if len(A[0]) != len(B):
        print("dimensions incompatibles")
        return None
    resultat = []
    for i in range(len(A)):
        ligne = []
        for j in range(len(B[0])):
            c = 0
            for k in range(len(B)):
                c = c + A[i][k] * B[k][j]
            ligne.append(c)
        resultat.append(ligne)
    return resultat
 
 
A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
print(produit([[1, 2], [3, 4]], [[0, 1], [1, 0]]))
produit([[1, 2]], [[1, 2]])

#exercice 2.2

import random
import time

random.seed(42)

def matrice_aleatoire(n):
    return [[random.random() for _ in range(n)] for _ in range(n)]

for n in (40, 80, 120):
    A = matrice_aleatoire(n)
    B = matrice_aleatoire(n)
    debut = time.perf_counter()
    produit(A, B)
    print(f"n = {n:>3} : {time.perf_counter() - debut:.4f} s")
 
 
#exercice 3.1

import numpy as np
 
a = 120
X = matrice_aleatoire(n)
Y = matrice_aleatoire(n)
debut = time.perf_counter()
produit(A, B)
t_python = time.perf_counter() - debut
An, Bn = np.array(A), np.array(B)
debut = time.perf_counter()
An @ Bn
t_numpy = time.perf_counter() - debut
print(f"python pur {t_python:.4f} s")
print(f"numpy      {t_numpy:.6f} s")
print("rapport :", round(t_python / max(t_numpy, 1e-9)))
 
 
#exercice 4.1
 
def resoudre(A, b, tolerance=1e-14):
    n = len(A)
    M = []
    for i in range(n):
        M.append(list(A[i]) + [b[i]])
    for k in range(n):
        p = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[p][k]):
                p = i
        if abs(M[p][k]) <= tolerance:
            print("système singulier ou mal posé")
            return None
        M[k], M[p] = M[p], M[k]
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] = M[i][j] - f * M[k][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        reste = M[i][n]
        for j in range(i + 1, n):
            reste = reste - M[i][j] * x[j]
        x[i] = reste / M[i][i]
    return x
 
#exercice 4.2

import numpy as np
import random

random.seed(7)
n = 50
A = matrice_aleatoire(n)
b = [random.random() for _ in range(n)]

mienne = resoudre(A, b)
celle_de_numpy = np.linalg.solve(np.array(A), np.array(b))

ecart = max(abs(mienne[i] - celle_de_numpy[i]) for i in range(n))
print("ecart maximal :", ecart)
print(ecart < 1e-9)
 
 
# exercice 5.1

#on constate que la méthode np.linalg.solve(H, b) donne des résultats nettement 
#meilleurs que l'utilisation de l'inverse np.linalg.inv(H) @ b
 
 
#exercice 6.1

import matplotlib.pyplot as plt

def rotation(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]])

# une maison, comme suite de points (fermée)
maison = np.array([[0, 0], [2, 0], [2, 1.5], [1, 2.5], [0, 1.5], [0, 0]]).T

plt.figure(figsize=(5, 5))
plt.plot(maison[0], maison[1], label="depart")
for angle in (np.pi / 6, np.pi / 3, np.pi / 2):
    image = rotation(angle) @ maison
    plt.plot(image[0], image[1], label=f"rotation {int(np.degrees(angle))} degres")
plt.axis("equal")
plt.legend()
plt.title("Une matrice fait tourner une figure")
plt.show()

gauche = rotation(np.pi / 3) @ rotation(np.pi / 6)
droite = rotation(np.pi / 2)
print(np.allclose(gauche, droite))
print(np.round(droite, 10))
 
# exercice7.1
 
import numpy as np

def determinant(A):
    n = len(A)
    M = [list(ligne) for ligne in A]
    det = 1.0
    for k in range(n):
        meilleure = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[meilleure][k]) < 1e-14:
            return 0.0
        if meilleure != k:
            M[k], M[meilleure] = M[meilleure], M[k]
            det = -det
        det = det * M[k][k]
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] = M[i][j] - facteur * M[k][j]
    return det

A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
print(determinant(A), float(np.linalg.det(np.array(A, dtype=float))))
print(determinant([[1, 2], [2, 4]]))
 
 
#exercice 8.1
 
from fractions import Fraction
import numpy as np

def hilbert_exacte(n):
    return [[Fraction(1, i + j + 1) for j in range(n)] for i in range(n)]

n = 12
H_exacte = hilbert_exacte(n)
b_exact = [sum(ligne) for ligne in H_exacte]

# Le premier essai échoue si la tolérance par défaut est trop élevée
try:
    resoudre(H_exacte, b_exact)
except ValueError as erreur:
    print("Premier essai échoué :", erreur)

# Solution avec tolérance à 0 pour les fractions exactes
x_exact = resoudre(H_exacte, b_exact, tolerance=0)
print("Solution exacte :", x_exact)
print("Tous les éléments valent 1 :", all(v == 1 for v in x_exact))

#exercice 9.1

import numpy as np

def translation(tx, ty):
    return np.array([[1.0, 0.0, tx],
                     [0.0, 1.0, ty],
                     [0.0, 0.0, 1.0]])

def rotation_h(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0.0],
                     [s, c, 0.0],
                     [0.0, 0.0, 1.0]])

point = np.array([1.0, 0.0, 1.0])
T = translation(3, 1)
R = rotation_h(np.pi / 2) # Rotation de 90°

print("Translation puis rotation :", np.round(R @ T @ point, 10))   
print("Rotation puis translation :", np.round(T @ R @ point, 10))