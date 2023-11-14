import datetime
import json
import os
from tkinter import Tk, messagebox
from tkinter import Label, Entry, Button, Frame, LabelFrame
from tkinter.ttk import Combobox
import requests

from calculos import calcula_dict, calcula_planta, calcula_vazao_complementar

root = Tk()


def update():
    datos = {
        "vazao": entry_vazao.get(),
        "diametro": combo_diametro.get(),
        "comprimento": entry_comprimento.get(),
        "hf": entry_hf.get(),
        "largura_planta": entry_largura_planta.get(),
        "largura_aspersor": entry_largura_aspersor.get(),
        "vazao_aspersor": entry_vazao_aspersor.get(),
        
    }
    json_string = json.dumps(datos)
    with open("valor.json", "w") as f:
        f.write(json_string)
def get_json():
    if os.path.exists("valor.json"):
        with open("valor.json", "r") as f:
            json_string = f.read()
            dados = json.loads(json_string)
            entry_vazao.delete(0, "end")
            entry_vazao.insert(0, dados["vazao"])
            if float(dados["diametro"]) == 22.0:
                combo_diametro.set("22.0")
            else:
                combo_diametro.set("29.0")

            entry_comprimento.delete(0, "end")
            entry_comprimento.insert(0, dados["comprimento"])
            entry_hf.delete(0, "end")
            entry_hf.insert(0, dados["hf"])
            entry_largura_planta.delete(0, "end")
            entry_largura_planta.insert(0, dados["largura_planta"])
            entry_largura_aspersor.delete(0, "end")
            entry_largura_aspersor.insert(0, dados["largura_aspersor"])
            entry_vazao_aspersor.delete(0, "end")
            entry_vazao_aspersor.insert(0, dados["vazao_aspersor"])
           



            calculate_ui()

    else:
        entry_vazao.delete(0, "end")
        combo_diametro.delete(0, "end")
        entry_comprimento.delete(0, "end")
        entry_hf.delete(0, "end")
def calculate_ui():
    dict = calcula_dict(float(entry_vazao.get()), float(combo_diametro.get()), float(entry_comprimento.get()), float(entry_hf.get()))
    preenche_entry_inativa(entry_vazao_l, dict["vazao_l"])
    preenche_entry_inativa(entry_velocidade, dict["velocidade"])
    preenche_entry_inativa(entry_hf_unitaria, dict["hf_unitaria"])
    preenche_entry_inativa(entry_desnivel, dict["desnivel"])
    preenche_entry_inativa(entry_hf_linha, dict["hf_na_linha"])
    preenche_entry_inativa(entry_hf_total, dict["hf_total"])
    
def validar_float(valor):
    if valor == "" or valor == "-":
        return True
    try:
        valor = valor.replace(",", ".")
        float(valor)
        return True
    except ValueError:
        if valor.startswith('-'):
            try:
                float(valor[1:])
                return True
            except ValueError:
                return False
        return False
def validar_int(valor):
    if valor == "" or valor == "-":
        return True
    try:
        int(valor)
        return True
    except ValueError:
        return False
def on_focus_out(e):
    entry = e.widget
    valor = e.widget.get()
    entry.delete(0, "end")    
    entry.insert(0, valor.replace(",", "."))

    if entry.get()[-1] == "." or entry.get()[-1] == ",":
        entry.insert("end", "0")
    if entry.get()[-1].isdigit():
        entry.insert("end", ".0")
    update()
    get_json()

        

 

def calculate():
    
    vazao = calcula_vazao_complementar(float(entry_vazao.get()), float(entry_comprimento.get()), float(entry_hf.get()))
    
    entry_vazao.delete(0, "end")
    entry_vazao.insert(0, vazao)

    preenche_entry_inativa(entry_vazao_saida, vazao)
    preenche_entry_inativa(entry_diametro_saida, 29.0 if float(combo_diametro.get())==22.0 else 22.0)
    preenche_entry_inativa(entry_comprimento_saida, float(entry_comprimento.get()))
    preenche_entry_inativa(entry_hf_saida, float(entry_hf.get()))


    resultado = calcula_dict(float(entry_vazao.get()), 29.0 if float(combo_diametro.get())==22.0 else 22, float(entry_comprimento.get()), float(entry_hf.get()))

    preenche_entry_inativa(entry_vazao_l_saida, resultado["vazao_l"])
    preenche_entry_inativa(entry_velocidade_saida, resultado["velocidade"])
    preenche_entry_inativa(entry_hf_unitaria_saida, resultado["hf_unitaria"])
    preenche_entry_inativa(entry_desnivel_saida, resultado["desnivel"])
    preenche_entry_inativa(entry_hf_linha_saida, resultado["hf_na_linha"])
    preenche_entry_inativa(entry_hf_total_saida, resultado["hf_total"])



    calculate_ui()



def preenche_entry_inativa(entry, valor):
    entry.config(state="normal")
    entry.delete(0, "end")
    entry.insert(0, valor)
    entry.config(state="readonly")

