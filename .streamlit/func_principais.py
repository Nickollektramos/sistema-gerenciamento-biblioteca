import func_util
from datetime import datetime, date, timedelta

arvore_cidades = func_util.construirArvore('arquivos/cidades.txt')
arvore_cursos = func_util.construirArvore('arquivos/cursos.txt')
arvore_alunos = func_util.construirArvore('arquivos/alunos.txt')
arvore_autores = func_util.construirArvore('arquivos/autores.txt')
arvore_categorias = func_util.construirArvore('arquivos/categorias.txt')
arvore_livros = func_util.construirArvore('arquivos/livros.txt')
arvore_emprestimos = func_util.construirArvore('arquivos/emprestimos.txt')

#FUNÇÕES PARA ADIÇÃO DE DADOS

def add_cidades():
    cod = func_util.validarInt('Código: ')
    if cod is None:
        return
    
    if arvore_cidades.buscar(cod) is not None:
        print(f'Código {cod} já existe! Tente novamente.')
        return
    
    descricao = input('Nome: ')
    uf = input('UF: ')

    cidade = f"{cod};{descricao};{uf}\n"

    func_util.inserirDados('arquivos/cidades.txt', cidade, cod, arvore_cidades)
    print(f'Cidade {descricao} cadastrada com sucesso!')

def add_curso():
    cod = func_util.validarInt('Código: ')
    if cod is None:
        return
    
    if arvore_cursos.buscar(cod) is not None:
        print(f'Código {cod} já existe! Tente novamente.')
        return

    descricao = input('Nome: ')

    curso = f"{cod};{descricao}\n"

    func_util.inserirDados('arquivos/cursos.txt', curso, cod, arvore_cursos)
    print(f'Curso {descricao} cadastrado com sucesso!')

def add_alunos():
    cod = func_util.validarInt('Código: ')
    if cod is None:
        return
    
    if arvore_alunos.buscar(cod) is not None:
        print(f'Código {cod} já existe! Tente novamente.')
        return
    
    nome = input('Nome: ')
    cod_curso = func_util.validarInt('Código do curso: ')
    if cod_curso is None:
        return
    
    if buscarCurso(cod_curso, busca=True) is None:
        return
    
    cod_cid = func_util.validarInt('Código da cidade: ')
    if cod_cid is None:
        return

    alunos = f"{cod};{nome};{cod_curso};{cod_cid}\n"

    func_util.inserirDados('arquivos/alunos.txt', alunos, cod, arvore_alunos)
    print(f'Aluno(a) {nome} cadastrado(a) com sucesso!')

def add_autor():
    cod = func_util.validarInt('Código: ')
    if cod is None:
        return
    
    if arvore_autores.buscar(cod) is not None:
        print(f'Código {cod} já existe! Tente novamente.')
        return
    
    nome = input('Nome: ')
    cod_cid = func_util.validarInt('Código da cidade: ')
    if cod_cid is None:
        return

    autor = f"{cod};{nome};{cod_cid}\n"

    func_util.inserirDados('arquivos/autores.txt', autor, cod, arvore_autores)
    print(f'Autor(a) {nome} cadastrado(a) com sucesso!')

def add_categoria():
    cod = func_util.validarInt('Código: ')
    if cod is None:
        return
    
    if arvore_categorias.buscar(cod) is not None:
        print(f'Código {cod} já existe! Tente novamente.')
        return
    
    descricao = input('Nome: ')

    categoria = f"{cod};{descricao}\n"

    func_util.inserirDados('arquivos/categorias.txt', categoria, cod, arvore_categorias)

    print(f'Categoria {descricao} cadastrada com sucesso!')

def add_livros():
    cod = func_util.validarInt('Código: ')
    if cod is None:
        return
    
    if arvore_livros.buscar(cod) is not None:
        print(f'Código {cod} já existe! Tente novamente.')
        return
    
    titulo = input('Título: ')
    cod_autor = func_util.validarInt('Código do autor: ')
    if cod_autor is None:
        return
    
    buscarAutor(cod_autor, busca=True)

    cod_categ = func_util.validarInt('Código da categoria: ')
    if cod_categ is None:
        return
    
    buscarCateg(cod_categ, busca=True)

    ano_publicacao = func_util.validarInt('Ano de publicação: ')
    disponivel = 'S'

    livros = f"{cod};{titulo};{cod_autor};{cod_categ};{ano_publicacao};{disponivel}\n"

    func_util.inserirDados('arquivos/livros.txt', livros, cod, arvore_livros)

    print(f'Livro {titulo} cadastrado com sucesso!')

