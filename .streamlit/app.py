import streamlit as st
import func_principais
import func_util
import builtins, sys
from io import StringIO
 
def pegar_input(func, entrada=None, *args, **kwargs):
    saida = None
    entrada = entrada or []
    entrada = list(map(str, entrada))

    def simula_input(msg=''):
        if entrada:
            return entrada.pop(0)
        else:
            return None

    inputOriginal = builtins.input
    builtins.input = simula_input

    printOriginal = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        func(*args, **kwargs)
    except Exception as e:
        print('Erro:', e)

    builtins.input = inputOriginal
    sys.stdout = printOriginal
    saida = mystdout.getvalue()

    return saida

def pegar_saida(func, *args, **kwargs):
        printOriginal = sys.stdout
        sys.stdout = mystdout = StringIO()
        func(*args, **kwargs)
        sys.stdout = printOriginal
        return mystdout.getvalue()

st.set_page_config(
    page_title="Biblioteca",
    page_icon="📖",
    layout="wide"
)

st.title('Sistema de Gestão - Biblioteca')

if 'menu' not in st.session_state:
    st.session_state.menu = 'Cadastros'

st.sidebar.title('Menu principal')

def set_cadastros():
    st.session_state.menu = 'Cadastros'
def set_consultas():
    st.session_state.menu = 'Consultas'
def set_delete():
    st.session_state.menu = 'Exclusão'
def set_emprestimos():
    st.session_state.menu = 'Empréstimos/Devoluções'

st.sidebar.button('Cadastros', on_click=set_cadastros, type='tertiary')
st.sidebar.button('Consultas', on_click=set_consultas, type='tertiary')
st.sidebar.button('Exclusão', on_click=set_delete, type='tertiary')
st.sidebar.button('Empréstimos/Devoluções', on_click=set_emprestimos, type='tertiary')

menu = st.session_state.menu

#CADASTROS
if menu == 'Cadastros':
    st.subheader('Cadastros')
    opc = st.selectbox('Escolha o que deseja cadastrar:', ['Aluno', 'Autor', 'Categoria', 'Cidade', 'Curso', 'Livro'])

    if opc == 'Cidade':
        cod = st.number_input('Código', min_value=1)
        nome = st.text_input('Nome')
        uf = st.selectbox('UF', ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
                                 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                                 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'])
        if st.button('Cadastrar', type='primary'):
            saida = pegar_input(func_principais.add_cidades, [str(cod), nome, uf])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)
                
    elif opc == 'Curso':
        cod = st.number_input('Código', min_value=1)
        nome = st.text_input('Nome do curso')
        if st.button('Cadastrar', type='primary'):
            saida = pegar_input(func_principais.add_curso, [str(cod), nome])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    elif opc == 'Aluno':
        cod = st.number_input('Código', min_value=1)
        nome = st.text_input('Nome')
        cod_curso = st.number_input('Código do curso', min_value=1)
        cod_cid = st.number_input('Código da cidade', min_value=1)
        if st.button('Cadastrar', type='primary'):
            saida = pegar_input(func_principais.add_alunos, [str(cod), nome, str(cod_curso), str(cod_cid)])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    elif opc == 'Autor':
        cod = st.number_input('Código', min_value=1)
        nome = st.text_input('Nome')
        cod_cid = st.number_input('Código da cidade', min_value=1)
        if st.button('Cadastrar', type='primary'):
            saida = pegar_input(func_principais.add_autor, [str(cod), nome, str(cod_cid)])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    elif opc == 'Categoria':
        cod = st.number_input('Código', min_value=1)
        nome = st.text_input('Nome')
        if st.button('Cadastrar', type='primary'):
            saida = pegar_input(func_principais.add_categoria, [str(cod), nome])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    elif opc == 'Livro':
        cod = st.number_input('Código', min_value=1)
        titulo = st.text_input('Título')
        cod_autor = st.number_input('Código do autor', min_value=1)
        cod_categ = st.number_input('Código da categoria', min_value=1)
        ano = st.number_input('Ano de publicação', min_value=0)
        if st.button('Cadastrar', type='primary'):
            saida = pegar_input(func_principais.add_livros, [str(cod), titulo, str(cod_autor), str(cod_categ), str(ano)])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