def calcula_ui_plantas():
    largura_planta = float(entry_largura_planta.get())
    largura_aspersor = float(entry_largura_aspersor.get())
    vazao_aspersor = float(entry_vazao_aspersor.get())
    vazao_litros = float(entry_vazao_l.get())
    comprimento = float(entry_comprimento.get())
    dict_planta = calcula_planta(
        largura_planta=largura_planta,
        largura_aspersor=largura_aspersor,
        vazao_aspersor=vazao_aspersor,
        vazao_litro=vazao_litros,
        comprimento=comprimento

    )

    preenche_entry_inativa(entry_quantidade_aspersor, dict_planta["qtd_aspersor"])
   
    preenche_entry_inativa(entry_tubo_25, dict_planta["tubo25"])
    preenche_entry_inativa(entry_tubo_32, dict_planta["tubo32"])
    preenche_entry_inativa(entry_tubo_35, dict_planta["tubo35"])

    update()



    




validate_float = root.register(validar_float)
validate_int = root.register(validar_int)

"""Criação do Frame Pai"""
frame_pai = Frame(root)
frame_pai.pack(padx=10, pady=10)


"""Criação do Frame Entrada"""
frame_entrada = LabelFrame(frame_pai, text="Entrada")
frame_entrada.grid(row=0, column=0)

frame_vazao = Frame(frame_entrada)
frame_vazao.grid(row=0, column=0, columnspan=2, sticky="e")

Label(frame_vazao, text="Vazão(m³/h): ").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_vazao = Entry(frame_vazao)
entry_vazao.grid(row=0, column=1, padx=10, pady=10)


Label(frame_vazao, text="Vazão(\u2113/h): ").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_vazao_l = Entry(frame_vazao, state="readonly", takefocus=False)
entry_vazao_l.grid(row=1, column=1, padx=10, pady=10)

Label(frame_entrada, text="Diametro Interno: ").grid(row=1, column=0, padx=10, pady=10, sticky="e", )
combo_diametro = Combobox(frame_entrada, values=["22.0", "29.0"], state="readonly", width=16)
combo_diametro.grid(row=1, column=1, padx=10, pady=10)
combo_diametro.bind("<<ComboboxSelected>>", on_focus_out)
combo_diametro.bind("<FocusOut>", on_focus_out)

Label(frame_entrada, text="Velocidade: ").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_velocidade = Entry(frame_entrada, state="readonly", takefocus=False)
entry_velocidade.grid(row=2, column=1, padx=10, pady=10)

Label(frame_entrada, text="HF Unitária: ").grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_hf_unitaria = Entry(frame_entrada, state="readonly", takefocus=False)
entry_hf_unitaria.grid(row=3, column=1, padx=10, pady=10)

Label(frame_entrada, text="Comprimento: ").grid(row=4, column=0, padx=10, pady=10, sticky="e")
entry_comprimento = Entry(frame_entrada)
entry_comprimento.grid(row=4, column=1, padx=10, pady=10)

Label(frame_entrada, text="Desnivel: ").grid(row=5, column=0, padx=10, pady=10, sticky="e")
entry_desnivel = Entry(frame_entrada, state="readonly", takefocus=False)
entry_desnivel.grid(row=5, column=1, padx=10, pady=10)

Label(frame_entrada, text="HF na Linha: ").grid(row=6, column=0, padx=10, pady=10, sticky="e")
entry_hf_linha = Entry(frame_entrada, state="readonly", takefocus=False)
entry_hf_linha.grid(row=6, column=1, padx=10, pady=10)

Label(frame_entrada, text="HF Total: ").grid(row=7, column=0, padx=10, pady=10, sticky="e")
entry_hf_total = Entry(frame_entrada, state="readonly", takefocus=False)
entry_hf_total.grid(row=7, column=1, padx=10, pady=10)

Label(frame_entrada, text="HF: ").grid(row=8, column=0, padx=10, pady=10, sticky="e")
entry_hf = Entry(frame_entrada)
entry_hf.grid(row=8, column=1, padx=10, pady=10)




   


"""Criação do Frame Saída"""

frame_saida = LabelFrame(frame_pai, text="Saida")

frame_saida.grid(row=0, column=1, padx=10, pady=10)

frame_vazao_saida = Frame(frame_saida)
frame_vazao_saida.grid(row=0, column=0, columnspan=2, sticky="e")


Label(frame_vazao_saida, text="Vazão(m³/h): ").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_vazao_saida = Entry(frame_vazao_saida, state="readonly", takefocus=False)
entry_vazao_saida.grid(row=0, column=1, padx=10, pady=10)


Label(frame_vazao_saida, text="Vazão(\u2113/h): ").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_vazao_l_saida = Entry(frame_vazao_saida, state="readonly", takefocus=False)
entry_vazao_l_saida.grid(row=1, column=1, padx=10, pady=10)



Label(frame_saida, text="Diametro Interno: ").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_diametro_saida = Entry(frame_saida, state="readonly", takefocus=False)
entry_diametro_saida.grid(row=1, column=1, padx=10, pady=10)