def add_emprestimos():
    cod = func_util.validarInt('Código: ')
    if cod is None:
        return
    
    if arvore_emprestimos.buscar(cod) is not None:
        print(f'Código {cod} já existe! Tente novamente.')
        return
    

    cod_livro = func_util.validarInt('Código do livro: ')
    if cod_livro is None:
        return
    if buscarLivro(cod_livro, busca=True) is None:
        return
    
    msg = func_util.atualizarDisp(cod_livro, 'N')

    cod_aluno = func_util.validarInt('Código do aluno: ')
    if cod_aluno is None:
        return
    if buscarAluno(cod_aluno, busca=True) is None:
        print(f'Aluno com código {cod} não encontrado!')
    
    data_emprestimo = date.today()
    data_devolucao = data_emprestimo + timedelta(days=7)
    devolvido = 'N'

    emprestimos = f"{cod};{cod_livro};{cod_aluno};{data_emprestimo};{data_devolucao};{devolvido}\n"

    func_util.inserirDados('arquivos/emprestimos.txt', emprestimos, cod, arvore_emprestimos)

    if "encontrado" in msg.lower():
        print(f'Empréstimo falhou! {msg}' )
    else:
        print(f'Empréstimo realizado com sucesso! {msg}' )
        

#BUSCA DE DADOS

def buscarCidade(cod, busca=None):
    cod = int(cod)
    pos = arvore_cidades.buscar(cod)
    if pos is not None:
        with open('arquivos/cidades.txt', 'rt', encoding="utf-8") as arq:
            for i, linha in enumerate(arq):
                if i == pos:
                    campos = linha.strip().split(';')
                    cod_arq = int(campos[0])
                    nome = campos[1]
                    uf = campos[2]
                    if cod == cod_arq:
                        if busca == True:
                            return nome, uf
                        else:
                            print(f'Código: {cod} | Nome: {nome} | UF: {uf}')
                            return
            return "Arquivo não encontrado!", "Arquivo não encontrado!"
    print(f'A cidade com código {cod} não foi encontrado!')

def buscarAutor(cod, busca=None):
    cod = int(cod)
    pos = arvore_autores.buscar(cod)
    if pos is not None:
        with open('arquivos/autores.txt', 'rt', encoding="utf-8") as arq:
            for i, linha in enumerate(arq):
                if i == pos:
                    campos = linha.strip().split(';')
                    cod_arq = int(campos[0])
                    nome = campos[1]
                    cidade = int(campos[2])
                    if cod == cod_arq:
                        nome_cid, uf = buscarCidade(cidade, busca=True)
                        if busca == True:
                            return {'Nome do autor': nome, 'Cidade': nome_cid, 'UF': uf}
                        else:
                            print(f'Código: {cod} | Nome: {nome} | Cidade: {nome_cid}/{uf}')
                            return
    print(f'O autor com código {cod} não foi encontrado!')

def buscarCateg(cod, busca=None):
    cod = int(cod)
    pos = arvore_categorias.buscar(cod)
    if pos is not None:
        with open('arquivos/categorias.txt', 'rt', encoding="utf-8") as arq:
            for i, linha in enumerate(arq):
                if i == pos:
                    campos = linha.strip().split(';')
                    cod_arq = int(campos[0])
                    descricao = campos[1]
                    if cod == cod_arq: 
                        if busca == True:
                            return {'Categoria': descricao}
                        else:
                            print(f'Código: {cod} | Descrição: {descricao}') 
                            return
    print(f'A categoria com código {cod} não foi encontrado!')

def buscarLivro(cod, ignorar=None, busca=None):
    cod = int(cod)
    pos = arvore_livros.buscar(cod)
    if pos is not None:
        with open('arquivos/livros.txt', 'rt', encoding="utf-8") as arq:
            for i, linha in enumerate(arq):
                if i == pos:
                    campos = linha.strip().split(';')
                    cod_arq = int(campos[0])
                    nome = campos[1]
                    cod_autor = int(campos[2])
                    categ = int(campos[3])
                    disponivel = campos[5]
                    autor = buscarAutor(cod_autor, busca=True)
                    categ = buscarCateg(categ, busca=True)
                    if cod == cod_arq:
                        if busca == True:
                            if disponivel in 'S' or ignorar:
                                return {'Título do livro': nome, 'Categoria': categ}
                            else:
                                if not ignorar:
                                    print(f'O livro {nome} não está disponível!')
                                    return None
                        else:
                            print(f'Código: {cod} | Título: {nome} | Autor: {autor['Nome do autor']} | Cidade do Autor: {autor['Cidade']}/{autor['UF']} | Categoria: {categ["Categoria"]} | Disponibilidade: {"Disponível" if disponivel == "S" else "Emprestado"}')
                            return
    print(f'O livro com código {cod} não foi encontrado!')

