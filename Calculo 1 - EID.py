import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import matplotlib.pyplot as plt

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
programa_calculo = ctk.CTk()
programa_calculo.title("EID-CALCULO-LIMITES")
programa_calculo.geometry("1080x720")

def limpiar():
    ingresar_datos.delete("1.0", "end")
    ingresar_tendencia.delete("1.0", "end")
    resultado.configure(text="Resultado del límite:")
    for grafico in lado_derecho.winfo_children():
        grafico.destroy()

def coseno():
    ingresar_datos.insert("end", "cos(x)") 

def sin():
    ingresar_datos.insert("end","sin(x)")

def tangente():
    ingresar_datos.insert("end","tan(x)")
    
def infinito():
    ingresar_tendencia.delete("1.0", "end")
    ingresar_tendencia.insert("end","oo")

def inf_neg():
    ingresar_tendencia.delete("1.0", "end")
    ingresar_tendencia.insert("end","-oo")

def raiz_cuadrada():
    ingresar_datos.insert("end","sqrt(x)")

def cuadrado():
    ingresar_datos.insert("end","**2")

def exp():
    ingresar_datos.insert("end", "**")
def calcular():
    try:
        funcion = ingresar_datos.get("1.0", "end-1c").strip()#el .strip() no es lo que suena sino que elimina los espacios vacios
        tendencia = ingresar_tendencia.get("1.0", "end-1c").strip()
        
        if not funcion or not tendencia:
            resultado.configure(text="Error: Rellene todos los campos")#avisa si está vacío algún campo
            return

        x = sp.Symbol('x')#se traduce por asi decirlo la x de letra a la x matematica
        expresion = sp.sympify(funcion)#y la funcion igual
        
        limite_es_infinito = False
        valor_limite_grafica = None
        #infinito ultra negativoooooooooooo
        if "-oo" in tendencia or "-inf" in tendencia:
            infinito_neg = -100000#como infinito no es un numero sino un concepto se le coloca un numero enorme negativo para simularlo
            evaluacion = expresion.subs(x, infinito_neg)#cambia la x en el calculo por el numero gigante
            
            if evaluacion.is_real and evaluacion.is_finite:#revisa si es un numero real
                resultado_infinitonegativooooo = float(evaluacion.evalf())#hace el calculo y lo convierte a decimal para que calcule mejor
                
                if resultado_infinitonegativooooo > 10000:
                    resultado.configure(text="El límite es: oo")#actualiza el resultado
                    limite_es_infinito = True
                elif resultado_infinitonegativooooo < -10000:#si se dispara en negativo se asume que es inf negativo
                    resultado.configure(text="El límite es: -oo")#actualiza el resultado
                    limite_es_infinito = True
                else:#este es por si no es ninguna de las anteriores
                    valor_limite_grafica = round(resultado_infinitonegativooooo, 3)#el resultado lo redondea
                    resultado.configure(text=f"El límite es: {valor_limite_grafica}")#actualiza el resultado
            else:
                resultado.configure(text="El límite no existe (Resultado no numérico)")

        #infinito +++++++++++++++
        elif "oo" in tendencia or "inf" in tendencia:#desde aca para abajo es lo mismo pero en el caso positivo
            infinitooo = 100000
            evaluacion = expresion.subs(x, infinitooo)
            
            if evaluacion.is_real and evaluacion.is_finite:#revisa si es real
                resultado_infinitoo = float(evaluacion.evalf())
                
                if resultado_infinitoo > 10000:
                    resultado.configure(text="El límite es: oo")
                    limite_es_infinito = True
                elif resultado_infinitoo < -10000:
                    resultado.configure(text="El límite es: -oo")
                    limite_es_infinito = True
                else:
                    valor_limite_grafica = round(resultado_infinitoo, 3)
                    resultado.configure(text=f"El límite es: {valor_limite_grafica}")
            else:
                resultado.configure(text="El límite no existe (Resultado no numérico)")
        else:#si no es infinito ni negativo se asume que es un numero normal
            try:
                c = float(tendencia)
            except ValueError:
                resultado.configure(text="Error: la tendencia no es válida")
                return

            izq = None#se inicia en none para que siosi este en 0
            der = None
            h = 0.001

            for i in range(4):
                punto_izq = c - h#a la tendencia se le resta un numero mas chico en cada ciclo para aproximarse mas x la izquierda
                try:
                    evaluacion_izq = expresion.subs(x, sp.Float(punto_izq, 30)).evalf(30)#el 30 es para que sea preciso en decimales y no trolee
                    if evaluacion_izq.is_real and evaluacion_izq.is_finite:
                        izq = float(evaluacion_izq)#se convierte en decimal para trabajarlo mejor
                except Exception:
                    pass#si falla se sigue nomas
                h = h / 10
                
            h = 0.001#reiniciamos el paso para el lado derecho

            for i in range(4):#evaluacion del limite por la derecha
                punto_der = c + h#a la tendencia se le suma un numero mas chico en cada ciclo para aproximarse mas x la derecha
                try:
                    evaluacion_der = expresion.subs(x, sp.Float(punto_der, 30)).evalf(30)
                    
                    if evaluacion_der.is_real and evaluacion_der.is_finite:
                        der = float(evaluacion_der)#se convierte en decimal para poderlo trabajar mejor
                except Exception:
                    pass
                h = h / 10
                
            #revisa si se calculo bien por cada lado
            if izq is None or der is None:
                resultado.configure(text="Error: No se pudo evaluar bien (posible división por cero o error de escritura)")
                return

            if abs(izq) > 10000 or abs(der) > 10000:#toma como que tiende a infinito si se pasa de un numero grande
                resultado.configure(text="El límite no existe (Tiende a infinito)")
                limite_es_infinito = True
            else:
                diferencia_laterales = abs(izq - der)#se le aplica valor absoluto para ver la distancia entre laterales
                if diferencia_laterales < 0.01:#si la diferencia es chica se toma como que los laterales son iguales
                    limite_final = round((izq + der) / 2, 6)#se saca el limite promediando los laterales y dejando para 6 decimales
                    if limite_final.is_integer():#revisa si el número es entero activa la condicion
                        limite_final = int(limite_final)#lo transforma a int para eliminar los decimales que no sirven
                    resultado.configure(text=f"El límite es: {limite_final}")#muestra el resultado
                    valor_limite_grafica = float(limite_final)#lo almacena en una variable para graficarlo
                else:
                    resultado.configure(text=f"El límite no existe (Izq: {round(izq,4)}, Der: {round(der,4)})") # mensaje si no existe el limite
        #____________________________________graficacioooooooon__________________________________
        for grafico in lado_derecho.winfo_children():
            grafico.destroy()

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        
        if tendencia in ["oo", "-oo", "inf", "-inf"]:
            c_grafica = 0.0
        else:
            c_grafica = float(tendencia)

        valores_x = []
        valores_y = []
        paso = 0.05
        
        for i in range(401):
            val_x = (c_grafica - 10.0) + (i * paso)
            if not (tendencia in ["oo", "-oo", "inf", "-inf"]) and abs(val_x - c_grafica) < 0.001:
                continue
            
            try:
                evaluacion_sp = expresion.subs(x, val_x).evalf()
                
                #
                if evaluacion_sp.is_real and evaluacion_sp.is_finite:
                    val_y = float(evaluacion_sp)
                    if -1000000 < val_y < 1000000:
                        valores_x.append(val_x)
                        valores_y.append(val_y)
            except (TypeError, ValueError, Exception):
                continue

        ax.plot(valores_x, valores_y, color="blue", label=f"f(x) = {funcion}")
        
        if tendencia not in ["oo", "-oo", "inf", "-inf"]:
            ax.axvline(x=c_grafica, color="purple", linestyle="--", label=f"x -> {tendencia}")
            if valor_limite_grafica is not None and not limite_es_infinito:
                ax.plot(c_grafica, valor_limite_grafica, 'o', color="red", markersize=10, zorder=5, label=f"Límite ({c_grafica}, {valor_limite_grafica})")
                ax.axhline(y=valor_limite_grafica, color="purple", linestyle="--")
                
                #hace una especie de zoom para que se vea bien sin importar si el limite esgrande o pequeño
                margen = max(5, abs(valor_limite_grafica) * 0.5)
                ax.set_ylim(valor_limite_grafica - margen, valor_limite_grafica + margen)
        
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()
        ax.set_title("Gráfica de la Función")

        canvas = FigureCanvasTkAgg(fig, master=lado_derecho)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    except (sp.SympifyError, TypeError, SyntaxError):
        resultado.configure(text="Error: la función no es válida o está mal escrita")
    except Exception as e:#por si falla avisa
        resultado.configure(text=f"Error al calcular el límite: {e}")
        

