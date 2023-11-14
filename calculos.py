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

def calcula_planta(largura_planta, largura_aspersor, vazao_litro, vazao_aspersor, comprimento):
    qtd_aspersor = largura_planta/largura_aspersor
    area = vazao_litro/vazao_aspersor/qtd_aspersor*largura_planta*comprimento
    
    return {
        "qtd_aspersor": round(qtd_aspersor, 2), 
        "tubo25": round(area, 2),
        "tubo32": round(area *1.997, 2),
        "tubo35": round(area *1.8, 2)
    }
        



def calcula_vazao_complementar(c41_vazao, c45_comprimento, c49_hf):
     
    hf_total_22 = calcula_hf_total(c41_vazao, 22.0, c45_comprimento, c49_hf)
    hf_total_29 = calcula_hf_total(c41_vazao, 29.0, c45_comprimento, c49_hf)
    print("valores iniciais")
    print("hf22 = {0}, hf29 = {1}".format(hf_total_22, hf_total_29))
    print("**************************************************************")
    i = 0.0005
    

    if hf_total_22 > hf_total_29 *-1.0:
        while hf_total_22 > hf_total_29 *-1.0:
            c41_vazao -= i
            hf_total_22 = calcula_hf_total(c41_vazao, 22.0, c45_comprimento, c49_hf)
            hf_total_29 = calcula_hf_total(c41_vazao, 29.0, c45_comprimento, c49_hf)
            print("hf22 = {0}, hf29 = {1}".format(hf_total_22, hf_total_29))
    if hf_total_22 < hf_total_29 *-1.0:
        while hf_total_22 < hf_total_29 *-1.0:
            c41_vazao += i
            hf_total_22 = calcula_hf_total(c41_vazao, 22.0, c45_comprimento, c49_hf)
            hf_total_29 = calcula_hf_total(c41_vazao, 29.0, c45_comprimento, c49_hf)
            print("hf22 = {0}, hf29 = {1}".format(hf_total_22, hf_total_29))
    return round(c41_vazao, 4)






            
               
          