#Importamos las librerias necesarias
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

#creamos la ventana principal y su aspecto en general (dependiendo del tema del computador, 
#es decir si esta en modo claro o modo oscuro)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
programa_calculo = ctk.CTk()
programa_calculo.title("EID-CALCULO-LIMITES")
programa_calculo.geometry("1080x720")
