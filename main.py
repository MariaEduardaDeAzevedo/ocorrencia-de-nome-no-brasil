import matplotlib.pyplot as plt
import json
import requests
import os
import sys

def has_dir(nome):
    for d in os.listdir("./relatorios"):
        if d == nome:
            return True
    return False

def requerimento(nome):
    req = requests.get(f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}")
    return json.loads(req.text)[0]

def busca_nome(nome):
    try:
        dados = requerimento(nome)
        dados_recorrencia = dados['res']

        periodos = list()
        recorrencias = list()

        for dado in dados_recorrencia:
            periodos.append(dado['periodo'].split(",")[0].strip("["))
            recorrencias.append(dado['frequencia'])

        titulo = f"Recorrência do nome {dados['nome']} entre as décadas de 1930-2010 [{sum(recorrencias)} registros]"
        rel = ""

        for k in dados.keys():
            if k != 'res':
                rel += f"{k}: {dados[k]}\n"

        plt.title(titulo)
        plt.bar(periodos, recorrencias)
        plt.plot(periodos, recorrencias)

        if not has_dir(nome):
            os.mkdir(f"./relatorios/{nome}")

        rel_file = open(f"./relatorios/{nome}/{nome}.txt", "w")
        rel_file.write("")
        rel_file.write(rel)
        rel_file.close()
        plt.savefig(f"./relatorios/{nome}/{nome}")
        print(f"Abrindo resultados... um relatório será salvo no diretório ./relatorios/{nome}")
        plt.show() 
        plt.close()   
    except IndexError:
        print("Nenhum registro encontrado")

def ranking_geral():
    dados = requerimento("ranking")['res']

    nomes = list()
    recorrencias = list()

    for dado in dados:
        nomes.append(dado['nome'])
        recorrencias.append(dado['frequencia'])

    plt.title("Ranking dos 20 nomes mais populares no Brasil entre 1930-2010")
    plt.barh(nomes, recorrencias)
    plt.show()
    plt.close()

def lista_relatorios():
    retorno = "Relatórios já gerados anteriormente\n"
    cont = 1    
    for directory in os.listdir("./relatorios"):
        retorno += f"\n{cont}. {directory}"
        cont += 1

    return retorno


op = sys.argv

if op[1].strip() == 'rel':
    if len(op) > 2:
        if has_dir(op[2].strip()):
            print (f"Diretório ./relatorios/{op[2].strip()} existente")
        else:
            print (f"Diretório ./relatorios/{op[2].strip()} inexistente. Pesquise para gerar relatório")
    else:
        print(lista_relatorios())
elif op[1].strip() != 'ranking':
    busca_nome(op[1].strip())
else:
    ranking_geral()