ingresar_datos = ctk.CTkTextbox(programa_calculo, width=200, height=30)
ingresar_datos.place(relx=0.01, rely=0.18)

ingresar_tendencia = ctk.CTkTextbox(programa_calculo, width=200, height=30)
ingresar_tendencia.place(relx=0.01, rely=0.32)

lado_derecho = ctk.CTkFrame(programa_calculo, width = 1, height=1)
lado_derecho.place(relx=0.4, rely=0.0, relwidth = 0.6, relheight = 1.0)

efe_de_x = ctk.CTkLabel(programa_calculo, text="Ingrese la función de su límite", font=("DejaVu Sans", 16))
efe_de_x.place(relx=0.01, rely=0.12)

tendencia_x = ctk.CTkLabel(programa_calculo, text="Ingrese la tendencia a 'x'", font=("DejaVu Sans", 16))
tendencia_x.place(relx=0.01, rely=0.26) 

funciones_rapidas = ctk.CTkLabel(programa_calculo, text="Funciones rápidas", font=("DejaVu Sans", 16))
funciones_rapidas.place(relx=0.01, rely=0.40)

resultado = ctk.CTkLabel(programa_calculo, text="Resultado del límite:", font=("DejaVu Sans", 16))
resultado.place(relx=0.01, rely=0.64)

