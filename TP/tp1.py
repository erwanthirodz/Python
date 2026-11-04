
# Exercice 1.1 

a = 2026
b = 7
quotient = a // b
reste = a % b
print(quotient, reste)
print(quotient * b + reste == a)
 
# Exercice 1.2 

a = 123456789
print(a % 10)
print(a // 10)
 
 
# Exercice 2.1 : 

t = 0.0
for i in range(1000):
    t = t + 0.1
print(t)
print(t - 100)
 
 
# Exercice 2.2 : 

def presque_egaux(a, b):
    ecart = 1e-3
    r = abs(a - b) <= ecart
    return r

print(presque_egaux(0.1 + 0.2, 0.3))
print(presque_egaux(1.0, 1.5))
 
# Exercice 3.1 : 

for i in range(1, 11):
    r = i*7
    print(i, "x", 7, "=", r)
 
# Exercice 3.2 : 

a = 100
t = 0
for i in range(1, n + 1):
    total = total + i
print(t)

# Exercice 4.1 : 
 
def nombre_de_chiffres(n):
    t = 0
    while t != len(str(n)):
        t = t + 1
    return t

print(nombre_de_chiffres(2026))
print(nombre_de_chiffres(7))

# Exercice 5.1 :  
 
import math

def heron(a, tolerance=1e-12):
    """Racine carrée de a par la méthode de Héron."""
    if a < 0:
        raise ValueError("pas de racine carrée réelle pour un nombre négatif")
    if a == 0:
        return 0.0
    x = float(a)
    tours = 0
    while True:
        suivant = 0.5 * (x + a / x)
        tours = tours + 1
        if abs(suivant - x) <= tolerance * abs(suivant):
            return suivant
        x = suivant

print(heron(2))
print(math.sqrt(2))
print(abs(heron(2) - math.sqrt(2)) < 1e-12)
 
# Exercice 6.1 : 

def vers_binaire(n):
    while n > 0:
        if n%2 == 0:
          print("0")
        else:
            print("1")  
        n = n//2

print(vers_binaire(0))
print(vers_binaire(37))

# Exercice 6.2 : epsilon machine

import sys

eps = 1.0
while (1.0 + eps) / 2 != 1.0:
    eps = eps / 2

print(eps)
print(sys.float_info.epsilon) 
 
# Exercice 7.1 : 

import math

def racines_naif(a, b, c):
    """Racines réelles de ax² + bx + c par la formule classique."""
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine réelle")
    r = math.sqrt(delta)
    return (-b - r) / (2 * a), (-b + r) / (2 * a)

petite, grande = racines_naif(1.0, -1e8, 1.0)
print(petite, grande)
print("produit :", petite * grande, "attendu : 1")
 
# Exercice 7.2 : 

def racines(a, b, c):
    """Racines réelles de ax² + bx + c, sans élimination catastrophique."""
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine réelle")
    r = math.sqrt(delta)
    # on choisit le signe qui additionne au lieu de soustraire
    if b >= 0:
        sure = (-b - r) / (2 * a)
    else:
        sure = (-b + r) / (2 * a)
    autre = c / (a * sure)
    return min(sure, autre), max(sure, autre)

petite, grande = racines(1.0, -1e8, 1.0)
print(petite, grande)
print("produit :", petite * grande)
for x in (petite, grande):
    residu = x * x - 1e8 * x + 1
    print(f"residu : {residu:.1e}, soit {residu / max(x * x, 1.0):.1e} en relatif")
 
# Exercice 7.3 : 

total = Fraction(0)
for _ in range(1000):
    total = total + Fraction(1, 10)
print(total, total == 100)
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))
