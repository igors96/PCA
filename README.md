# PCA

O projeto PCA contém uma aplicação web utilizando HTML5 e CSS3 para confecção dos recursos de front-end e linguagem Python com a biblioteca Flask para criação do upload, recursos adicionais, tratamento dos dados, geração de gráficos e do acesso à URL da aplicação. Todos os códigos foram realizados no Visual Studio Code e para abertura da aplicação foi utilizado o browser Google Chrome.

O arquivo "app_flask.py" contém todo o passo a passo da construção do código para que permita ao usuário fazer o upload do arquivo, gerar um gráfico pairplot que mostra a relação entre as features do dataset, gerar outro gráfico barplot que o permite escolher qual feature específica deseja visualizar, e também um gráfico com os componentes principais em relação à variância explicada.

Nos arquivos deste repositório são encontrados arquivos estáticos, templates e um arquivo denominado "requirements.txt" que contém as versões das bibliotecas utilizadas. Para obtenção da aplicação, é necessário realizar o download de todos estes arquivos e inseri-los numa única pasta. Também, faz-se necessária a criação de 3 subpastas: static (que receberá todos os arquivos estáticos, a saber: o arquivo style.css e imagens), templates (que receberá todos os templates html) e upload (receberá o arquivo enviado pelo usuário na aplicação). Uma demonstração da disposição destes arquivos encontra-se na imagem a seguir:


![tela_pasta_sparta](https://user-images.githubusercontent.com/67437213/166157189-300ffd4e-4b69-4389-b4f6-cac813b90b8e.png)


Após, abra a pasta que contém as subpastas e arquivos em alguma IDE (recomenda-se o Visual Studio Code). Uma visualização de como ficaria esta tela está na imagem abaixo. O autor da aplicação escolheu o nome "Sparta" como pasta principal.

![visual studio](https://user-images.githubusercontent.com/67437213/166159937-9cc3889c-7331-4135-ac31-64156f0814d5.PNG)

Abra então o arquivo "app_flask.py" e clique em run. Foi deixada a porta padrão (5000), portanto a URL gerada após execução será
http://127.0.0.1:5000. Após, clique no botão que recarrega a página até que todos os recursos HTML e CSS possam ser visualizados. Todas as instruções posteriores de execução da aplicação encontram-se na aba "Instruções".