cos_boton = ctk.CTkButton(programa_calculo, text="cos(x)", command=coseno, width=60, fg_color="green", hover_color="darkgreen")
cos_boton.place(relx=0.01, rely=0.46)

sin_boton = ctk.CTkButton(programa_calculo, text="sin(x)", command=sin, width=60, fg_color="green", hover_color="darkgreen")
sin_boton.place(relx=0.08, rely=0.46)

tan_boton = ctk.CTkButton(programa_calculo, text="tan(x)", command=tangente, width=60, fg_color="green", hover_color="darkgreen")
tan_boton.place(relx=0.15, rely=0.46)

sqrt_boton = ctk.CTkButton(programa_calculo, text="√x", command=raiz_cuadrada, width=60, fg_color="green", hover_color="darkgreen")
sqrt_boton.place(relx=0.01, rely=0.51)

sqr_boton = ctk.CTkButton(programa_calculo, text="x²", command=cuadrado, width=60, fg_color="green", hover_color="darkgreen")
sqr_boton.place(relx=0.08, rely=0.51)

exp_boton = ctk.CTkButton(programa_calculo, text="x**n", command=exp, width=60, fg_color="green", hover_color="darkgreen")
exp_boton.place(relx=0.15, rely=0.51)

inf_boton = ctk.CTkButton(programa_calculo, text="oo", command=infinito, width=60, fg_color="green", hover_color="darkgreen")
inf_boton.place(relx=0.01, rely=0.56)

infneg_boton = ctk.CTkButton(programa_calculo, text="-oo", command=inf_neg, width=60, fg_color="green", hover_color="darkgreen")
infneg_boton.place(relx=0.08, rely=0.56)

limpiar_boton = ctk.CTkButton(programa_calculo, text="Limpiar", command=limpiar, width=60, fg_color="green", hover_color="darkgreen")
limpiar_boton.place(relx=0.15, rely=0.56)

calcular_boton = ctk.CTkButton(programa_calculo, text="Calcular el límite", command=calcular, fg_color="green", hover_color="darkgreen")
calcular_boton.place(relx=0.01, rely=0.72)

eid_label = ctk.CTkLabel(programa_calculo, text="E\nI\nD\n\n-\n\nL\nI\nM\nI\nT\nE\nS", font=("DejaVu Sans", 24, "bold"))
eid_label.place(relx=0.35, rely=0.15)

programa_calculo.mainloop()
