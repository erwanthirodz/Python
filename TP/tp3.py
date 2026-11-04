# exercice 1.1
 
def evaluer_naif(P, x):
    total = 0
    for i in range(len(P)):
        total = total + P[i] * x ** i
    return total
 
 
print(evaluer_naif([2, 3, 0, 5], 2), evaluer_naif([2, 3, 0, 5], 0))
 
 
#exercice 2.1
 
def evaluer(P, x):
    resultat = 0
    for i in range(len(P) - 1, -1, -1):
        resultat = resultat * x + P[i]
    return resultat
 
 
print(evaluer([2, 3, 0, 5], 2), evaluer([], 5))
 
#exercice 2.2
import time

for degre in [1000, 5000, 20000]:
    P = [1] * (degre + 1)
    
    debut = time.perf_counter()
    evaluer_naif(P, 1.0001)
    t_naif = time.perf_counter() - debut
    
    debut = time.perf_counter()
    evaluer(P, 1.0001)
    t_horner = time.perf_counter() - debut
    
    print(t_naif, t_horner)

#exercice 2.3

import time

for degre in [200, 400, 800]:
    P = [1] * (degre + 1)
    
    debut = time.perf_counter()
    for _ in range(5):
        evaluer_naif(P, 3)
    t_naif = time.perf_counter() - debut
    
    debut = time.perf_counter()
    for _ in range(5):
        evaluer(P, 3)
    t_horner = time.perf_counter() - debut
    
    print(t_naif / t_horner, evaluer_naif(P, 3) == evaluer(P, 3))
 
#exercice 3.1
 
def deriver(P):
    derivee = []
    for i in range(1, len(P)):
        derivee.append(i * P[i])
    return derivee
 
 
print(deriver([2, 3, 0, 5]), deriver([7]))
 
#exercice 4.1

def dichotomie(f, a, b, tolerance=1e-12):
    fa, fb = f(a), f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("f(a) et f(b) doivent etre de signes opposes")
    while b - a > tolerance:
        milieu = (a + b) / 2
        if f(a) * f(milieu) <= 0:
            b = milieu
        else:
            a = milieu
    return (a + b) / 2

def carre_moins_deux(x):
    return x * x - 2

print(dichotomie(carre_moins_deux, 0, 2))

#exercice 4.2

def newton(P, depart, tolerance=1e-12, tours_max=100):
    derivee = deriver(P)
    x = float(depart)
    for tour in range(tours_max):
        valeur = evaluer(P, x)
        pente = evaluer(derivee, x)
        if pente == 0:
            raise ZeroDivisionError("tangente horizontale")
        suivant = x - valeur / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            return suivant, tour + 1
        x = suivant
    raise RuntimeError("pas de convergence")

Q = [-5, -2, 0, 1]
print(newton(Q, 2))

#exercice 4.3

def newton_trace(P, depart, tours):
    derivee = deriver(P)
    x = float(depart)
    trajet = [x]
    for _ in range(tours):
        pente = evaluer(derivee, x)
        if pente == 0:
            break
        x = x - evaluer(P, x) / pente
        trajet.append(x)
    return trajet

R = [2, -2, 0, 1]
print(newton_trace(R, 0, 8))


#exercice 4.4
for depart in (2, 1, 0):
    print(newton(Q, depart))
 
 
#exercice 5.1

#L'axe des abscisses n'est coupé q'une fois à environ 2

#exercice 6.1
 
def somme(P, Q):
    n = max(len(P), len(Q))
    resultat = []
    for i in range(n):
        a = P[i] if i < len(P) else 0
        b = Q[i] if i < len(Q) else 0
        resultat.append(a + b)
    return resultat
 
 
def produit_poly(P, Q):
    if len(P) == 0 or len(Q) == 0:
        return []
    resultat = [0] * (len(P) + len(Q) - 1)
    for i in range(len(P)):
        for j in range(len(Q)):
            resultat[i + j] = resultat[i + j] + P[i] * Q[j]
    return resultat
 
 
print(somme([1, 2], [0, 0, 3]), produit_poly([1, 1], [1, 1]), produit_poly([-1, 1], [1, 1]))

#exercice 6.2

binome = [1]
for i in range(10):
    binome = produit_poly(binome, [1, 1])
print(binome, sum(binome) == 2 ** 10)
 
 
#exercice 7.1

import math

def derivee_avant(f, x, h):
    return (f(x + h) - f(x)) / h
 
 
def derivee_centree(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)
 
 
exacte = math.cos(1.0)
for h in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12):
    e_avant = abs(derivee_avant(math.sin, 1.0, h) - exacte)
    e_centree = abs(derivee_centree(math.sin, 1.0, h) - exacte)
    print(f"h = {h:.0e} : avant {e_avant:.1e} | centree {e_centree:.1e}")
 
 
#exercice 8.1
 
def rectangles(f, a, b, n):
    h = (b - a) / n
    total = 0
    for i in range(n):
        total = total + f(a + i * h)
    return h * total
 
 
def trapezes(f, a, b, n):
    h = (b - a) / n
    total = (f(a) + f(b)) / 2
    for i in range(1, n):
        total = total + f(a + i * h)
    return h * total
 
 
def simpson(f, a, b, n):
    if n % 2 == 1:
        n = n + 1
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        if i % 2 == 1:
            total = total + 4 * f(a + i * h)
        else:
            total = total + 2 * f(a + i * h)
    return h / 3 * total
 
 
def carre(x):
    return x * x
 

for n in (10, 100, 1000):
    e_rect = abs(rectangles(carre, 0, 1, n) - 1 / 3)
    e_trap = abs(trapezes(carre, 0, 1, n) - 1 / 3)
    e_simp = abs(simpson(carre, 0, 1, n) - 1 / 3)
    print(f"n = {n:>4} : rectangles {e_rect:.1e} | trapezes {e_trap:.1e} | simpson {e_simp:.1e}")

#exercice 8.2
 
def arctangente_derivee(x):
    return 4 / (1 + x * x)

approx_trap = trapezes(arctangente_derivee, 0, 1, 1000)
approx_simp = simpson(arctangente_derivee, 0, 1, 1000)
print(approx_trap, abs(approx_trap - math.pi))
print(approx_simp, abs(approx_simp - math.pi))