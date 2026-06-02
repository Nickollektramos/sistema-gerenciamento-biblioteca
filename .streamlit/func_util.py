from arvorebinaria import ArvoreBinaria
from datetime import date, datetime
import streamlit as st

def validarInt(msg):
    valor = 0
    n = str(input(msg))
    if n.isnumeric():
        valor = int(n)
        return valor
    else:
        print('ERRO! Digite um número inteiro: ')

def validarData(msg):
    n = str(input(msg)).strip()
    try:
        data = datetime.strptime(n, '%Y-%m-%d').date()
        return data
    except ValueError:
        print('Digite uma data válida!')
    

# def validarUf(msg):
#     ufs = {"AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
#            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
#            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"}
#     n = str(input(msg)).strip().upper()
#     if n in ufs:
#         return n
#     else: 
#         print('ERRO! Digite uma UF válida!')

def construirArvore(arquivo):
    arv = ArvoreBinaria()
    with open(arquivo, 'rt', encoding="utf-8") as arq:
        pos=0
        for linha in arq:
            campos = linha.strip().split(';')
            cod = int(campos[0])
            arv.inserir_no(cod, pos)
            pos += 1
    return arv

def inserirDados(arquivo, dados, cod, arv):
    with open(arquivo, 'at', encoding="utf-8") as arq:
        arq.write(dados)

    with open(arquivo, 'rt', encoding="utf-8")as arq:
        pos = sum(1 for _ in arq) - 1

    arv.inserir_no(cod, pos)

def deletarDados(arquivo, cod, arv):
    cod = int(cod)
    arq_atualizado = []
    encontrado = False
    with open(arquivo, 'rt', encoding="utf-8") as arq:
        linhas = arq.readlines()
    for linha in linhas:
        if not linha.strip():
            continue
        campos = linha.strip().split(';')
        cod_arq = int(campos[0])
        if cod == cod_arq:
            encontrado = True
        else:
            arq_atualizado.append(linha)
    if not encontrado:
        print(f'Código {cod} não encontrado!')
        return
    with open(arquivo, 'wt', encoding="utf-8") as arq:
        arq.writelines(arq_atualizado)

    arv_atualizada = construirArvore(arquivo)
    arv.raiz = arv_atualizada.raiz
    print('Registro excluído com sucesso!')

def atualizarDisp(cod_livro, status):
    livros = []
    livro_encon = False
    with open('arquivos/livros.txt', 'rt', encoding="utf-8") as arq_livro:
            for linha in arq_livro:
                campos = linha.strip().split(';')
                cod_arq_livro = int(campos[0])
                titulo = campos[1]
                if cod_livro == cod_arq_livro:
                    campos[5] = status
                    linha = ';'.join(campos)
                    livro_encon = True
                    msg = f'O livro {titulo} agora está {"disponível" if status == "S" else "emprestado"}!'
                livros.append(linha.strip())
    if livro_encon:
        with open('arquivos/livros.txt', 'wt', encoding="utf-8") as atual_livro:
            for linha in livros:
                atual_livro.write(linha + '\n')
    return msg
    
def verificarAtraso(data_dev):
    hoje = date.today()
    if hoje > data_dev:
        dias = (hoje - data_dev).days
        print(f'A devolução está atrasada a {dias} dias!\n')    

def tabela_front(colunas, cabecalhos, linhas):
    for cl, cb in zip(colunas, cabecalhos):
        cl.write(f'{cb}')
    st.write('---')
    for linha in linhas:
        if '|' not in linha:
            st.info(linha)
            continue
        campos = linha.strip().split('|')
        for c, cp in zip(colunas, campos):
            if ':' in cp:
                _, valor = cp.split(':', 1)
                c.write(valor.strip())
            else:
                c.write(cp.strip())     