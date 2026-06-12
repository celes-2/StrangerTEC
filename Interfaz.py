import socket
import tkinter as tk
from tkinter import *
import time
import random
from os import path
import threading

client_socket = None
conexion_activa = False
unidad=0.2
puntos_raspberry=0

def servidor():
    global client_socket, conexion_activa

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8001))
    server_socket.listen(1)

    print("Servidor listo... esperando conexión")

    client_socket, addr = server_socket.accept()
    conexion_activa = True
    print("Conectado con:", addr)

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                print("Cliente desconectado")
                break

            mensaje = data.decode()
            print("Recibido:", mensaje)

            if mensaje.startswith("Puntos totales:"):
                global puntos_raspberry
                try:
                    partes = mensaje.split(",")
                    puntos_raspberry = int(partes[0].replace("Puntos totales:", "").strip())
                    puntos_texto_rasp = int(partes[1].replace("Puntos texto:", "").strip())
                    puntos_precision_rasp = int(partes[2].replace("Puntos precisión:", "").strip())
                    mensaje_rasp = partes[3].replace("Mensaje:", "").strip()

                    def actualizar_ui():
                        resultado2.config(text=f"Puntos Raspberry: {puntos_raspberry}")
                        texto_rasp_label.config(text=f"Puntos texto: {puntos_texto_rasp}")
                        precision_rasp_label.config(text=f"Puntos precisión: {puntos_precision_rasp}")
                        mensaje_rasp_label.config(text=f"Mensaje: {mensaje_rasp}")
                        siguiente3.config(state="normal")

                    ventana.after(0, actualizar_ui)

                except Exception as e:
                    print("Error parseando puntos:", e)
            elif mensaje.startswith("Precision:"):
                try:
                    puntos_parciales = int(mensaje.replace("Precision:", "").strip())

                    def actualizar_parcial():
                        turno1.config(text=f"Puntos Raspberry: {puntos_parciales}")

                    ventana.after(0, actualizar_parcial)
                except Exception as e:
                    print("Error parcial:", e)
            elif mensaje == "Esperando frase":
                response = f"FRASE:{frase_juego}"
                client_socket.sendall(response.encode())

        except Exception as e:
            print("Error en servidor:", e)
            break

    client_socket.close()
    server_socket.close()


ventana=tk.Tk()
ventana.title("StrangerTEC")
ventana.minsize(1200,676)
ventana.resizable(width=NO, height=NO)

def mostrar_frame(frame):
    frame.tkraise()


def cargar_img(nombre):
    ruta  = path.join('imagenes', nombre) 
    img = PhotoImage(file=ruta)          
    return img
def boton():
    siguiente3.config(state="normal")


pagina1=tk.Frame(ventana,bg="gray")
pagina2=tk.Frame(ventana,bg="gray")
pagina3=tk.Frame(ventana,bg="gray")
pagina4=tk.Frame(ventana,bg="gray")
pagina5=tk.Frame(ventana,bg="gray")

canvas2=Canvas(pagina2,width=2000,height=700,bg="#0C414B")
canvas2.place(x=0,y=0)
canvas1=Canvas(pagina1,width=2000,height=700,bg='#0C414B')
canvas1.place(x=0,y=0)
canvas3=Canvas(pagina3,width=2000,height=700,bg='#0C414B')
canvas3.place(x=0,y=0)
canvas4=Canvas(pagina4,width=2000,height=700,bg='#0C414B')
canvas4.place(x=0,y=0)
canvas5=Canvas(pagina5,width=2000,height=700,bg='#0C414B')
canvas5.place(x=0,y=0)



siguiente3=tk.Button(pagina3, text="Inicio Jugador 2", command=lambda: mostrar_frame(pagina4),width=12, height=2)
siguiente3.place(x=550,y=550)
siguiente1=tk.Button(pagina1, text="INICIO", command=lambda: mostrar_frame(pagina2),width=12, height=2)
siguiente1.place(x=550,y=600)

siguiente2=tk.Button(pagina2, text="Inicio Turno 1", command=lambda: mostrar_frame(pagina3),width=15, height=2)
siguiente2.place(x=900,y=350)
siguiente4=tk.Button(pagina4, text="Siguiente4", command=lambda: mostrar_frame(pagina5),width=12, height=2)
siguiente4.place(x=350,y=550)
siguiente5=tk.Button(pagina5, text="Nueva Ronda", command=lambda:nueva_ronda(), width=12, height=2)
siguiente5.place(x=550,y=500)

canvas1.fondo = cargar_img('fondos4.png')
Fondo1 = canvas1.create_image(0, 0, anchor=NW,  image=canvas1.fondo)

