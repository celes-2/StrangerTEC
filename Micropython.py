import machine
import network
import time
from time import sleep
import socket
from machine import Pin

client_socket = None
frase = ""
modo=""
unidad=0.2

########## WIFI ##########
ssid = "Redmi2g "
password = "escobar02"

def connectToWifi():
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            print("Esperando conexión...")
            sleep(1)

        print("Conectado IP:", wlan.ifconfig()[0])
        
        time.sleep(0.5)

    except Exception as e:
        print("Error WiFi:", e)

connectToWifi()

########## SOCKET ##########
def connectToPC():
    global client_socket

    server_address = ('10.169.237.80', 8001)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    client_socket.setblocking(False)

    print("Conectado al servidor")

connectToPC()


modo_actual = "LEDS"

def recibir():
    global client_socket, frase, modo_actual, unidad
    try:
        msg = client_socket.recv(1024).decode()
        if msg:
            print("Recibido raw:", msg) 
          
            partes = msg.split("\n")
            
            for parte in partes:
                parte = parte.strip()
                
                if not parte:
                    continue
                    
                if parte.startswith("FRASE:"):
                    frase = parte.replace("FRASE:", "")
                    print("Nueva frase:", frase)
                    if modo_actual == "LEDS":
                        mostrar_palabra(frase)
                    elif modo_actual == "BUZZER":
                        sonido(frase)

                elif parte.startswith("MODO:"):
                    modo_actual = parte.replace("MODO:", "")
                    print("Modo actualizado:", modo_actual)

                elif parte.startswith("VELOCIDAD:"):
                    unidad = float(parte.replace("VELOCIDAD:", ""))
                    print("Unidad recibida:", unidad)

    except OSError:
        pass
    
    
    
def enviar_puntos(puntos):
    global client_socket, puntos_totales, puntos_texto, puntos_precision, mensaje

    msg = f"Puntos totales: {puntos_totales}, Puntos texto: {puntos_texto}, Puntos precisión: {precision_total}, Mensaje: {mensaje}"

    client_socket.sendall(msg.encode())
    
boton = Pin(19, Pin.IN, Pin.PULL_UP)
buzzer = machine.Pin(4, machine.Pin.OUT)

AB = machine.Pin(16, machine.Pin.OUT)
CLK = machine.Pin(17, machine.Pin.OUT)

LED1 = machine.Pin(14, machine.Pin.OUT)
LED2 = machine.Pin(15, machine.Pin.OUT)
LED3 = machine.Pin(13, machine.Pin.OUT)

