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


def cargar_img(nombre):
    ruta  = path.join('imagenes', nombre) 
    img = PhotoImage(file=ruta)          
    return img

pagina1=tk.Frame(ventana,bg="gray")
pagina2=tk.Frame(ventana,bg="gray")
pagina3=tk.Frame(ventana,bg="gray")

canvas2=Canvas(pagina2,width=2000,height=700,bg="#0C414B")
canvas2.place(x=0,y=0)
canvas1=Canvas(pagina1,width=2000,height=700,bg='#0C414B')
canvas1.place(x=0,y=0)
canvas3=Canvas(pagina3,width=2000,height=700,bg='#0C414B')
canvas3.place(x=0,y=0)

siguiente3=tk.Button(pagina3, text="volver", command=lambda: mostrar_frame(pagina1),width=12, height=2)
siguiente3.place(x=350,y=550)
siguiente1=tk.Button(pagina1, text="Siguiente", command=lambda: mostrar_frame(pagina2),width=12, height=2)
siguiente1.place(x=500,y=550)
siguiente2=tk.Button(pagina2, text="Siguiente2", command=lambda: mostrar_frame(pagina3),width=12, height=2)
siguiente2.place(x=350,y=550)

canvas1.fondo = cargar_img('fondo5.png')
Fondo1 = canvas1.create_image(0, 0, anchor=NW,  image=canvas1.fondo)


for frame in (pagina1,pagina2,pagina3):
    frame.grid(row=0, column=0, sticky="nsew")



ventana.grid_rowconfigure(0, weight=1)
ventana.grid_columnconfigure(0, weight=1)


frases=[]
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

morse = {
".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E",
"..-.":"F","--.":"G","....":"H","..":"I",".---":"J",
"-.-":"K",".-..":"L","--":"M","-.":"N","---":"O",
".--.":"P","--.-":"Q",".-.":"R","...":"S","-":"T",
"..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z",
"-----":"0",".----":"1","..---":"2","...--":"3","....-":"4",
".....":"5","-....":"6","--...":"7","---..":"8","----.":"9","+":".-.-.","-":"-....-"
}

def traducir(frase):

    letras = frase.split(" ") #Hacerlo lista

    texto_tradcido = "" 

    for letra in letras:

        if letra in morse:
            texto_tradcido = texto_tradcido + morse[letra] #Esto es para añadir las letras que sí se escriben bien para despues sumar puntos

    return texto_tradcido

def agregar_frase():

    texto = entrada.get()
    if len(texto) <= 16 and texto != "":

        frases.append(texto.upper())

        lista_label.config(text=(frases))

        entrada.delete(0, END)

    else:

        lista_label.config(text="Máximo 16 caracteres")

    if len(frases) == 10:

        iniciar_juego()

 
def iniciar_juego():

    global frase_juego

    frase_juego = random.choice(frases)

    frase_label.config(text="Frase: " + frase_juego)


def presionar(tiempo2):   #Es para contar el tiempo que dura presionado, el time.time cuenta desde una fecha específica, aquíes del 31 de diciembre de 1969 a las 6
    global inicio, boton_apretado
    inicio = time.time()
    boton_apretado=True


def soltar(tiempo2): #Depende de cuanto tiempo se presiona detecta si es un punto o una raya

    global inicio, texto_morse, tiempo_pausas, esperando, boton_apretado, valor_correcto, valor_real,puntos_precision,precision_total

    tiempo3 = time.time() - inicio

    if tiempo3 <= 1:
        texto_morse = texto_morse + "."
        valor_correcto=1
        
 
    else:
        texto_morse = texto_morse + "-"
        valor_correcto=3
    
    valor_real=tiempo3
    error= abs(valor_correcto-valor_real)
    precision= max(0, 100-(error*100))  #Se usa el error como porcentaje

    
    if precision>=70:
        puntos_precision=2
    elif precision< 70 and precision>=30:
        puntos_precision=1
    else:
        puntos_precision=0
    

    precision_total+=puntos_precision
    print(precision_total)


    tiempo_pausas= time.time()
    esperando=True
    boton_apretado=False

    pantalla.config(text=texto_morse)