elif menu == 'Consultas':
    st.subheader('Consultas')
    opc = st.selectbox('Escolha qual tabela consultar:', ['Alunos', 'Autores', 'Categorias', 'Cidades', 'Cursos', 'Empréstimos', 'Livros'])
    esc = st.toggle('Consultar por código')
    if opc == 'Livros' and esc == False:
        opc = st.selectbox('Escolha', ['Todos os livros',  'Livros atrasados',  'Livros emprestados', 'Livros por período'])

    if opc == 'Todos os livros' and st.button('Executar'):
        saida = pegar_saida(func_principais.todos_livros)
        linhas = [l for l in saida.split('\n') if l.strip() != '']
        if not linhas:
            st.info('Não há registros no momento!')
        else:
            st.write('Todos os livros')
            st.write('---')
            colunas = st.columns(6)
            cabecalhos = ['Código', 'Título', 'Autor', 'Cidade do Autor', 'Categoria', 'Disponibilidade']
            func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Livros emprestados' and st.button('Executar'):
        saida = pegar_saida(func_principais.livros_empres)
        if 'momento' in saida:
            st.info(saida)
        else:
            linhas = [l for l in saida.split('\n') if l.strip() != '']
            st.write('Livros Emprestados')
            st.write('---')
            colunas = st.columns(6)
            cabecalhos = ['Código', 'Título', 'Autor', 'Cidade do Autor', 'Categoria', 'Disponibilidade']
            func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Livros atrasados' and st.button('Executar'):
        saida = pegar_saida(func_principais.livros_atrasados)
        if 'momento' in saida:
            st.info(saida)
        else:
            linhas = [l for l in saida.split('\n') if l.strip() != '']
            st.write('Livros Atrasados')
            st.write('---')
            colunas = st.columns(6)
            cabecalhos = ['Código', 'Título', 'Autor', 'Cidade do Autor', 'Data de empréstimo', 'Data de devolução']
            func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Livros por período':
        dataI = st.date_input('Data inicial')
        dataF = st.date_input('Data final')
        if st.button('Consultar', type='primary'):
            saida = pegar_saida(func_principais.livros_periodo, dataI, dataF)
            linhas = [l for l in saida.split('\n') if l.strip() != '']
            if not linhas:
                st.info('Não há registros no momento!')
            else:
                st.write('Livros por período')
                st.write('---')
                colunas = st.columns(6)
                cabecalhos = ['Código', 'Título', 'Aluno', 'Cidade do aluno', 'Data de empréstimo', 'Data de devolução']
                func_util.tabela_front(colunas, cabecalhos, linhas)
    
    elif opc == 'Alunos':
        if esc == True:
            cod = st.number_input('Código do aluno:', min_value=1)
            if st.button('Consultar', type='primary'):
                saida = pegar_saida(func_principais.buscarAluno, cod, busca=False)
                if 'encontrado' in saida:
                    st.error(saida)
                else:
                    st.write(saida)
        else:
            saida = pegar_saida(func_principais.arvore_alunos.lerEmOrdem, 'arquivos/alunos.txt', func_principais.leituraAluno)
            linhas = [l for l in saida.split('\n') if l.strip() != '']
            if st.button('Consultar', type='primary'):
                if not linhas:
                    st.info('Não há registros no momento!')
                else:
                    st.write('Alunos cadastrados')
                    st.write('---')
                    colunas = st.columns(4)
                    cabecalhos = ['Código', 'Nome', 'Curso', 'Cidade']
                    func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Autores':
        if esc == True:
            cod = st.number_input('Código do autor:', min_value=1)
            if st.button('Consultar', type='primary'):
                saida = pegar_saida(func_principais.buscarAutor, cod, busca=False)
                if 'encontrado' in saida:
                    st.error(saida)
                else:
                    st.write(saida)
        else:
            saida = pegar_saida(func_principais.arvore_autores.lerEmOrdem, 'arquivos/autores.txt', func_principais.leituraAutor)
            linhas = [l for l in saida.split('\n') if l.strip() != '']
            if st.button('Consultar', type='primary'):
                if not linhas:
                    st.info('Não há registros no momento!')
                else:
                    st.write('Autores cadastrados')
                    st.write('---')
                    colunas = st.columns(3)
                    cabecalhos = ['Código', 'Nome', 'Cidade']
                    func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Categorias':
        if esc == True:
            cod = st.number_input('Código da categoria:', min_value=1)
            if st.button('Consultar', type='primary'):
                saida = pegar_saida(func_principais.buscarCateg, cod, busca=False)
                if 'encontrado' in saida:
                    st.error(saida)
                else:
                    st.write(saida)
        else:
            saida = pegar_saida(func_principais.arvore_categorias.lerEmOrdem, 'arquivos/categorias.txt', func_principais.leituraCateg)
            linhas = [l for l in saida.split('\n') if l.strip() != '']
            if st.button('Consultar', type='primary'):
                if not linhas:
                    st.info('Não há registros no momento!')
                else:
                    st.write('Categorias cadastradas')
                    st.write('---')
                    colunas = st.columns(4)
                    cabecalhos = ['Código', 'Descrição']
                    func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Cidades':
        if esc == True:
            cod = st.number_input('Código da cidade:', min_value=1)
            if st.button('Consultar', type='primary'):
                saida = pegar_saida(func_principais.buscarCidade, cod, busca=False)
                if 'encontrado' in saida:
                    st.error(saida)
                else:
                    st.write(saida)
        else:
            saida = pegar_saida(func_principais.arvore_cidades.lerEmOrdem, 'arquivos/cidades.txt', func_principais.leituraCidade)
            linhas = [l for l in saida.split('\n') if l.strip() != '']
            if st.button('Consultar', type='primary'):
                if not linhas:
                    st.info('Não há registros no momento!')
                else:
                    st.write('Cidades cadastradas')
                    st.write('---')
                    colunas = st.columns(3)
                    cabecalhos = ['Código', 'Descrição', 'Estado']
                    func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Cursos':
        if esc == True:
            cod = st.number_input('Código do curso:', min_value=1)
            if st.button('Consultar', type='primary'):
                saida = pegar_saida(func_principais.buscarCurso, cod, busca=False)
                if 'encontrado' in saida:
                    st.error(saida)
                else:
                    st.write(saida)
        else:
            saida = pegar_saida(func_principais.arvore_cursos.lerEmOrdem, 'arquivos/cursos.txt', func_principais.leituraCurso)
            linhas = [l for l in saida.split('\n') if l.strip() != '']
            if st.button('Consultar', type='primary'):
                if not linhas:
                    st.info('Não há registros no momento!')
                else:
                    st.write('Cursos cadastrados')
                    st.write('---')
                    colunas = st.columns(4)
                    cabecalhos = ['Código', 'Descrição']
                    func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Empréstimos':
        if esc == True:
            cod = st.number_input('Código do empréstimo:', min_value=1)
            if st.button('Consultar', type='primary'):
                saida = pegar_saida(func_principais.buscarEmpres, cod)
                if 'encontrado' in saida:
                    st.error(saida)
                else:
                    st.write(saida)
        else:
            if st.button('Consultar', type='primary'):
                saida = pegar_saida(func_principais.arvore_emprestimos.lerEmOrdem, 'arquivos/emprestimos.txt', func_principais.leituraEmpres)
                linhas = [l for l in saida.split('\n') if l.strip() != '']
                if not linhas:
                    st.info('Não há registros no momento!')
                else:
                    st.write('Empréstimos cadastrados')
                    st.write('---')
                    colunas = st.columns(7)
                    cabecalhos = ['Código', 'Título', 'Aluno', 'Cidade do aluno','Data de empréstimo','Data de devolução', 'Disponibilidade']
                    func_util.tabela_front(colunas, cabecalhos, linhas)

    elif opc == 'Livros':
        cod = st.number_input('Código do livro:', min_value=1)
        if st.button('Consultar', type='primary'):
            saida = pegar_saida(func_principais.buscarLivro, cod, busca=False)
            if 'não foi encontrado' in saida:
                st.error(saida)
            else:
                st.write(saida)

