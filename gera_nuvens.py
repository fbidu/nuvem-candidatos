"""
Esse script utiliza dos arquivos limpos gerados pelo
script "limpeza" para montar as nuvens de palavra
"""
from os import listdir
from os.path import join, dirname
from wordcloud import WordCloud, ImageColorGenerator

def main():
    """
    Função principal que gera todas as nuvens com base
    nos planos de governo limpos e salva em arquivos
    """

    # Obtém o caminho do diretório atual
    diretório_atual = dirname(__file__)

    # Obtém o caminho para o arquivo com a fonte
    # que será usada no texto das nuvens
    fonte = join(diretório_atual, "fonte", "NotoSerif-Regular.ttf")

    # Aqui nós criamos o objeto que irá gerar a nuvem de palavras,
    # definindo suas dimensões e quantas palavras queremos no máximo,
    # as cores que queremos usar e a fonte
    word_cloud = WordCloud(width=1080, height=720,
                           max_words=200, font_path=fonte,
                           collocations=False)

    # Percorre todos os arquivos em planos-de-governo
    for arquivo in listdir('planos-de-governo/'):

        # Só processaremos arquivos que foram limpos
        if arquivo.endswith('limpo.txt'):

            # O nome do presidenciável é o nome do arquivo
            # menos as 10 últimas letras
            presidenciável = arquivo[:-10]

            # Exibindo no console que estamos processando o plano atual
            print("Processando a nuvem de palavras para {}".format(presidenciável))

            # Pega todo o conteúdo do arquivo
            conteúdo = open(join('planos-de-governo', arquivo)).read()

            # Utilizamos o objeto de WordCloud para gerar a nuvem
            # e salvar em um arquivo
            word_cloud.generate(conteúdo).to_file('img/{}.png'.format(presidenciável))

if __name__ == "__main__":
    main()