def buscarAluno(cod, busca=None):
    cod = int(cod)
    pos = arvore_alunos.buscar(cod)
    if pos is not None:
        with open('arquivos/alunos.txt', 'rt', encoding="utf-8") as arq:
            for i, linha in enumerate(arq):
                if i == pos:
                    campos = linha.strip().split(';')
                    cod_arq = int(campos[0])
                    nome = campos[1]     
                    cod_curso = campos[2]   
                    cidade = int(campos[3])
                    if cod == cod_arq:
                        nome_cid, uf = buscarCidade(cidade, busca=True)
                        curso = buscarCurso(cod_curso, busca=True)
                        if busca == True:
                            return {'Nome do aluno': nome, 'Cidade': nome_cid, 'UF': uf}
                        else:
                            print(f'Código: {cod} | Nome: {nome} | Curso: {curso['Curso']} | Cidade: {nome_cid}/{uf}')
                            return
    print(f'O aluno com código {cod} não foi encontrado!')

def buscarCurso(cod, busca=None):
    cod = int(cod)
    pos = arvore_cursos.buscar(cod)
    if pos is not None:
        with open('arquivos/cursos.txt', 'rt', encoding="utf-8") as arq:
            for i, linha in enumerate(arq):
                if i == pos:
                    campos = linha.strip().split(';')
                    cod_arq = int(campos[0])
                    descricao = campos[1]
                    if cod == cod_arq:
                        if busca == True:
                            return {'Curso': descricao}
                        else:
                            print(f'Código: {cod} | Descrição: {descricao}')
                            return
    print(f'O curso com código {cod} não foi encontrado!')

def buscarEmpres(cod):
    cod = int(cod)
    pos = arvore_emprestimos.buscar(cod)
    if pos is not None:
        with open('arquivos/emprestimos.txt', 'rt', encoding="utf-8") as arq:
            for i, linha in enumerate(arq):
                if i == pos:
                    campos = linha.strip().split(';')
                    cod_arq = int(campos[0])
                    cod_aluno = int(campos[2])
                    status = campos[5]
                    data_empr = datetime.strptime(campos[3], '%Y-%m-%d').date()
                    data_dev = datetime.strptime(campos[4], '%Y-%m-%d').date()
                    livro = buscarLivro(int(campos[1]), ignorar=True, busca=True)
                    aluno = buscarAluno(cod_aluno, busca=True)
                    if livro is None:
                        print('Livro não encontrado!')
                    if cod == cod_arq:
                        print(f'Código: {cod} | Título: {livro["Título do livro"]} | Nome do aluno: {aluno["Nome do aluno"]} | Cidade do aluno: {aluno["Cidade"]}/{aluno["UF"]} | Data de empréstimo: {data_empr} | Data de devolução: {data_dev} | Disponibilidade: {"Disponível" if status == "S" else "Emprestado"}')
                        return
    print(f'O empréstimo com código {cod} não foi encontrado!')


def devolverLivro(cod):
    emprestimos = []
    empr_encon = False
    with open('arquivos/emprestimos.txt', 'rt', encoding="utf-8") as arq_empr:
        for linha in arq_empr:
            campos = linha.strip().split(';')
            cod_arq = int(campos[0])
            data_dev = datetime.strptime(campos[4], '%Y-%m-%d').date()
            if cod == cod_arq:
                cod_livro = int(campos[1])
                func_util.verificarAtraso(data_dev)
                empr_encon = True
            emprestimos.append(linha.strip())
        if empr_encon:
            with open('arquivos/emprestimos.txt', 'wt', encoding="utf-8") as atualizado:
                for linha in emprestimos:
                    atualizado.write(linha + '\n')
        else:
           print('Empréstimo não encontrado!')
           return
    msg = func_util.atualizarDisp(cod_livro, 'S')
    print('Devolução realizada com sucesso! ' + msg)

#EXCLUSÃO
def deletarCidade():
    cod = func_util.validarInt('Código do registro a ser deletado: ')
    func_util.deletarDados('arquivos/cidades.txt', cod, arvore_cidades)

def deletarCurso():
    cod = func_util.validarInt('Código do registro a ser deletado: ')
    func_util.deletarDados('arquivos/cursos.txt', cod, arvore_cursos)

def deletarAluno():
    cod = func_util.validarInt('Código do registro a ser deletado: ')
    func_util.deletarDados('arquivos/alunos.txt', cod, arvore_alunos)

def deletarAutor():
    cod = func_util.validarInt('Código do registro a ser deletado: ')
    func_util.deletarDados('arquivos/autores.txt', cod, arvore_autores)

def deletarCateg():
    cod = func_util.validarInt('Código do registro a ser deletado: ')
    func_util.deletarDados('arquivos/categorias.txt', cod, arvore_categorias)