secuencia13 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
secuencia0  = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
secuencia1  = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
secuencia2  = [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
secuencia3  = [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
secuencia4  = [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
secuencia5  = [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
secuencia6  = [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]
secuencia7  = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
secuencia8  = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
secuencia9  = [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
secuencia10 = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
secuencia11 = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
secuencia12 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]

letras = {
    "A": (secuencia0, LED1),
    "B": (secuencia1, LED1),
    "C": (secuencia2, LED1),
    "D": (secuencia3, LED1),
    "E": (secuencia4, LED1),
    "F": (secuencia5, LED1),
    "G": (secuencia12, LED1),
    "H": (secuencia9, LED1),
    "I": (secuencia4, LED1),
    "J": (secuencia8, LED1),
    "K": (secuencia10, LED1),
    "L": (secuencia7, LED1),
    "M": (secuencia11, LED1),

    "N": (secuencia0, LED2),
    "O": (secuencia1, LED2),
    "P": (secuencia2, LED2),
    "Q": (secuencia3, LED2),
    "R": (secuencia4, LED2),
    "S": (secuencia5, LED2),
    "T": (secuencia12, LED2),
    "U": (secuencia9, LED2),
    "V": (secuencia4, LED2),
    "W": (secuencia8, LED2),
    "X": (secuencia10, LED2),
    "Y": (secuencia7, LED2),
    "Z": (secuencia11, LED2),

    "1": (secuencia0, LED3),
    "2": (secuencia1, LED3),
    "3": (secuencia2, LED3),
    "4": (secuencia3, LED3),
    "5": (secuencia4, LED3),
    "6": (secuencia5, LED3),
    "7": (secuencia12, LED3),
    "8": (secuencia9, LED3),
    "9": (secuencia4, LED3),
    "0": (secuencia8, LED3),
    "+": (secuencia10, LED3),
    "-": (secuencia7, LED3),
    "*": (secuencia11, LED3),
}

def EjecutarSecuencia(secuencia):
    for i in range(15):
        bit = secuencia[14 - i]

        AB.value(bit)

        CLK.value(1)
        CLK.value(0)

def limpiar():
    EjecutarSecuencia(secuencia13)

def apagar_leds():
    LED1.value(0)
    LED2.value(0)
    LED3.value(0)

def mostrar_letra(letra):
    if letra in letras:

        secuencia, led = letras[letra]

        limpiar()
        EjecutarSecuencia(secuencia)

        apagar_leds()
        led.value(1)

def mostrar_palabra(palabra, espera=1):

    for letra in palabra:
        mostrar_letra(letra)
        time.sleep(espera)

    limpiar()
    apagar_leds()
    
def morse_sonido(letra):
    for codigo, l in morse.items():
        if l == letra.upper():
            return codigo
    return ""


def sonido(frase):
    for letra in frase:
        if letra == " ":
            time.sleep(unidad * 7)
            continue
        codigo = morse_sonido(letra)
        for caracter in codigo:
            if caracter == ".":
                buzzer.value(1)
                time.sleep(unidad)
            elif caracter == "-":
                buzzer.value(1)
                time.sleep(unidad * 3)
            buzzer.value(0)
            time.sleep(unidad)
        time.sleep(unidad * 3)

def ejecutar(secuencia, led):

    limpiar()
    time.sleep(0.01)

    EjecutarSecuencia(secuencia)

    apagar_leds()
    led.value(1)


morse = {
".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E",
"..-.":"F","--.":"G","....":"H","..":"I",".---":"J",
"-.-":"K",".-..":"L","--":"M","-.":"N","---":"O",
".--.":"P","--.-":"Q",".-.":"R","...":"S","-":"T",
"..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z",
"-----":"0",".----":"1","..---":"2","...--":"3","....-":"4",
".....":"5","-....":"6","--...":"7","---..":"8","----.":"9",
".-.-.":"+",
"-....-":"-"
}

letra1 = ""
mensaje = ""


ultimo = time.ticks_ms()

precision_total = 0
valor_correcto = 0
valor_real = 0

puntos_precision = 0
puntos_texto = 0
puntos_totales = 0

def puntuacion():

    global puntos_texto, puntos_precision, puntos_totales

    puntos_totales = puntos_texto + precision_total

    print("Puntos totales:", puntos_totales)
    enviar_puntos(puntos_totales)

def puntos_palabra():

    global mensaje, frase, puntos_texto

    puntos_texto = 0

    mensaje_limpio = mensaje.replace(" ", "").replace("?", "")
    frase_limpia = frase.replace(" ", "")

    for i in range(len(mensaje_limpio)):

        if i < len(frase_limpia):

            if mensaje_limpio[i] == frase_limpia[i]:

                puntos_texto += 1

    print("Mensaje:", mensaje_limpio)
    print("Frase:", frase_limpia)
    print("Puntos texto:", puntos_texto)

def puntos():
    global duracion, valor_real, valor_correcto, puntos_precision, precision_total

    valor_real = duracion
    error = abs(valor_correcto - valor_real)
    precision = max(0, 100 - (error * 100))

    if precision >= 70:
        puntos_precision = 2
    elif precision >= 30:
        puntos_precision = 1
    else:
        puntos_precision = 0

    precision_total += puntos_precision

    print("Precision:", precision)
    print("Puntos precision:", precision_total)

    try:
        msg = f"Precision:{precision_total}\n"
        client_socket.sendall(msg.encode())
    except:
        pass

def cerrar_letra():

    global letra1, mensaje

    if letra1:

        letra = morse.get(letra1, "?")

        mensaje += letra

        print("Letra:", letra)
        print("Mensaje:", mensaje)

        letra1 = ""

def cerrar_palabra():

    global mensaje

    cerrar_letra()

    if mensaje and not mensaje.endswith(" "):

        mensaje += " "

        print("Palabra completa:", mensaje)

def cerrar_mensaje():

    global mensaje

    cerrar_palabra()

    mensaje_final = mensaje

    print("Mensaje final:", mensaje_final)

    puntos_palabra()
    puntuacion()

    mensaje = ""

while True:
    recibir()
    
    pausa_corta = unidad*3
    pausa_larga = unidad*7
    fin = unidad*10

    if boton.value() == 0:
        buzzer.value(1)
    else:
        buzzer.value(0)

    if boton.value() == 0:

        time.sleep(0.02)

        if boton.value() == 0:

            inicio = time.ticks_ms()

            while boton.value() == 0:
                time.sleep(0.001)

            duracion = time.ticks_diff(time.ticks_ms(),inicio) / 1000

            if duracion < unidad:
                letra1 += "."
                print(".")
                valor_correcto = unidad
                puntos()
            else:
                letra1 += "-"
                print("-")
                valor_correcto = unidad * 3
                puntos()

            ultimo = time.ticks_ms()

            time.sleep(0.02)

    tiempo_inactivo = time.ticks_diff(time.ticks_ms(),ultimo) / 1000

    if tiempo_inactivo > fin and (letra1 != "" or mensaje != ""):

        cerrar_mensaje()

        ultimo = time.ticks_ms()

    elif tiempo_inactivo > pausa_larga and (letra1 != "" or mensaje != ""):

        cerrar_palabra()

    elif tiempo_inactivo > pausa_corta and letra1 != "":

        cerrar_letra()

    time.sleep(0.02)