Label(frame_saida, text="Velocidade: ").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_velocidade_saida = Entry(frame_saida, state="readonly", takefocus=False)
entry_velocidade_saida.grid(row=2, column=1, padx=10, pady=10)

Label(frame_saida, text="HF Unitária: ").grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_hf_unitaria_saida = Entry(frame_saida, state="readonly", takefocus=False)
entry_hf_unitaria_saida.grid(row=3, column=1, padx=10, pady=10)

Label(frame_saida, text="Comprimento: ").grid(row=4, column=0, padx=10, pady=10, sticky="e")
entry_comprimento_saida = Entry(frame_saida, state="readonly", takefocus=False)
entry_comprimento_saida.grid(row=4, column=1, padx=10, pady=10)

Label(frame_saida, text="Desnivel: ").grid(row=5, column=0, padx=10, pady=10, sticky="e")
entry_desnivel_saida = Entry(frame_saida, state="readonly", takefocus=False)
entry_desnivel_saida.grid(row=5, column=1, padx=10, pady=10)

Label(frame_saida, text="HF na Linha: ").grid(row=6, column=0, padx=10, pady=10, sticky="e")
entry_hf_linha_saida = Entry(frame_saida, state="readonly", takefocus=False)
entry_hf_linha_saida.grid(row=6, column=1, padx=10, pady=10)

Label(frame_saida, text="HF Total: ").grid(row=7, column=0, padx=10, pady=10, sticky="e")
entry_hf_total_saida = Entry(frame_saida, state="readonly", takefocus=False)
entry_hf_total_saida.grid(row=7, column=1, padx=10, pady=10)

Label(frame_saida, text="HF: ").grid(row=8, column=0, padx=10, pady=10, sticky="e")
entry_hf_saida = Entry(frame_saida, state="readonly", takefocus=False)
entry_hf_saida.grid(row=8, column=1, padx=10, pady=10)



frame_planta_tubulacoes = Frame(frame_pai)
frame_planta_tubulacoes.grid(row=0, column=2, sticky="N")

"""Criação do Frame Planta"""


frame_planta = LabelFrame(frame_planta_tubulacoes, text="Planta")
frame_planta.grid(row=0, column=0, padx=0, pady=10)

Label(frame_planta, text="Largura da Planta: ").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_largura_planta = Entry(frame_planta)
entry_largura_planta.grid(row=0, column=1, padx=10, pady=10)

Label(frame_planta, text="Largura do Aspersor: ").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_largura_aspersor = Entry(frame_planta)
entry_largura_aspersor.grid(row=1, column=1, padx=10, pady=10)

Label(frame_planta, text="Vazão do Aspersor: ").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_vazao_aspersor = Entry(frame_planta)
entry_vazao_aspersor.grid(row=2, column=1, padx=10, pady=10)

Label(frame_planta, text="Aspersores por planta: ").grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_quantidade_aspersor = Entry(frame_planta, state="readonly", takefocus=False)
entry_quantidade_aspersor.grid(row=3, column=1, padx=10, pady=10)





"""Criação do Frame Tubulações"""



frame_tubulacoes = LabelFrame(frame_planta_tubulacoes, text="Tubulacões")
frame_tubulacoes.grid(row=1, column=0, padx=0, pady=(47,10))

Label(frame_tubulacoes, text="                   Tubo 25mm: ").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_tubo_25 = Entry(frame_tubulacoes, state="readonly", takefocus=False)
entry_tubo_25.grid(row=0, column=1, padx=10, pady=10, sticky="e")

Label(frame_tubulacoes, text="Tubo 32mm: ").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_tubo_32 = Entry(frame_tubulacoes, state="readonly", takefocus=False)
entry_tubo_32.grid(row=1, column=1, padx=10, pady=10, sticky="e")

Label(frame_tubulacoes, text="Tubo 35mm: ").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_tubo_35 = Entry(frame_tubulacoes, state="readonly", takefocus=False)
entry_tubo_35.grid(row=2, column=1, padx=10, pady=10, sticky="e")








button_calcular = Button(frame_pai, text="Calcular", command=calculate, width=77, height=3)
button_calcular.grid(row=3, column=0, columnspan=2, sticky="w")

button_calcular_planta = Button(frame_pai, text="Calcular Planta", command=calcula_ui_plantas, width=42, height=3)
button_calcular_planta.grid(row=3, column=1, columnspan=2, sticky="e")

entries_variaveis = [entry_vazao, combo_diametro, entry_comprimento, entry_hf, 
                     entry_largura_planta, entry_largura_aspersor, entry_vazao_aspersor]



for entrie in entries_variaveis:
    entrie.config(validate="key", validatecommand=(validate_float, '%P'))
    entrie.bind("<FocusOut>", on_focus_out)


frame_copyright = Frame(root)
frame_copyright.pack(side='right', padx=10, pady=10)
Label(frame_copyright, text="Copyright © 2023 - Safra Rural: by Mikael Bergamin").grid(sticky="w", row=0, column=0, padx=10, pady=10)
get_json()







root.wm_title("By Safra Rural")
root.iconbitmap("res/safra.ico")
root.wm_iconify()


root.mainloop()