canvas2.fondo = cargar_img('fondos.png')
Fondo2 = canvas2.create_image(0, 0, anchor=NW,  image=canvas2.fondo)

canvas3.fondo = cargar_img('fondos.png')
Fondo3 = canvas3.create_image(0, 0, anchor=NW,  image=canvas3.fondo)

canvas4.fondo = cargar_img('fondos.png')
Fondo4 = canvas4.create_image(0, 0, anchor=NW,  image=canvas4.fondo)
canvas5.fondo = cargar_img('fondos.png')
Fondo5= canvas5.create_image(0, 0, anchor=NW,  image=canvas5.fondo)


for frame in (pagina1,pagina2,pagina3,pagina4,pagina5):
    frame.grid(row=0, column=0, sticky="nsew")

ventana.grid_rowconfigure(0, weight=1)
ventana.grid_columnconfigure(0, weight=1)

frases1=["HOLA","ADIOS","SOS","SI","NO","TAL VEZ","CAFE","SUEÑO","TEC","AVEJA"]
frases=frases1.copy()

frase_juego = ""
texto_morse = ""

inicio = 0
tiempo_pausas=0
esperando=False
boton_apretado=False

precision_total = 0
valor_correcto = 0
valor_real=0
puntos_precision=0

jugador1=True
jugador2=False

puntos_totales=0

entries_frases=[]
panel=[]

morse = {
".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E",
"..-.":"F","--.":"G","....":"H","..":"I",".---":"J",
"-.-":"K",".-..":"L","--":"M","-.":"N","---":"O",
".--.":"P","--.-":"Q",".-.":"R","...":"S","-":"T",
"..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z",
"-----":"0",".----":"1","..---":"2","...--":"3","....-":"4",
".....":"5","-....":"6","--...":"7","---..":"8","----.":"9","+":".-.-.","-":"-....-"
}

codigo_ascii={
'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69,
'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74,
'K': 75, 'L': 76, 'M': 77, 'N': 78, 'O': 79,
'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84,
'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89,
'Z': 90, '0': 48, '1': 49, '2': 50, '3': 51, 
'4': 52,'5': 53, '6': 54, '7': 55, '8': 56, 
'9': 57, '+': 43, '-': 45
}


frame_panel = tk.Frame(pagina2, bg="gray")
frame_panel.place(x=600, y=200)

abecedario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890+-"

panel_letras = []

fila = 0
columna = 0

for letra in abecedario:

    caracter = tk.Label(frame_panel,text=letra,font=("Times New Roman",10),width=3,height=2,bg="black",fg="white")

    caracter.grid(row=fila, column=columna, padx=5, pady=5)

    panel_letras.append(caracter)

    columna += 1

    if columna == 7:
        columna = 0
        fila += 1

def traducir(frase):

    letras = frase.split(" ")

    texto_tradcido = "" 

    for letra in letras:

        if letra in morse:
            texto_tradcido = texto_tradcido + morse[letra]

        else:
            texto_tradcido = texto_tradcido + "?"

    return texto_tradcido

def traducir_ascii(codigo):
        codigo1= codigo_ascii[codigo]
        print(codigo1)
        cuatro_bits = codigo1 & 0b1111

        print(format(cuatro_bits, '04b'))

        


def mostrar_entries():

    global entries_frases

    for entry in entries_frases:
        entry.destroy()

    entries_frases = []

    for palabra, frase in enumerate(frases):

        frase3 = tk.Entry(pagina2, font=("Arial", 14), width=20)

        frase3.insert(0, frase)

        frase3.place(x=100, y=200 + palabra*30)

        entries_frases.append(frase3)

def guardar_cambios():

    global frases

    nuevas_frases = []

    for entry in entries_frases:

        texto = entry.get().upper()

        if texto != "":
            nuevas_frases.append(texto)

    frases = nuevas_frases

    mostrar_entries()

    iniciar_juego()

def iluminar_frase(frase, indice=0):

    if indice >= len(frase):
        return

    letra = frase[indice]

    if letra in abecedario:

        posicion = abecedario.index(letra)

        panel_letras[posicion].config(bg="red", fg="black")

        def apagar():

            panel_letras[posicion].config(bg="black", fg="white")

            iluminar_frase(frase, indice + 1)

        ventana.after(1000, apagar)

    else:
        iluminar_frase(frase, indice + 1)

def enviar_frase(frase):
    if conexion_activa:
        msg = f"FRASE:{frase}"
        client_socket.sendall(msg.encode())


def enviar_modo(modo):
    guardar_cambios()
    velocidad_juego()
    enviar_velocidad()
    time.sleep(0.1)
    if client_socket:
        client_socket.sendall(f"MODO:{modo}\n".encode())
    time.sleep(0.1)           
    siguiente2.config(state="normal")
    iniciar_juego()
    enviar_frase(frase_juego)     
    if modo == "LEDS":
        iluminar_frase(frase_juego)