elif menu == 'Exclusão':
    st.subheader('Exclusão')
    opc = st.selectbox('Escolha de qual tabela deseja excluir:', ['Alunos', 'Autores', 'Categorias', 'Cidades', 'Cursos', 'Empréstimos','Livros'])

    if opc == 'Alunos':
        cod = st.number_input('Código do aluno: ', min_value=1)
        if st.button('Excluir', type='primary'):
            saida = pegar_input(func_principais.deletarAluno, [cod])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    if opc == 'Autores':
        cod = st.number_input('Código do autor:', min_value=1)
        if st.button('Excluir', type='primary'):
            saida = pegar_input(func_principais.deletarAutor, [cod])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    if opc == 'Categorias':
        cod = st.number_input('Código da categoria:', min_value=1)
        if st.button('Excluir', type='primary'):
            saida = pegar_input(func_principais.deletarCateg, [cod])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    if opc == 'Cidades':
        cod = st.number_input('Código da cidade:', min_value=1)
        if st.button('Excluir', type='primary'):
            saida = pegar_input(func_principais.deletarCidade, [cod])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    if opc == 'Cursos':
        cod = st.number_input('Código do curso:', min_value=1)
        if st.button('Excluir', type='primary'):
            saida = pegar_input(func_principais.deletarCurso, [cod])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    if opc == 'Empréstimos':
        cod = st.number_input('Código do empréstimo:', min_value=1)
        if st.button('Excluir', type='primary'):
            saida = pegar_input(func_principais.deletarEmpres, [cod])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    if opc == 'Livros':
        cod = st.number_input('Código do livro:', min_value=1)
        if st.button('Excluir', type='primary'):
            saida = pegar_input(func_principais.deletarLivros, [cod])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

