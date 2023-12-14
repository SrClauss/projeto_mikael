import math
def calcula_hf_total(c41_vazao, c42_diametro, c45_comprimento, c49_hf):
    d40 = (c42_diametro/2)/10.0
    d41 = (d40**2)*math.pi*0.36
    d42 = ((c42_diametro/1000.0)**0.63)*49.7
    c43_velocidade = c41_vazao/d41
    c44_hf_unitaria = (c43_velocidade/d42)**1.852
    c46_desnivel = c49_hf*c45_comprimento
    c47_hf_na_linha = c44_hf_unitaria*c45_comprimento
    return c46_desnivel+c47_hf_na_linha




def calcula_dict(c41_vazao, c42_diametro, c45_comprimento, c49_hf):
    d40 = (c42_diametro/2)/10.0
    d41 = (d40**2)*math.pi*0.36
    d42 = ((c42_diametro/1000.0)**0.63)*49.7
    c43_velocidade = c41_vazao/d41
    c44_hf_unitaria = (c43_velocidade/d42)**1.852
    c46_desnivel = c49_hf*c45_comprimento
    c47_hf_na_linha = c44_hf_unitaria*c45_comprimento
    return {
        "vazao_l": round(c41_vazao*1000, 4),
        "velocidade": round(c43_velocidade, 4),
        "hf_unitaria": round(c44_hf_unitaria, 4),
        "desnivel": round(c46_desnivel, 4),
        "hf_na_linha": round(c47_hf_na_linha, 4),
        "hf_total": round(c46_desnivel + c47_hf_na_linha, 4)
    }

def calcula_planta(largura_planta, largura_aspersor, vazao_litro, vazao_aspersor, comprimento, hf, diametro_entrada, diametro_saida, area_setor):
    qtd_aspersor = largura_planta/largura_aspersor
    area = calcula_vazao_complementar(vazao_litro/1000,comprimento,hf,diametro_entrada,diametro_saida)*1000/vazao_aspersor/qtd_aspersor*largura_planta*comprimento
    tubo1 = area
    area_setor = area_setor - tubo1 if area_setor - tubo1 > 0 else 0
    tubo2 = area/1.997 if area_setor > area/1.997 else area_setor 
    area_setor = area_setor - tubo2 if area_setor - tubo2 > 0 else 0
    tubo3 = area/1.8 if area_setor > area/1.8  else area_setor
    area_setor = area_setor - tubo3 if area_setor - tubo3 > 0 else 0
    tubo4 = area/2.88 if area_setor > area/2.88  else area_setor
    return {
        "qtd_aspersor": round(qtd_aspersor, 2), 
        "tubo1": round(tubo1, 2),
        "tubo2": round(tubo2, 2),
        "tubo3": round(tubo3, 2),
        "tubo4": round(tubo4, 2)
    }


        



def calcula_vazao_complementar(c41_vazao, c45_comprimento, c49_hf, diametro_entrada, diametro_saida):
    hf_total_entrada = calcula_hf_total(c41_vazao, diametro_entrada, c45_comprimento, c49_hf)
    hf_total_saida = calcula_hf_total(c41_vazao, diametro_saida, c45_comprimento, c49_hf)
    
    print("valores iniciais")
    print("hf{0} = {1}, hf{2} = {3}".format(diametro_entrada, hf_total_entrada, diametro_saida, hf_total_saida))
    print("**************************************************************")
    i = 0.005
    

    if hf_total_entrada > hf_total_saida *-1.0:
        while hf_total_entrada > hf_total_saida *-1.0:
            c41_vazao -= i
            hf_total_entrada = calcula_hf_total(c41_vazao, diametro_entrada, c45_comprimento, c49_hf)
            hf_total_saida = calcula_hf_total(c41_vazao, diametro_saida, c45_comprimento, c49_hf)
            print("hf{0} = {1}, hf{2} = {3}".format(diametro_entrada, hf_total_entrada, diametro_saida, hf_total_saida))
    if hf_total_entrada < hf_total_saida *-1.0:
        while hf_total_entrada < hf_total_saida *-1.0:
            c41_vazao += i
            hf_total_entrada = calcula_hf_total(c41_vazao, diametro_entrada, c45_comprimento, c49_hf)
            hf_total_saida = calcula_hf_total(c41_vazao, diametro_saida, c45_comprimento, c49_hf)
            print("hf{0} = {1}, hf{2} = {3}".format(diametro_entrada, hf_total_entrada, diametro_saida, hf_total_saida))

    return round(c41_vazao, 4)