velocidad2 = tk.IntVar()
velocidad2 = tk.IntVar(value=1)

nivel1 = tk.Radiobutton(pagina2, text="Nivel 1", variable=velocidad2, value=1, width=10, height=2)
nivel2 = tk.Radiobutton(pagina2, text="Nivel 2", variable=velocidad2, value=2, width=10, height=2)
nivel1.place(x=400,y=220)
nivel2.place(x=400,y=290)

def velocidad_juego():
    global unidad
    velocidad = velocidad2.get()
    if velocidad == 1:
        unidad = 0.2
    else:
        unidad = 0.3

def enviar_velocidad():
    if client_socket:
        client_socket.sendall(f"VELOCIDAD:{unidad}".encode())


def iniciar_juego():

    global frase_juego

    frase_juego = random.choice(frases)
    frase_label.config(text=f"Frase de la ronda: {frase_juego}")


    print(frase_juego)

def presionar(tiempo2):

    global inicio, boton_apretado

    inicio = time.time()

    boton_apretado=True

def soltar(tiempo2):

    global inicio, texto_morse, tiempo_pausas, esperando, boton_apretado, valor_correcto, valor_real, puntos_precision,precision_total

    tiempo3 = time.time() - inicio

    if tiempo3 <= unidad:
        texto_morse = texto_morse + "."
        valor_correcto = unidad
    else:
        texto_morse = texto_morse + "-"
        valor_correcto = unidad * 3

    valor_real=tiempo3

    error= abs(valor_correcto-valor_real)

    precision= max(0, 100-(error*100))

    if precision>=70:
        puntos_precision=2

    elif precision< 70 and precision>=30:
        puntos_precision=1

    else:
        puntos_precision=0

    precision_total+=puntos_precision

    print(precision_total)

    Puntaje.config(text=f"Puntos: {precision_total}")

    tiempo_pausas= time.time()

    esperando=True
    boton_apretado=False

    pantalla.config(text=texto_morse)

    partes = texto_morse.replace("/", " / ").split()
    traduccion = ""
    for parte in partes:
        if parte == "/":
            traduccion += " "
        elif parte in morse:
            traduccion+= morse[parte]
        elif parte:
            traduccion = "?"


def pausas():

    global tiempo_pausas, texto_morse, esperando, boton_apretado

    fin_pausa = time.time()

    if boton_apretado:

        ventana.after(200, pausas)
        return

    if esperando:

        pausa = fin_pausa - tiempo_pausas

        if pausa > 2 and pausa < 4:

            if len(texto_morse) > 0 and texto_morse[-1]!=" ":

                texto_morse += " "

                pantalla.config(text=texto_morse)

                partes = texto_morse.replace("/", " ").split()

                if partes:
                    ultimo_codigo = partes[-1]

                    if ultimo_codigo in morse:
                        letra = morse[ultimo_codigo]

                        print("Letra detectada:", letra)

                        traducir_ascii(letra)

        elif pausa >= 4:

            if len(texto_morse) > 0 and texto_morse[-1] != "/":

                texto_morse += "/"

                pantalla.config(text=texto_morse)

                

    ventana.after(200, pausas)

def quitar_espacios(frase):

    frase = frase.replace("/", "")
    frase = frase.replace(" ", "")

    return frase

def evaluar():

    global texto_morse, precision_total, puntos_totales

    traducido = traducir(texto_morse)

    objetivo = frase_juego.replace(" ", "")

    traducido = traducido.replace("/", "").replace(" ", "")

    traducido = traducido.strip()
    objetivo = objetivo.strip()

    puntos_texto = 0

    for i in range(len(traducido)):

        if i < len(objetivo):

            if traducido[i] == objetivo[i]:

                puntos_texto += 1

    print("Traducido:", traducido)
    print("Objetivo:", objetivo)
    print("Puntos texto:", puntos_texto)

    traducido_label.config(text=f"Mensaje: {traducido}")

    objetivo_label.config(text=f"Puntos Precision: {precision_total}")

    puntos_label.config(text=f"Puntos texto: {puntos_texto}")

    puntos_totales = puntos_texto + precision_total

    resultado.config(text=f"Puntos totales: {puntos_totales}")

    turnos()
    mostrar_frame(pagina5)