elif menu == 'Empréstimos/Devoluções':
    st.subheader('Realizar Empréstimos/Devoluções')
    opc = st.selectbox('Escolha:', ['Realizar Empréstimo', 'Devolver Livro'])

    if opc == 'Realizar Empréstimo':
        cod = st.number_input('Código do empréstimo', min_value=1)
        cod_livro = st.number_input('Código do livro', min_value=1)
        cod_aluno = st.number_input('Código do aluno', min_value=1)
        if st.button('Realizar Empréstimo', type='primary'):
            saida = pegar_input(func_principais.add_emprestimos, [str(cod), str(cod_livro), str(cod_aluno)])
            if 'sucesso' in saida:
                st.success(saida)
            else:
                st.error(saida)

    elif opc == 'Devolver Livro':
        cod = st.number_input('Código do empréstimo', min_value=1)
        cod = int(cod)
        if st.button('Realizar devolução', type='primary'):
            saida = pegar_saida(func_principais.devolverLivro, cod)
            campos_saida = saida.split('!')
            if len(campos_saida) > 1:
                if 'atrasada' in campos_saida[0]:
                    st.info(campos_saida[0] + '!')
                    if 'sucesso' in campos_saida[1]:
                        st.success(campos_saida[1] + '!' + campos_saida[2] +'!')
                elif 'sucesso' in saida:
                    st.success(campos_saida[0] + '!')
                else:
                    st.error(campos_saida[0] +'!')
            