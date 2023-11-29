import json

import os
from tkinter import DoubleVar, Radiobutton, Tk, Toplevel, messagebox
from tkinter import Label, Entry, Button, Frame, LabelFrame
from tkinter.ttk import Combobox
from calculos import calcula_dict, calcula_planta, calcula_vazao_complementar

root = Tk()

diametro_inicial = DoubleVar()

def update():
    datos = {
        "vazao": entry_vazao.get(),
        "diametro": float(combo_diametro.get()),
        "comprimento": entry_comprimento.get(),
        "hf": entry_hf.get(),
        "largura_planta": entry_largura_planta.get(),
        "largura_aspersor": entry_largura_aspersor.get(),
        "vazao_aspersor": entry_vazao_aspersor.get(),
        "diametro_inicial": diametro_inicial.get()
        
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
            combo_diametro.set(dados["diametro"])
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

            if diametro_inicial.get() == 22.0:
                radio_button_22.select()
            else:
                radio_button_29.select()



            

            




            calculate_ui()

    else:
        entry_vazao.delete(0, "end")
        combo_diametro.delete(0, "end")
        entry_comprimento.delete(0, "end")
        entry_hf.delete(0, "end")
def calculate_ui():
    dict_entrada = calcula_dict(
        c41_vazao=float(entry_vazao.get()),
        c42_diametro=float(combo_diametro.get()),
        c45_comprimento=float(entry_comprimento.get()),
        c49_hf=float(entry_hf.get()),
        )
    preenche_entry_inativa(entry_vazao_l, dict_entrada["vazao_l"])
    preenche_entry_inativa(entry_velocidade, dict_entrada["velocidade"])
    preenche_entry_inativa(entry_hf_unitaria, dict_entrada["hf_unitaria"])
    preenche_entry_inativa(entry_desnivel, dict_entrada["desnivel"])
    preenche_entry_inativa(entry_hf_linha, dict_entrada["hf_na_linha"])
    preenche_entry_inativa(entry_hf_total, dict_entrada["hf_total"])

    dict_saida = calcula_dict(
        c41_vazao=float(entry_vazao.get()),
        c42_diametro=complementa_diametro(float(combo_diametro.get())),
        c45_comprimento=float(entry_comprimento.get()),
        c49_hf=float(entry_hf.get()),
        )
    
    preenche_entry_inativa(entry_vazao_saida, entry_vazao.get())
    preenche_entry_inativa(entry_diametro_saida, complementa_diametro(float(combo_diametro.get())))
    preenche_entry_inativa(entry_comprimento_saida, float(entry_comprimento.get()))
    preenche_entry_inativa(entry_hf_saida, float(entry_hf.get()))


    preenche_entry_inativa(entry_vazao_l_saida, dict_saida["vazao_l"])
    preenche_entry_inativa(entry_velocidade_saida, dict_saida["velocidade"])
    preenche_entry_inativa(entry_hf_unitaria_saida, dict_saida["hf_unitaria"])
    preenche_entry_inativa(entry_desnivel_saida, dict_saida["desnivel"])
    preenche_entry_inativa(entry_hf_linha_saida, dict_saida["hf_na_linha"])
    preenche_entry_inativa(entry_hf_total_saida, dict_saida["hf_total"])
    
    
    
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
    calculate_ui()


def on_combo_select(event):
    print(event.widget.get())
    update()
    calculate()
    calculate_ui()

    

        
def complementa_diametro(diametro):
    if diametro == 22.0:
        return 29.0
    elif diametro == 29.0:
        return 35.0
    elif diametro == 35.0:
        return 50.0
    else:
        return 75.0

def calculate():

    wait_dialog = Toplevel(root)
    wait_dialog.title("Calculando, Por favor, aguarde...")
    wait_dialog.geometry("200x100")
    wait_dialog.resizable(False, False)
    wait_dialog.transient(root)

        
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    wait_dialog.geometry(f"+{x}+{y}")

  
        
  
    wait_dialog.grab_set()
    wait_dialog.wait_visibility()
    

    diametro_entrada = float(combo_diametro.get())
    diametro_saida = complementa_diametro(diametro_entrada)

    vazao = calcula_vazao_complementar(float(entry_vazao.get()), 
                                       float(entry_comprimento.get()), 
                                       float(entry_hf.get()), 
                                       diametro_entrada, 
                                       diametro_saida)
    
    
    entry_vazao.delete(0, "end")
    entry_vazao.insert(0, vazao)

    preenche_entry_inativa(entry_vazao_saida, vazao)
    preenche_entry_inativa(entry_diametro_saida, complementa_diametro(float(combo_diametro.get())))
    preenche_entry_inativa(entry_comprimento_saida, float(entry_comprimento.get()))
    preenche_entry_inativa(entry_hf_saida, float(entry_hf.get()))

    wait_dialog.destroy()

  





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
    hf = float(entry_hf.get())
    dict_planta = calcula_planta(
        largura_planta=largura_planta,
        largura_aspersor=largura_aspersor,
        vazao_aspersor=vazao_aspersor,
        vazao_litro=vazao_litros,
         comprimento=comprimento,
        hf=hf,
        diametro_entrada=diametro_inicial.get(),
        diametro_saida=22.0 if diametro_inicial.get() == 29.0 else 22.0

    )

    preenche_entry_inativa(entry_quantidade_aspersor, dict_planta["qtd_aspersor"])
   
    preenche_entry_inativa(entry_tubo_25, dict_planta["tubo25"])
    preenche_entry_inativa(entry_tubo_32, dict_planta["tubo32"])
    preenche_entry_inativa(entry_tubo_35, dict_planta["tubo35"])
    preenche_entry_inativa(entry_tubo_50, dict_planta["tubo50"])

    update()



    




validate_float = root.register(validar_float)
validate_int = root.register(validar_int)

"""Criação do Frame Pai"""
frame_pai = Frame(root)


"""Criação dos radio buttons"""
frame_radio = LabelFrame(root, text="Diametro de Entrada")
frame_radio.pack(padx=0, pady=0)

radio_button_22 = Radiobutton(frame_radio, text="22mm", variable=diametro_inicial, value=22.0)
radio_button_22.grid(row=0, column=0, padx=0, pady=0)


radio_button_29 = Radiobutton(frame_radio, text="29mm", variable=diametro_inicial, value=29.0)
radio_button_29.grid(row=0, column=1, padx=0, pady=0)



def update_labels(*args):
    if diametro_inicial.get() == 29.0:
        label_tubo1.config(text='                   Tubo 32mm')
        label_tubo2.config(text='Tubo 35mm')
        label_tubo3.config(text='Tubo 50mm')
        label_tubo4.config(text='Tubo 75mm')
    else:
        label_tubo1.config(text='                   Tubo 25mm')
        label_tubo2.config(text='Tubo 32mm')
        label_tubo3.config(text='Tubo 35mm')
        label_tubo4.config(text='Tubo 50mm')

diametro_inicial.trace("w", update_labels)






frame_pai.pack(padx=10, pady=0)


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
combo_diametro = Combobox(frame_entrada, values=["22.0", "29.0", "35.0", "50.0"], state="readonly", width=16)
combo_diametro.grid(row=1, column=1, padx=10, pady=10)
combo_diametro.bind("<<ComboboxSelected>>", on_combo_select)
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
frame_planta.grid(row=0, column=0, padx=0, pady=(10,0))

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
frame_tubulacoes.grid(row=1, column=0, padx=0, pady=(10,10))

label_tubo1 = Label(frame_tubulacoes, text="                   Tubo 25mm: ")
label_tubo1.grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_tubo_25 = Entry(frame_tubulacoes, state="readonly", takefocus=False)
entry_tubo_25.grid(row=0, column=1, padx=10, pady=10, sticky="e")

label_tubo2 = Label(frame_tubulacoes, text="Tubo 32mm: ")
label_tubo2.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_tubo_32 = Entry(frame_tubulacoes, state="readonly", takefocus=False)
entry_tubo_32.grid(row=1, column=1, padx=10, pady=10, sticky="e")

label_tubo3 = Label(frame_tubulacoes, text="Tubo 35mm: ")
label_tubo3.grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_tubo_35 = Entry(frame_tubulacoes, state="readonly", takefocus=False)
entry_tubo_35.grid(row=2, column=1, padx=10, pady=10, sticky="e")

label_tubo4 = Label(frame_tubulacoes, text="Tubo 50mm: ")
label_tubo4.grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_tubo_50 = Entry(frame_tubulacoes, state="readonly", takefocus=False)
entry_tubo_50.grid(row=3, column=1, padx=10, pady=10, sticky="e")





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