def turnos():
    global puntos_jugador1, puntos_totales, texto_morse, precision_total

    puntos_jugador1 = puntos_totales 

    if puntos_jugador1 > puntos_raspberry:
        resultado_final.config(text=f"Resultado: Ganó Jugador Servidor")
    elif puntos_raspberry > puntos_jugador1:
        resultado_final.config(text=f"Resultado: Ganó Jugador Raspberry")
    else:
        resultado_final.config(text=f"Resultado: Empate")

    texto_morse = ""
    precision_total = 0
    pantalla.config(text="")

    texto_morse = ""
    precision_total = 0

    pantalla.config(text="")

def nueva_ronda():
        global jugador1, jugador2, puntos_jugador1, puntos_raspberry, texto_morse, precision_total, puntos_totales

        jugador1 = True
        jugador2 = False
        puntos_jugador1 = 0
        puntos_raspberry = 0
        texto_morse = ""
        precision_total = 0
        puntos_totales = 0

        resultado.config(text="")
        resultado2.config(text="")
        traducido_label.config(text="")
        objetivo_label.config(text="")
        puntos_label.config(text="")
        texto_rasp_label.config(text="")
        precision_rasp_label.config(text="")
        mensaje_rasp_label.config(text="")
        pantalla.config(text="")

        mostrar_frame(pagina2)

inicio_label = tk.Label(pagina2,text="Selecciona Modo de Juego",font=("Times New Roman",30),fg="black",bg="#5C2C31")
inicio_label.place(x=80,y=30)

frases_label = tk.Label(pagina2,text="Frases",font=("Times New Roman",28),fg="black",bg="#5C2C31")
frases_label.place(x=140,y=140)

velocidad_labl = tk.Label(pagina2,text="Velocidad",font=("Times New Roman",28),fg="black",bg="#5C2C31")
velocidad_labl.place(x=370,y=140)

Puntaje = tk.Label(pagina4,text="Puntos: ",font=("Times New Roman", 24))
Puntaje.place(x=100, y=0)

pantalla = tk.Label(pagina4,text="",font=("Times New Roman", 30),bg="white",width=25,height=2)
pantalla.place(x=290,y=200)

turno1=tk.Label(pagina3, text="Turno Jugador 1", font=("Times New Roman",80), bg="#5C2C31")
turno1.place(x=200,y=300)

resultado_final = tk.Label(pagina5,text="Resultados de la ronda: ",font=("Times New Roman", 20))
resultado_final.place(x=400, y=50)
frase_label = tk.Label(pagina5,text=f"Frase de la ronda: {frase_juego}",font=("Times New Roman", 20))
frase_label.place(x=400, y=100)

#Jugador Rasp
mensaje_rasp_label = tk.Label(pagina5, text="Recibido:", font=("Times New Roman", 18), bg="#0C414B", fg="white")
mensaje_rasp_label.place(x=600, y=350)

resultado2 = tk.Label(pagina5,text="Puntos totales:",font=("Times New Roman", 20))
resultado2.place(x=600, y=300)

texto_rasp_label = tk.Label(pagina5, text="Puntos texto:", font=("Times New Roman", 18), bg="#0C414B", fg="white")
texto_rasp_label.place(x=600, y=410)


precision_rasp_label = tk.Label(pagina5, text="Puntos precision:", font=("Times New Roman", 18), bg="#0C414B", fg="white")
precision_rasp_label.place(x=600, y=380)

#Jgador compu

traducido_label = tk.Label(pagina5,text="Recibido 2",font=("Times New Roman", 18),bg="#0C414B",fg="white")
traducido_label.place(x=300, y=350)

resultado = tk.Label(pagina5,text="Puntos totales2:",font=("Times New Roman", 20))
resultado.place(x=300, y=300)

puntos_label = tk.Label(pagina5,text="Puntos texto2:",font=("Times New Roman", 18),bg="#0C414B",fg="white")
puntos_label.place(x=300, y=410)

objetivo_label = tk.Label(pagina5,text="Puntos precision2:",font=("Times New Roman", 18),bg="#0C414B",fg="white")
objetivo_label.place(x=300, y=380)


boton = tk.Button(pagina4,text="Mantener presionado",width=20,height=4,bg="lightblue")
boton.place(x=500,y=400)

boton.bind("<ButtonPress-1>", presionar)
boton.bind("<ButtonRelease-1>", soltar)

puntos_boton=Button(pagina4,text="Evaluar",command=evaluar,width=10,height=2)
puntos_boton.place(x=530,y=350)

buzzer = tk.Button(pagina2,text="Modo Escucha",command=lambda: enviar_modo("BUZZER"),width=15,height=2)
buzzer.place(x=900, y=300)

leds = tk.Button(pagina2,text="Modo Simple",command=lambda: enviar_modo("LEDS"),width=15,height=2)
leds.place(x=900, y=250)

mostrar_entries()

pausas()

mostrar_frame(pagina1)
threading.Thread(target=servidor, daemon=True).start()
ventana.mainloop()