def deletarLivros():
    cod = func_util.validarInt('Código do registro a ser deletado: ')
    func_util.deletarDados('arquivos/livros.txt', cod, arvore_livros)

def deletarEmpres():
    cod = func_util.validarInt('Código do registro a ser deletado: ')
    func_util.deletarDados('arquivos/emprestimos.txt', cod, arvore_emprestimos)


def leituraCidade(linha, *args):
    campos = linha.strip().split(';')
    print(f'Código: {campos[0]} | Nome: {campos[1]} | UF: {campos[2]}')

def leituraCurso(linha, *args):
    campos = linha.strip().split(';')
    print(f'Código: {campos[0]} | Descrição: {campos[1]}') 

def leituraAluno(linha, *args):
    campos = linha.strip().split(';')
    curso = buscarCurso(int(campos[2]), busca=True)
    cid, uf = buscarCidade(int(campos[3]), busca=True)
    print(f'Código: {campos[0]} | Nome: {campos[1]} | Curso: {curso["Curso"]} | Cidade: {cid}/{uf}')

def leituraAutor(linha, *args):
    campos = linha.strip().split(';')
    cid, uf = buscarCidade(int(campos[2]), busca=True)
    print(f'Código: {campos[0]} | Nome: {campos[1]} | Cidade: {cid}/{uf}')

def leituraCateg(linha, *args):
    campos = linha.strip().split(';')
    print(f'Código: {campos[0]} | Descrição: {campos[1]}') 

def leituraLivros(linha, contadores=None, filtro=None, dataI=None, dataF=None):
    campos = linha.strip().split(';')
    autor = buscarAutor(int(campos[2]), busca=True)
    categ = buscarCateg(int(campos[3]), busca=True)
    status = campos[5]
    if filtro == 'emprestados' and status != 'N':
        return
    if filtro == 'disponiveis' and status != 'S':
        return
    print(f'Código: {campos[0]} | Título: {campos[1]} | Autor: {autor["Nome do autor"]} | Cidade do Autor: {autor["Cidade"]}/{autor["UF"]} | Categoria: {categ["Categoria"]} | Disponibilidade: {"Disponível" if status == "S" else "Emprestado"}')

    if contadores is not None:
        if status == 'S': 
            contadores['disponiveis'] += 1
        else:
            contadores['emprestados'] += 1
        if filtro == 'atrasados':
            contadores['atrasados'] += 1

def leituraEmpres(linha, contadores=None, filtro=None, dataI=None, dataF=None):
    campos = linha.strip().split(';')
    cod = int(campos[0])
    status = campos[5]
    data_empr = datetime.strptime(campos[3], '%Y-%m-%d').date()
    data_dev = datetime.strptime(campos[4], '%Y-%m-%d').date()
    hoje = date.today()
    if filtro == 'atrasados':
        if status == 'S' or hoje <= data_dev:
            return 
        buscarEmpres(cod)
        contadores['atrasados'] += 1
    elif filtro == 'periodo':
        if not (dataI <= data_empr <= dataF):
            return
        contadores['periodo'] += 1
        buscarEmpres(cod)
    else:
        buscarEmpres(cod)
    
    
def todos_livros():
    contadores = {'disponiveis': 0, 'emprestados': 0}
    arvore_livros.lerEmOrdem('arquivos/livros.txt', leituraLivros, contadores)
    print(f'Quantidade de livros disponíveis: {contadores["disponiveis"]}')
    print(f'Quantidade de livros emprestados: {contadores["emprestados"]}')

def livros_empres():
    contadores = {'emprestados': 0}
    arvore_livros.lerEmOrdem('arquivos/livros.txt', leituraLivros, contadores, filtro='emprestados')
    if contadores['emprestados'] == 0:
        print('Não há livros emprestados no momento!')
    
def livros_atrasados():
    contadores = {'atrasados': 0}
    arvore_emprestimos.lerEmOrdem('arquivos/emprestimos.txt', leituraEmpres, contadores, filtro = 'atrasados')
    if contadores['atrasados'] == 0:
        print('Não há livros atrasados no momento!')

def livros_periodo(dataI=None, dataF=None):
    contadores = {'periodo': 0}
    filtro = 'periodo'

    if dataI is None or dataF is None:
        print('Insira o período desejado para pesquisa')

        dataI = func_util.validarData('Data inicial (YYYY-MM-DD):')
        if dataI is None:
            return
        
        dataF = func_util.validarData('Data final (YYYY-MM-DD):')
        if dataF is None:
            return
    
    if dataF < dataI:
        print('A data final não pode ser menor que a data inicial!')
    arvore_emprestimos.lerEmOrdem('arquivos/emprestimos.txt', leituraEmpres, contadores, filtro, dataI, dataF)
    print(f'Quantidade de livros emprestados nesse período: {contadores["periodo"]}')
