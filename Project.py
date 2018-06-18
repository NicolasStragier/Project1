from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL
from flask import session
from flask import request

import RPi.GPIO as GPIO
import SimpleMFRC522
import spidev
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = Flask(__name__)


mysql = MySQL(app)

app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_DB"] = "smartfridgedb"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "Leerling123"

def get_data(sql,params=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql,params)

    except Exception as ex:
        print("Woops:", ex)

    result = cursor.fetchall()
    dbdata = []
    for data in result:
        dbdata.append(list(data))
    cursor.close()
    conn.close()
    return dbdata

def set_data(sql, params=None):
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        print(sql)
        cursor.execute(sql, params)
        conn.commit()
        print("SQL uitgevoerd")

    except Exception as e:
        print("Fout bij uitvoeren van sql: {0})".format(e))
        return False

    cursor.close()
    conn.close()

    return True


@app.route('/')
def index():
    aantalbier = get_data('SELECT D.Dranknaam, D.Drankid, Sum(aantal) as Momenteel FROM smartfridgedb.logging as L, smartfridgedb.acties as A, smartfridgedb.users as U, smartfridgedb.dranken as D WHERE L.Actieid = A.Actieid and L.Userid = U.Userid and L.Drankid = D.Drankid and L.Loggingid != 1 and D.Drankid = 2 group by D.Drankid ORDER BY Tijd;')
    aantalblik = get_data('SELECT D.Dranknaam, D.Drankid, Sum(aantal) as Momenteel FROM smartfridgedb.logging as L, smartfridgedb.acties as A, smartfridgedb.users as U, smartfridgedb.dranken as D WHERE L.Actieid = A.Actieid and L.Userid = U.Userid and L.Drankid = D.Drankid and L.Loggingid != 1 and D.Drankid = 1 group by D.Drankid ORDER BY Tijd;')
    logins = get_data('SELECT concat(cast(Voornaam as char), " ", cast(Naam as char)) as Username FROM users')
    passwords = get_data('SELECT RFID FROM users')
    aantal = get_data('SELECT count(concat(cast(Voornaam as char), " ", cast(Naam as char))) as Username FROM users')
    session['login'] = "False"
    session['user'] = ""
    return render_template('login.html', bier = aantalbier, blik = aantalblik, users = logins, passes = passwords, lengte = aantal)

@app.route('/login')
def login():
    return render_template('loginpagina.html')

@app.route('/welkomadmin')
def welkom():
    gegevens = get_data('SELECT L.Loggingid,  A.Actie, concat(cast(U.Voornaam as char), " ", cast(U.Naam as char)) as Naam, U.rol, D.Dranknaam, L.Aantal, L.Tijd FROM smartfridgedb.logging as L, smartfridgedb.acties as A, smartfridgedb.users as U, smartfridgedb.dranken as D WHERE L.Actieid = A.Actieid and L.Userid = U.Userid and L.Drankid = D.Drankid ORDER BY L.Loggingid desc;')
    #if session.get('login') == "True":
    return render_template('welkom.html', data=gegevens)
    #else:
     #   return  index()

@app.route('/welkom')
def welkomuser():
    user = session.get('user')

    return render_template('welkomuser.html', gebruiker = user)



@app.route('/adduser')
def adduser():
    return render_template('adduser.html')

@app.route('/addinguser', methods=['get'])
def addinguser():
    Naam = request.args.get('Name', None)
    Voornaam = request.args.get('Firstname', None)
    Rol = request.args.get('Function', None)
    RFID = request.args.get('RFID', None)
    set_data("insert into smartfridgedb.users (Userid, Naam, Voornaam, Rol, RFID) VALUES (0,%s, %s, %s, %s)", (Naam, Voornaam, Rol, RFID))
    return render_template('adduser.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'  # secret key, anders werkt het niet
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)


