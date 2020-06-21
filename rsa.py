import random
from math import gcd


class RSA:

    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.public = {}
        self.private = {}
        self.n = None
        self.phi = None
        self.e = None
        self.d = None
        self.private = {}
        self.public = {}

    def generate_keys(self):
        self.private["n"] = self.n
        self.private["d"] = self.d
        self.public["n"] = self.n
        self.public["e"] = self.e

    def calulate_phi(self):
        self.phi = (self.p - 1)*(self.q - 1)

    def calculate_n(self):
        self.n = self.p * self.q

    # Rozszerzony algorytm Euklidesa
    def egcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = self.egcd(b % a, a)
            return g, x - (b // a) * y, y

    def find_e(self):
        matches = []
        for e in range(2, self.phi):
            if gcd(e, self.phi) == 1:
                matches.append(e)

        return matches

    def modinv(self):
        g, x, y = self.egcd(self.e, self.phi)
        if g != 1:
            raise Exception('Odwrotnosc modularna nie istnieje')
        else:
            self.d = x % self.phi

    def encrypt(self, message):
        c = [pow(ord(char), self.public["e"], self.public["n"]) for char in message]
        return c

    def decrypt(self, cyphertext):
        m = [chr(pow(char, self.private["d"], self.private["n"])) for char in cyphertext]
        return ''.join(m)


def generate_primes():
    primes = []

    for number in range(1000, 10000):
        is_prime = True
        for divider in range(2, int(number**0.5) + 1):
            if number % divider == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(number)

    while True:
        p = primes[random.randint(0, len(primes))]
        q = primes[random.randint(0, len(primes))]

        if p != q:
            return p, q


def is_prime(number):
    if number <= 1:
        return False

    for divider in range(2, int(number**0.5)+1):
        if number % divider == 0:
            return False

    return True



def main():
    print(
        """Ten program zaprezentuje działanie algorytmu RSA
    
        Pierwszym krokiem w celu wygenerowania klucza publicznego i prywatnego jest wybranie dwóch dużych liczb pierwszych p i q
        1. Chce je wybrać sam
        2. Wygeneruj je automatycznie""")

    while True:
        while True:
            try:
                choice = int(input(">>>"))
                break
            except ValueError:
                print("wpisz cyfrę odpowiadającą pozycji w menu")

        if choice == 1:
            while True:
                try:
                    p = int(input("p: "))
                    if is_prime(p):
                        break
                    else:
                        print(f"Liczba {p} nie jest liczbą pierwszą")

                except ValueError:
                    print("Wprowadzona wartość nie jest poprawna, spróbuj jeszcze raz")

            while True:
                try:
                    q = int(input("q: "))
                    if p != q:
                        if is_prime(q):
                            break
                        else:
                            print(f"Liczba {q} nie jest liczbą pierwszą")
                    else:
                        print("p i q nie mogą być równe")

                except ValueError:
                    print("Wprowadzona wartość nie jest poprawna, spróbuj jeszcze raz")

            break

        elif choice == 2:
            p, q = generate_primes()
            print(f"Wybrane liczby pierwsze to p: {p} q: {q}")
            break

        else:
            print("To nie jest poprawny wybór spróbuj jeszcze raz")

    input("\nNaciśnij enter żeby kontynuować...")

    rsa = RSA(p, q)
    rsa.calculate_n()
    print("\nTeraz trzeba obliczyć n = p*q")
    print(f"{rsa.p} * {rsa.q} = {rsa.n}")

    input("\nNaciśnij enter żeby kontynuować...")

    print("\nNastępnie obliczamy phi(n)=(p-1)(q-1)")
    rsa.calulate_phi()
    print(f"({rsa.p}-1) * ({rsa.q}-1) = {rsa.phi}")

    input("\nNaciśnij enter żeby kontynuować...")

    print("\nNastępnie wybieramy liczbę e taką, że 1 < e < phi(n), względnie pierwszą z phi(n)")
    print("Znalazłem już klika takich liczb, wybierz jedną z nich lub inną spełniającą powyższe warunki")
    list_of_e = rsa.find_e()
    print(list_of_e[-10:-1])

    while True:
        try:
            e = int(input("e: "))
            if e in list_of_e:
                rsa.e = e
                break
            else:
                print(f"Ta liczba nie jest wzglęgnie pierwsza z phi(n) = {rsa.phi}")

        except ValueError:
            print("To nie jest poprawna wartość, spróbuj jeszcze raz")

    input("\nNaciśnij enter żeby kontynuować...")

    print("\nTeraz obliczamy d takiej, że d = e^-1 mod phi(n)")
    rsa.modinv()
    print(f"{rsa.e}^-1 mod {rsa.phi} = {rsa.d}")

    input("\nNaciśnij enter żeby kontynuować...")

    rsa.generate_keys()
    print(f"\nKlucz prywatny to para {rsa.private} i nie należy go nikomu ujawniać")
    print(f"Klucz publiczny to para {rsa.public} i służy do szyfrowania wiadomości przez nadawce")

    input("\nNaciśnij enter żeby kontynuować...")

    print("Żeby zaszyfrować wiadomość dzielimy ją na bloki (m) mniejsze od n i korzystamy ze wzoru c = m^e mod n")
    print("Podaj wiadomość do zaszyfrowania")
    message = input(">>>")
    ciphertext = rsa.encrypt(message)
    print(f"Szyfrogram: {ciphertext}")

    input("\nNaciśnij enter żeby kontynuować...")

    print("W celu odszyfrowania szyfrogramu korzystamy ze wzoru m = c^d mod n")
    decrypted = rsa.decrypt(ciphertext)
    print(f"Odszyfrowana wiadomość: {decrypted}")


if __name__ == "__main__":
    main()


