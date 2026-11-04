#exercice 1.1
 
def diviseurs(n):
    liste = []
    for d in range(1, n + 1):
        if n % d == 0:
            liste.append(d)
    return liste
 
print("1.1 ->", diviseurs(28), diviseurs(97))
 
#exercice 2.1
 
def pgcd_naif(a, b):
    d = min(a, b)
    while a % d != 0 or b % d != 0:
        d = d - 1
    return d
 
def pgcd(a, b):
    while b != 0:
        reste = a % b
        a = b
        b = reste
    return a

print(pgcd_naif(1071, 462), pgcd(1071, 462))

#exercice 3.1
 
def est_premier_naif(n):
    """Teste la primalité en essayant tous les diviseurs jusqu'à n - 1."""
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True

print(est_premier_naif(97), est_premier_naif(91))
 
 
def est_premier(n):
    """Teste la primalité en s'arrêtant à la racine carrée de n."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d = d + 2
    return True

print(est_premier(97), est_premier(91), est_premier(2), est_premier(1))

import time

def duree(fonction, argument):
    """Renvoie le temps d'exécution de fonction(argument), en secondes."""
    debut = time.perf_counter()
    fonction(argument)
    return time.perf_counter() - debut

n = 1_000_003  # un nombre premier
print(f"naif        : {duree(est_premier_naif, n):.4f} s")
print(f"jusqu'a rac : {duree(est_premier, n):.6f} s")

for n in [10007, 100003, 1000003]:
    debut = time.time()
    est_premier_naif(n)
    temps_naif = time.time() - debut
 
    debut = time.time()
    est_premier(n)
    temps_racine = time.time() - debut
 
print(round(temps_naif, 5), round(temps_racine, 6), "s")
print(est_premier(1000000000039)) 
#exercice 4.1
 
def crible(limite):
    """Renvoie la liste des nombres premiers de 2 à limite inclus."""
    est_premier_tab = [True] * (limite + 1)
    est_premier_tab[0] = False
    if limite >= 1:
        est_premier_tab[1] = False
    d = 2
    while d * d <= limite:
        if est_premier_tab[d]:
            for multiple in range(d * d, limite + 1, d):
                est_premier_tab[multiple] = False
        d = d + 1
    return [n for n in range(limite + 1) if est_premier_tab[n]]

premiers = crible(100)
print(premiers)
print(len(premiers), "premiers jusqu'a 100")
 
 
debut = time.time()
premiers = crible(100000)
temps_crible = time.time() - debut
 
debut = time.time()
un_par_un = []
for n in range(100001):
    if est_premier(n):
        un_par_un.append(n)
temps_un_par_un = time.time() - debut
 
print(len(premiers), round(temps_crible, 4), round(temps_un_par_un, 4))
print( premiers == un_par_un)
 
 
#exercice 5.1
 
def facteurs(n):
    resultat = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            resultat.append(d)
            n = n // d
        d = d + 1
    if n > 1:
        resultat.append(n)
    return resultat
 
 
print(facteurs(360), facteurs(14), facteurs(97), facteurs(1))

#exercice 6.1
 
def fibonacci_recursif(n):
    """F(n) en suivant la définition, par récurrence."""
    if n < 2:
        return n
    return fibonacci_recursif(n - 1) + fibonacci_recursif(n - 2)

print([fibonacci_recursif(n) for n in range(15)])

temps = {}
for n in [20, 25, 30]:
    debut = time.time()
    fibonacci_recursif(n)
    temps[n] = time.time() - debut
    print(str(n) + round(temps[n], 4))
print(str(round(temps[25] / temps[20])), ", x" + str(round(temps[30] / temps[25])))
 
#exercice 6.2

appels = {}

def fibonacci_compte(n):
    appels[n] = appels.get(n, 0) + 1
    if n < 2:
        return n
    return fibonacci_compte(n - 1) + fibonacci_compte(n - 2)

resultat = fibonacci_compte(30)
print(resultat)
print(appels[1])
print(sum(appels.values()))

#exercice 6.3

def fibonacci(n):
    a = 0
    b = 1
    for i in range(n):
        a, b = b, a + b
    return a
 
 
debut = time.time()
fibonacci(30)
temps_boucle = time.time() - debut
grand = fibonacci(10000)
print(round(temps_boucle, 7), len(str(grand)))
 
#exercice 7.1
 
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

#exercice 7.2
 
def puissance_mod_naive(a, e, n):
    """a^e mod n, par e multiplications successives."""
    resultat = 1
    for _ in range(e):
        resultat = resultat * a % n
    return resultat

def puissance_mod(a, e, n):
    """a^e mod n, par élévations au carré successives."""
    resultat = 1
    a = a % n
    while e > 0:
        if e % 2 == 1:
            resultat = resultat * a % n
        a = a * a % n
        e = e // 2
    return resultat

a, e, n = 7, 10 ** 7, 1_000_003
print(puissance_mod(a, e, n), pow(a, e, n))

debut = time.perf_counter()
puissance_mod_naive(a, e, n)
t_naive = time.perf_counter() - debut
debut = time.perf_counter()
puissance_mod(a, e, n)
t_rapide = time.perf_counter() - debut
print(f"naive {t_naive:.3f} s | rapide {t_rapide:.6f} s")
 