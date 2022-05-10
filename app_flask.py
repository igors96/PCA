from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods = ['POST'])
def upload():
    global nome_arquivo 
    file = request.files['excelfile']
    save_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(save_path)
    nome_arquivo = file.filename
    return render_template('index.html')

@app.route('/dist_pairplot', methods = ['GET', 'POST'])
def dist_pairplot():

    dirlist = os.listdir(".") 
    for i in dirlist:
        caminho = os.path.abspath(i)
    if "upload" in caminho:
        caminho_encontrado = caminho

    caminho_encontrado = caminho_encontrado.replace("\\","/")

    arquivo_upload = f'{caminho_encontrado}' + '/' + f'{secure_filename(nome_arquivo)}'

    arquivo = pd.read_excel(arquivo_upload)    

    # Dropando a primeira coluna do dataset
    arquivo = arquivo.iloc[:,1:]

    # Visualizando os dados originais
    sns.set(style="ticks", color_codes=True)
    grafico = sns.pairplot(arquivo, vars = list(arquivo.columns), diag_kind="hist")
    plt.show()
    return render_template('index.html')

@app.route('/dist_barplot', methods = ['GET', 'POST'])
def dist_barplot():

    dirlist = os.listdir(".") 
    for i in dirlist:
        caminho = os.path.abspath(i)
    if "upload" in caminho:
        caminho_encontrado = caminho

    caminho_encontrado = caminho_encontrado.replace("\\","/")

    arquivo_upload = f'{caminho_encontrado}' + '/' + f'{secure_filename(nome_arquivo)}'

    arquivo = pd.read_excel(arquivo_upload)    

    # Dropando a primeira coluna do dataset
    arquivo = arquivo.iloc[:,1:]

    # Visualizando os dados originais
    if request.method == 'POST':
        sns.set(style="ticks", color_codes=True)
        variavel = request.form['variavel']
        arquivo[variavel].value_counts().plot(kind = 'bar')
        plt.xlabel(f"{variavel}", size = 12)
        plt.ylabel("Frequência", size = 12)
        plt.show()
    return render_template('dist_barplot.html')

@app.route('/var_explicada', methods = ['GET','POST'])
def var_explicada():

    dirlist = os.listdir(".") 
    for i in dirlist:
        caminho = os.path.abspath(i)
    if "upload" in caminho:
        caminho_encontrado = caminho

    caminho_encontrado = caminho_encontrado.replace("\\","/")

    arquivo_upload = f'{caminho_encontrado}' + '/' + f'{secure_filename(nome_arquivo)}'

    arquivo = pd.read_excel(arquivo_upload) 

    # Dropando a primeira coluna do dataset
    arquivo = arquivo.iloc[:,1:]

    def media():

        conta_linhas = len(arquivo.index)
        media_colunas = []

        for coluna in arquivo:
            media_coluna = arquivo[coluna].sum()/conta_linhas
            media_colunas.append(media_coluna)

        return media_colunas
    
    medias = media()

    # Subtraindo as médias de cada coluna na coluna respectiva
    P = arquivo - medias

    # Matriz de covariância
    def produto_matrizes(A,B):
        
        linhas_A = len(A)
        colunas_B = len(B[0])
        matriz_zeros = [([0]*colunas_B) for i in range(linhas_A)]  
    
        for i in range(len(A)):
            for j in range(len(B[0])):        
                for k in range(len(B)):
                    matriz_zeros[i][j] += A[i][k] * B[k][j]
        
        matriz_resultante = matriz_zeros
        matriz_resultante = pd.DataFrame(matriz_resultante)

        return matriz_resultante

    # Funções para converter lista em dataframe e vice-versa
    def converte_lista_em_df(A):
        df = pd.DataFrame(A)
        return df

    def converte_df_em_lista(A):
        lista = A.values.tolist()
        return lista

    a = converte_df_em_lista(P.T)
    b = converte_df_em_lista(P)

    # Realizando produto da matriz P e sua transposta
    produto_p_p_transposta = produto_matrizes(a,b)

    # Calculando a parcela (1/n-1) do cálculo da matriz de covariância
    c = 1/(arquivo.shape[0]-1)

    # Obtendo a matriz covariância
    matriz_covariancia = c * produto_p_p_transposta

    # Obtenção dos autovalores e autovetores da matriz covariância
    autovalores, autovetores = np.linalg.eig(matriz_covariancia)

    # Ordenando os autovalores e autovetores em ordem decrescente e arredondando para 3 casas decimais
    index_ordenado = np.argsort(autovalores)[::-1]
    autovalores_ordenados = autovalores[index_ordenado]
    autovalores_ordenados = [np.round(valor, 3) for valor in autovalores_ordenados]
    autovetores_ordenados = autovetores[:, index_ordenado]
    autovetores_ordenados = [np.round(valor, 3) for valor in autovetores_ordenados]

    # Calculando a variância explicada e 100% da variância acumulada
    total_autovalores= sum(autovalores)
    variancia_explicada = [round(((i/total_autovalores)*100), 3) for i in autovalores_ordenados]

    variancia_explicada_acumulada = []
    soma = 0
    for valor in variancia_explicada:
        soma += valor
        variancia_explicada_acumulada.append(soma)

    # Calculando a variância acumulada para atingir 95% 
    variancia_explicada_acumulada_95 = []
    soma_95 = 0
    for valor in variancia_explicada:
        soma_95 += valor
        if soma_95 <= 95:
            variancia_explicada_acumulada_95.append(valor)

    # Número de componentes necessários para atingir 95% da variância acumulada
    n_componentes_95 = len(variancia_explicada_acumulada_95)
    componentes_95 = ['PC%s' %i for i in range(1,n_componentes_95+1)]

    # Visualizando os componentes principais em relação à 95% da variância explicada acumulada
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False
    plt.figure(figsize=(8, 8))
    plot3 = sns.barplot(x = componentes_95, y= variancia_explicada_acumulada_95, color = '#0f3655')
    for i in plot3.patches:
        plot3.annotate(i.get_height(), (i.get_x() + i.get_width()/2, i.get_height()), ha = 'center', va = 'baseline', fontsize = 10, color = 'black', xytext = (0,3), textcoords = 'offset points')
    plt.xlabel("Componentes principais", size = 12)
    plt.ylabel("Variância explicada (%)", size = 12)
    plt.show()
    return render_template('index.html')

@app.route('/explicacao_pca')
def explicacao_pca():
    return render_template('pca.html')

@app.route('/instrucoes')
def instrucoes():
    return render_template('instrucoes.html')

@app.route('/autor')
def autor():
    return render_template('autor.html')

if __name__ == '__main__':
    app.run(debug=True)