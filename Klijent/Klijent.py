import sys
import os #clear console
import time #sleep
import getpass #password
import re #password valid
from socket import * #soket
from tqdm import tqdm #progressBar
from random import randint #randomNumber

# Progress bar - finish
def progressBar(sekunde):
    with tqdm(total = 100) as progressBar:
        for i in range(10):
            time.sleep(sekunde/10)
            progressBar.update(10)

# Konekcija - finish
def konekcijaSaServerom():
    for i in range(3):
        try:
            adresaServera = 'localhost'
            portServera = 10001
            print('Povezivanje sa serverom na adresi: ' + str(adresaServera) + ' i portu: ' + str(portServera))
            progressBar(randint(0,5))
            klijentSoket = socket(AF_INET, SOCK_STREAM)
            klijentSoket.connect((adresaServera, portServera))
            return klijentSoket, adresaServera, portServera
        except:
            print('Greska prilikom konekcije...')
            print('Program ce automatski pokusati za 3 sekunde...')
            time.sleep(3)
    if i == 2:
        print('Neuspesna konekcija...')
        time.sleep(3)
        iskljucivanje()

# Exit - finish
def iskljucivanje():
    for i in [5, 4, 3, 2, 1]:
        print('Iskljucivanje.....  ' + str(i) + 's')
        time.sleep(1)
        os.system('cls')
    sys.exit(0)

# ProveraSifre -
def proveraSifre(sifra):
    if len(sifra) < 8:
        return False
    elif not re.search("[A-Z]", sifra):
        return False
    elif not re.search("[0-9]", sifra):
        return False
    return True

def main():
    klijentSoket, adresaServera, portServera = konekcijaSaServerom()
    time.sleep(3)
    os.system('cls')
    meni = klijentSoket.recv(4096).decode()
    operacije = ['+', '-', '*', '/']
    op = ['+', '-', '*', '/']
    imeKlijenta = ''
    try:
        while True:
            print(meni)
            odgovor = input('\nOdgovor: ')
            os.system('cls')
            klijentSoket.send(odgovor.encode())
            # Prijava - finish
            if (odgovor == '1'):
                while True:
                    korImeISifra = [input('Unesite korisnicko ime: '), getpass.getpass(prompt='Unesite sifru: ')]
                    imeKlijenta = korImeISifra[0]
                    klijentSoket.send(korImeISifra[0].encode())
                    klijentSoket.send(korImeISifra[1].encode())
                    if klijentSoket.recv(4096).decode() == '1':
                        print('Prijava na korisnicko ime -> ' + korImeISifra[0] + '\nSacekajte . . .')
                        progressBar(3)
                        os.system('cls')
                        odgovor = 'MeniKorisnik'
                        break
                    else:
                        os.system('cls')
                        print('Neuspesno ste se prijavili sa korisnickim imenom -> ' + korImeISifra[0] + '\nPokusajte ponovo!\n')
            # MeniKorisnik - finish
            if (odgovor == 'MeniKorisnik'):
                while True:
                    operacija = input('Korisnik prijavljen kao: ' + imeKlijenta + '\n\n1. Sabiranje\n2. Oduzimanje\n3. Mnozenje\n4. Deljenje\n5. Unesite izraz\n6. Istorija izraza\n7. Izlogujte se\n\nOdgovor: ')
                    os.system('cls')
                    klijentSoket.send(operacija.encode())
                    # Operacija - finish
                    if (operacija == '1' or operacija == '2' or operacija == '3' or operacija == '4'):
                        izraz = input('Unesite izraz: ')
                        klijentSoket.send(operacije[int(operacija)-1].encode())
                        klijentSoket.send(izraz.encode())
                        resenje = klijentSoket.recv(4096).decode()
                        print(resenje)
                        continue
                    # Izrazi - finish
                    if (operacija == '5'):
                        while True:
                            izraz = input('Unesite izraz: ')
                            provera = 0
                            if len(izraz) < 3:
                                print('Niste lepo uneli izraz.. Pokusajte ponovo!')
                                continue
                            for i in operacije:
                                if (izraz.count(i) != 0):
                                    klijentSoket.send(str(i).encode())
                                    klijentSoket.send(izraz.encode())
                                    provera = 1
                                    break
                            if provera == 0:
                                print('Niste lepo uneli izraz.. Pokusajte ponovo!')
                            else: break
                        resenje = klijentSoket.recv(4096).decode()
                        print(resenje)
                        continue
                    # Istorija - finish
                    if (operacija == '6'):
                        izrazi = klijentSoket.recv(4096).decode()
                        if (len(izrazi) != 0):
                            izrazi = izrazi.replace('x', '\n')
                        # upis u fajl - finish
                        f = open(imeKlijenta + ".txt", "w+")
                        f.write(izrazi)
                        f.close()
                        print('Preuzimanje fajla . . .')
                        progressBar(2)
                        print('Fajl je preuzet pod nazivom: ' + imeKlijenta + '.txt')
                        continue
                    # Logout - finish
                    if (operacija == '7'): break
            # Gost - finish
            if (odgovor == '2'):
                p = 0
                while True:
                    operacija = input('Korisnik prijavljen kao: Gost\nImate maksimalno 3 kalkulacije kao gost!\n\n1. Unesite izraz\n2. Izlogujte se\n\nOdgovor: ')
                    os.system('cls')
                    p = p + 1
                    # Max 3 kalk - finish
                    if (p == 4):
                        print('Iskoristili ste 3 kalkulcaije... Sledi povratak na meni...\nRegistrujte se...')
                        time.sleep(3)
                        operacija = '2'
                        os.system('cls')
                    klijentSoket.send(operacija.encode())
                    # Izrazi - finish
                    if (operacija == '1'):
                        while True:
                            izraz = input('Unesite izraz: ')
                            provera = 0
                            if len(izraz) < 3:
                                print('Niste lepo uneli izraz.. Pokusajte ponovo!')
                                continue
                            for i in operacije:
                                if (izraz.count(i) != 0):
                                    klijentSoket.send(str(i).encode())
                                    klijentSoket.send(izraz.encode())
                                    provera = 1
                                    break
                            if provera == 0:
                                print('Niste lepo uneli izraz.. Pokusajte ponovo!')
                            else: break
                        resenje = klijentSoket.recv(4096).decode()
                        print(resenje)
                        continue
                    # Logout - finish
                    if (operacija == '2'): break
                    else: continue
            # Registracija - finish
            if (odgovor == '3'):
                while True:
                    korImeISifra = [input('Unesite korisnicko ime: '), getpass.getpass(prompt='Unesite sifru: ')]
                    imeKlijenta = korImeISifra[0]
                    if not proveraSifre(korImeISifra[1]):
                        print('Sifra se mora sastojati iz minimum 8 karaktera, minimum jednog velikog slova'
                              '(A-Z) i minimum jednog broja (0-9)\nPokusajte ponovo!\n')
                        continue
                    klijentSoket.send(korImeISifra[0].encode())
                    klijentSoket.send(korImeISifra[1].encode())
                    if klijentSoket.recv(4096).decode() == '1':
                        print('Uspesno ste se registrovali sa korisnickim imenom -> ' + korImeISifra[0])
                        time.sleep(3)
                        break
                    else:
                        print('Postoji vec registrovan korisnik sa korisnickim imenom -> ' + korImeISifra[0] + '\nPokusajte ponovo!\n')
                os.system('cls')
                continue
            # Iskljucivanje - finish
            if (odgovor == '4'): iskljucivanje()
    except ConnectionResetError:
        print("Doslo je do prekida konekcije sa serverom!")
        main()

# Program
main()