def pausas():

    global tiempo_pausas, texto_morse, esperando, boton_apretado

    fin_pausa = time.time()

    if boton_apretado:
        ventana.after(200, pausas)   #Evita silencios falsos
        return

    if esperando:

        pausa = fin_pausa - tiempo_pausas

        if pausa > 2 and pausa < 4: #El valor es de 3 pero se puso por que no siempre va a ser preciso
            if len(texto_morse) > 0 and texto_morse[-1]!=" ":
                texto_morse += " "
                pantalla.config(text=texto_morse)

        elif pausa >= 4:
            if len(texto_morse) > 0 and texto_morse[-1] != "/":
                texto_morse += "/"
                pantalla.config(text=texto_morse)
                

    ventana.after(200, pausas) #Para que vaya revisando las pausas constantemente

def quitar_espacios(frase):         #Se quitan para evaluar solo la frase
    frase = frase.replace("/", "")
    frase = frase.replace(" ", "")
    return frase


def evaluar():

    global texto_morse, precision_total, puntos_totales
    traducido = traducir(texto_morse)

    objetivo = frase_juego.replace(" ", "") 
    traducido = traducido.replace("/", "").replace(" ", "")

    puntos_texto = 0

    for letra in range(len(traducido)):

        if letra < len(objetivo):

            if traducido[letra] == objetivo[letra]:
                puntos_texto += 1 
            else:
                puntos_texto += 0    

        else:
            puntos_texto += 0       


    puntos_totales=puntos_texto+ precision_total

    resultado.config(text="Puntos totales: " + str(puntos_totales))
    turnos()


def turnos():

    global jugador1, jugador2
    global puntos_jugador1, puntos_jugador2
    global puntos_totales
    global texto_morse
    global precision_total


    if jugador1 == True:

        puntos_jugador1 = puntos_totales

        jugador1 = False
        jugador2 = True

        resultado.config(
            text="Turno jugador 2"
        )


    elif jugador2 == True:

        puntos_jugador2 = puntos_totales

        # ganador
        if puntos_jugador1 > puntos_jugador2:

            resultado.config(
                text="Ganó jugador 1"
            )

        elif puntos_jugador2 > puntos_jugador1:

            resultado.config(
                text="Ganó jugador 2"
            )

        else:

            resultado.config(
                text="Empate"
            )

    texto_morse = ""
    precision_total = 0

    pantalla.config(text="")

    def nueva_ronda():

        global texto_morse
        global precision_total
        global puntos_totales
        global frase_juego

        texto_morse = ""
        precision_total = 0
        puntos_totales = 0

        pantalla.config(text="")
        resultado.config(text="")

        frase_juego = random.choice(frases)

        frase_label.config(
            text="Frase: " + frase_juego)





entrada = tk.Entry(pagina2, font=("Arial",20), width=30)
entrada.place(x=0,y=10)

agregar=Button(pagina2,text="Agregar frase",command=agregar_frase)
agregar.place(x=200,y=20)

lista_label = tk.Label(pagina2, text="")
lista_label.place(x=500,y=50)



frase_label = tk.Label(pagina3,text="Frase: " + frase_juego, font=("Arial", 24))
frase_label.place(x=100, y=0)

pantalla = tk.Label(pagina3, text="", font=("Arial", 30), bg="white", width=25, height=2)
pantalla.place(x=600,y=0)

resultado = tk.Label(pagina3, text="", font=("Arial", 20))
resultado.place(x=300, y=80)

boton = tk.Button(pagina3, text="Mantener presionado", width=25, height=4, bg="lightblue")
boton.place(x=900,y=0)

boton.bind("<ButtonPress-1>", presionar)
boton.bind("<ButtonRelease-1>", soltar)


puntos_boton=Button(pagina3, text="Evaluar", command=evaluar)
puntos_boton.place(x=0,y=100)
pausas()
mostrar_frame(pagina1)
ventana.mainloop()