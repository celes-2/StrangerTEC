import tkinter as tk
from tkinter import *
import time
import random
from os import path

ventana=tk.Tk()
ventana.title("StrangerTEC")
ventana.minsize(1200,676)
ventana.resizable(width=NO, height=NO)

def mostrar_frame(frame):
    frame.tkraise()
    pagina3


def cargar_img(nombre):
    ruta  = path.join('imagenes', nombre) 
    img = PhotoImage(file=ruta)          
    return img

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



siguiente3=tk.Button(pagina3, text="volver", command=lambda: mostrar_frame(pagina4),width=12, height=2)
siguiente3.place(x=350,y=550)

siguiente1=tk.Button(pagina1, text="INICIO", command=lambda: mostrar_frame(pagina2),width=12, height=2)
siguiente1.place(x=550,y=600)

siguiente2=tk.Button(pagina2, text="Siguiente2", command=lambda: mostrar_frame(pagina3),width=12, height=2)
siguiente2.place(x=350,y=550)
siguiente4=tk.Button(pagina4, text="Siguiente4", command=lambda: mostrar_frame(pagina5),width=12, height=2)
siguiente4.place(x=350,y=550)
siguiente5=tk.Button(pagina5, text="Siguiente5", command=lambda: mostrar_frame(pagina1),width=12, height=2)
siguiente5.place(x=350,y=550)

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

frases1=["HOLA","SADSA","SRFGB","HMBKJ","GJKM","DTFHN","DYTHGN","GHV","TYFHG","FGHVGJ"]
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

frame_panel = tk.Frame(pagina2, bg="gray")
frame_panel.place(x=500, y=200)

abecedario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890+-"

panel_letras = []

fila = 0
columna = 0

for letra in abecedario: #Panel de letras

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

def mostrar_entries():

    global entries_frases

    for entry in entries_frases:
        entry.destroy()

    entries_frases = []

    for palabra, frase in enumerate(frases):

        frase3 = tk.Entry(pagina2, font=("Arial", 14), width=20)

        frase3.insert(0, frase)

        frase3.place(x=150, y=200 + palabra*30)

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

def iniciar_juego():

    global frase_juego

    frase_juego = random.choice(frases)

    iluminar_frase(frase_juego)

    print(frase_juego)

def presionar(tiempo2):

    global inicio, boton_apretado

    inicio = time.time()

    boton_apretado=True

def soltar(tiempo2):

    global inicio, texto_morse, tiempo_pausas, esperando, boton_apretado, valor_correcto, valor_real, puntos_precision,precision_total

    tiempo3 = time.time() - inicio

    if tiempo3 <= 1:

        texto_morse = texto_morse + "."
        valor_correcto=1

    else:

        texto_morse = texto_morse + "-"
        valor_correcto=3

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

    traducido_label.config(text=f"Traducido: {traducido}")

    objetivo_label.config(text=f"Objetivo: {objetivo}")

    puntos_label.config(text=f"Puntos texto: {puntos_texto}")

    puntos_totales = puntos_texto + precision_total

    resultado.config(text=f"Puntos totales: {puntos_totales}")

    turnos()

def turnos():

    global jugador1, jugador2, puntos_jugador1, puntos_jugador2, puntos_totales, texto_morse, precision_total

    if jugador1 == True:

        puntos_jugador1 = puntos_totales

        jugador1 = False
        jugador2 = True

        resultado.config(text="Turno jugador 2")

    elif jugador2 == True:

        puntos_jugador2 = puntos_totales

        if puntos_jugador1 > puntos_jugador2:

            resultado.config(text="Ganó jugador 1")

        elif puntos_jugador2 > puntos_jugador1:

            resultado.config(text="Ganó jugador 2")

        else:

            resultado.config(text="Empate")

    texto_morse = ""
    precision_total = 0

    pantalla.config(text="")

inicio_label = tk.Label(
    pagina2,
    text="Selecciona Modo de Juego",
    font=("Times New Roman",30),
    fg="black",
    bg="#5C2C31"
)
inicio_label.place(x=80,y=30)

Puntaje = tk.Label(
    pagina4,
    text="Puntos: ",
    font=("Times New Roman", 24)
)
Puntaje.place(x=100, y=0)

pantalla = tk.Label(pagina4,text="",font=("Times New Roman", 30),bg="white",width=25,height=2)
pantalla.place(x=290,y=200)

turno1=tk.Label(pagina3, text="Turno Jugador 1", font=("Times New Roman",80), bg="#5C2C31")
turno1.place(x=200,y=300)

resultado = tk.Label(
    pagina5,
    text="",
    font=("Times New Roman", 20)
)
resultado.place(x=300, y=80)

traducido_label = tk.Label(
    pagina5,
    text="",
    font=("Times New Roman", 18),
    bg="#0C414B",
    fg="white"
)
traducido_label.place(x=300, y=120)

objetivo_label = tk.Label(
    pagina5,
    text="",
    font=("Times New Roman", 18),
    bg="#0C414B",
    fg="white"
)
objetivo_label.place(x=300, y=150)

puntos_label = tk.Label(
    pagina5,
    text="",
    font=("Times New Roman", 18),
    bg="#0C414B",
    fg="white"
)
puntos_label.place(x=300, y=180)

boton = tk.Button(
    pagina4,
    text="Mantener presionado",
    width=20,
    height=4,
    bg="lightblue"
)
boton.place(x=500,y=400)

guardar=tk.Button(
    pagina2,
    text="Guardar Frases",
    command=guardar_cambios,
    width=16,
    height=2
)
guardar.place(x=570,y=549)

boton.bind("<ButtonPress-1>", presionar)
boton.bind("<ButtonRelease-1>", soltar)

puntos_boton=Button(
    pagina4,
    text="Evaluar",
    command=evaluar,
    width=10,
    height=2
)
puntos_boton.place(x=530,y=350)

mostrar_entries()

pausas()

mostrar_frame(pagina1)

ventana.mainloop()