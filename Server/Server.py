import pymysql
from socket import *
from _thread import start_new_thread

# Main - finish
def main():
    serverAddress = 'localhost'
    serverPort = 10001
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverAddress, serverPort))
    serverSocket.listen()
    print('Cekanje na konekciju . . .')
    while True:
        soketKlijenta, adresaKlijenta = serverSocket.accept()
        start_new_thread(client_thread, (soketKlijenta, adresaKlijenta))

def client_thread(soketKlijenta, adresaKlijenta):
    print('Povezani smo sa korisnikom na adresi ' + adresaKlijenta[0] + ' i na portu ' + str(adresaKlijenta[1]))
    meni = 'KALKULATOR\n\n1. Prijavi se\n2. Gost(max 3 kalkulacije)\n3. Registruj se\n\n4. Exit'
    soketKlijenta.send(meni.encode())
    korisnickoIme = ''
    while True:
        try:
            odgovorKlijenta = soketKlijenta.recv(1024).decode()
            # Prijava - finish
            if (odgovorKlijenta == '1'):
                while True:
                    try:
                        korisnickoIme = soketKlijenta.recv(1024).decode()
                        sifra = soketKlijenta.recv(1024).decode()
                        if proveraPriPrijavi(korisnickoIme, sifra):
                            soketKlijenta.send('1'.encode())
                            odgovorKlijenta = 'MeniKorisnik'
                            break
                        else:
                            soketKlijenta.send('0'.encode())
                    except pymysql.err.ProgrammingError:
                        soketKlijenta.send('0'.encode())
            # MeniKorisnik - finish
            if (odgovorKlijenta == 'MeniKorisnik'):
                while True:
                    odgovorKlijentaNaMeni = soketKlijenta.recv(1024).decode()
                    # Operacija - finish
                    if (odgovorKlijentaNaMeni == '1' or odgovorKlijentaNaMeni == '2' or odgovorKlijentaNaMeni == '3' or odgovorKlijentaNaMeni == '4'):
                        operacija = soketKlijenta.recv(1024).decode()
                        izraz = soketKlijenta.recv(1024).decode()
                        izrazSplit = izraz.split(operacija)
                        resenje = kalkulator(operacija, int(izrazSplit[0]), int(izrazSplit[1]))
                        izraz = izraz + '=' + str(resenje)
                        soketKlijenta.send(izraz.encode())
                        unesiUBazu(izraz, korisnickoIme)
                        continue
                    # Izrazi - finish
                    if (odgovorKlijentaNaMeni == '5'):
                        operacija = soketKlijenta.recv(1024).decode()
                        izraz = soketKlijenta.recv(1024).decode()
                        izrazSplit = izraz.split(operacija)
                        resenje = kalkulator(operacija, int(izrazSplit[0]), int(izrazSplit[1]))
                        izraz = izraz + '=' + str(resenje)
                        soketKlijenta.send(izraz.encode())
                        unesiUBazu(izraz, korisnickoIme)
                        continue
                    # Istorija - finish
                    if (odgovorKlijentaNaMeni == '6'):
                        stringIzraza = ucitajIzBaze(korisnickoIme)
                        soketKlijenta.send(stringIzraza[0].encode())
                        continue
                    # Logout - finish
                    if (odgovorKlijentaNaMeni == '7'): break
            # Gost - finish
            if (odgovorKlijenta == '2'):
                while True:
                    odgovorKlijentaNaMeni = soketKlijenta.recv(1024).decode()
                    # Izrazi - finish
                    if (odgovorKlijentaNaMeni == '1'):
                        operacija = soketKlijenta.recv(1024).decode()
                        izraz = soketKlijenta.recv(1024).decode()
                        izrazSplit = izraz.split(operacija)
                        resenje = kalkulator(operacija, int(izrazSplit[0]), int(izrazSplit[1]))
                        izraz = izraz + '=' + str(resenje)
                        soketKlijenta.send(izraz.encode())
                        continue
                    # Logout - finish
                    if (odgovorKlijentaNaMeni == '2'): break
                    else: continue
            # Registracija - finish
            if (odgovorKlijenta == '3'):
                while True:
                    try:
                        korisnickoIme = soketKlijenta.recv(1024).decode()
                        sifra = soketKlijenta.recv(1024).decode()
                        if proveraPriRegistraciji(korisnickoIme):
                            registracija(korisnickoIme, sifra)
                            soketKlijenta.send('1'.encode())
                            break
                        else:
                            soketKlijenta.send('0'.encode())
                    except pymysql.err.ProgrammingError:
                        soketKlijenta.send('0'.encode())
                continue
            # Iskljucivanje - finish
            if (odgovorKlijenta == '4'): break
        except ConnectionResetError:
            print('Doslo je do neocekivanog prekida konekcije sa klijentom!')
            break
    soketKlijenta.close()
    print('Prekid konekcije sa korisnikom na adresi ' + adresaKlijenta[0] + ' i na portu ' + str(adresaKlijenta[1]))

# ProveraReg - finish
def proveraPriRegistraciji(korisnickoIme):
    db = pymysql.connect("localhost", "Nemanja", "sifra", "Kalkulator")
    cursor = db.cursor()
    sql = "SELECT * FROM USERS \
            WHERE USER = '" + korisnickoIme + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        return True
    else:
        return False

# Registracija - finish
def registracija(korisnickoIme, sifra):
    db = pymysql.connect("localhost", "Nemanja", "sifra", "Kalkulator")
    cursor = db.cursor()
    sql = "INSERT INTO USERS \
            (USER, PASSWORD, IZRAZI) \
            VALUES ('" + korisnickoIme + "', '" + sifra + "', '')"
    cursor.execute(sql)
    db.commit()
    db.close()

# ProveraPrij - finish
def proveraPriPrijavi(korisnickoIme, sifra):
    db = pymysql.connect("localhost", "Nemanja", "sifra", "Kalkulator")
    cursor = db.cursor()
    sql = "SELECT * FROM USERS \
                WHERE USER = '" + korisnickoIme + "' AND PASSWORD = '" + sifra + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) != 0:
        return True
    else:
        return False

# Kalkulator - finish
def kalkulator(znak, br1, br2):
    if (znak == '1' or znak == '+'):
        return int(br1) + int(br2)
    elif (znak == '2' or znak == '-'):
        return int(br1) - int(br2)
    elif (znak == '3' or znak == '*'):
        return int(br1) * int(br2)
    elif (znak == '4' or znak == '/'):
        try:
            return int(br1) / int(br2)
        except ZeroDivisionError:
            print("Ne moze se deliti sa nulom!")
            return 0
    else:
        print("Greska!")

# Ubaci u bazu - finish
def unesiUBazu(izraz, korisnickoIme):
    db = pymysql.connect("localhost", "Nemanja", "sifra", "Kalkulator")
    cursor = db.cursor()
    sql = "UPDATE `users` SET IZRAZI = concat(IZRAZI, '" + izraz + "x') WHERE USER = '" + korisnickoIme + "'"
    cursor.execute(sql)
    db.commit()
    db.close()

# Ucitaj iz baze - finish
def ucitajIzBaze(korisnickoIme):
    db = pymysql.connect("localhost", "Nemanja", "sifra", "Kalkulator")
    cursor = db.cursor()
    sql = "SELECT `IZRAZI` FROM `users` WHERE USER = '" + korisnickoIme + "'"
    cursor.execute(sql)
    results = cursor.fetchone()
    db.close()
    return results

# Program
main()