reader = SimpleMFRC522.SimpleMFRC522()
spi = spidev.SpiDev()
spi.open(0,0)

ledgroen = 23
ledrood = 24
ledblauw = 26
lock = 21
knop = 6

#LEDGROEN
GPIO.setup(ledgroen, GPIO.OUT)
GPIO.output(ledgroen, GPIO.LOW)
#LEDROOD
GPIO.setup(ledrood, GPIO.OUT)
GPIO.output(ledrood, GPIO.LOW)
#LEDBLAUW
GPIO.setup(ledblauw, GPIO.OUT)
GPIO.output(ledblauw, GPIO.LOW)
#LOCK
GPIO.setup(lock, GPIO.OUT)
GPIO.output(lock, GPIO.LOW)
#BUTTON
GPIO.setup(knop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

lijst = [705861867776, 644758420395, 923327707913]


def Setup():
    GPIO.output(ledblauw, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(ledblauw, GPIO.LOW)
    sleep(0.5)
    GPIO.output(ledblauw, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(ledblauw, GPIO.LOW)
    sleep(0.5)
    GPIO.output(ledblauw, GPIO.HIGH)
    # Go to Scannen()
    Scannen()


spi = spidev.SpiDev()
spi.open(0, 1)


def read_spi(channel):
    spidata = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((spidata[1] & 3) << 8 + spidata[2])


def read_spi_b(channel):
    spidata = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((spidata[1] & 3) << 8 + spidata[2])


def Controleer():
        Gesloten = 1
        Open = 0
        Bier1 = 0
        Bier2 = 0
        Bier3 = 0
        Cola1 = 0
        Cola2 = 0
        Cola3 = 0

        try:
            while GPIO.input(knop) != Gesloten:
                # GPIO.output(lock, GPIO.LOW)
                data1 = read_spi(0)
                data2 = read_spi(1)
                data3 = read_spi(2)
                data4 = read_spi(3)
                data5 = read_spi(4)
                data6 = read_spi(5)
                # print("Waarde channel 1 = {}".format(data1))
                # print("Waarde channel 4 = {}" .format(read_spi_b(4)))
                # print("Waarde channel 2 = {}".format(data2))
                # print("Waarde channel 3 = {}".format(data3))
                # sleep(1)
                if data1 != 0:
                    Cola1 = 1
                if data2 != 0:
                    Cola2 = 1
                if data3 != 0:
                    Cola3 = 1
                if data4 != 0:
                    Bier1 = 1
                if data5 != 0:
                    Bier2 = 1
                if data6 != 0:
                    Bier3 = 1
                sleep(0.5)
                # If knop is closed
                GPIO.output(lock, GPIO.LOW)
                GPIO.output(ledgroen, GPIO.LOW)
                print("Doorsturen genomen dranken")
                Bieren = (Bier1 + Bier2 + Bier3)
                Colas = (Cola1 + Cola2 + Cola3)
                print("Er zijn {} aantal Bierjtes genomen".format(Bieren))
                print("er zijn {} aantal Cola's genomen".format(Colas))
                Scannen()

        except KeyboardInterrupt:
            spi.close()

    def Scannen():
        GPIO.output(ledgroen, GPIO.LOW)
        GPIO.output(ledrood, GPIO.LOW)
        print("Looking for cards")
        print("Press Ctrl-C to stop.")

        try:
            while True:

                id, text = reader.read()
                print('ID: ' + str(id))
                print('Functie: ' + str(text))
                if id in lijst:
                    GPIO.output(ledgroen, GPIO.HIGH)
                    GPIO.output(lock, GPIO.HIGH)
                    sleep(2)
                    GPIO.output(lock, GPIO.LOW)
                    Controleer()
                else:
                    GPIO.output(ledrood, GPIO.HIGH)
                    sleep(2)
                    Scannen()
        except KeyboardInterrupt:
            GPIO.output(lock, GPIO.LOW)
            GPIO.cleanup()






