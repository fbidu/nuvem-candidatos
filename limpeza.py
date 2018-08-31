"""
A primeira parte do processamento.

Os arquivos PDF convertidos automaticamente possuem diversas linhas em branco.
Além disso, palavras muito curtas, preposições e pronomes não fazem sentido
ao montar uma nuvem de palavras.

Esse script passa por todos os arquivos de texto na pasta planos-de-governo e
executa diversos procedimentos de limpeza, dando origem aos arquivos 
nome_do_candidato_limpo.txt, que serão utilizados nas próximas etapas.
"""

import re  # Biblioteca de regex. Muito útil para lidar com textos
from os import listdir  # Função que lista o conteúdo de um diretório
from os.path import join  # Função que monta nomes de arquivo


# Constante que guarda o nome da pasta que contém os planos de governo
PLANOS_DE_GOVERNO = 'planos-de-governo'

def salva_lista(lista, caminho_do_arquivo, separador='\n'):
    """
    Esta função salva todo o conteúdo de uma lista em um novo arquivo
    e separa seus elementos usando o caracter definido em separador.
    Teoricamente é possível fazer simplesmente

    saída.write("\n".join(lista))

    Mas essa solução gasta bem mais memória que um loop simples.
    Como os arquivos podem ser bastante grandes, é bom evitar.
    """

    # Abre o arquivo para escrita
    saída = open(caminho_do_arquivo, 'w')

    # Percorre cada linha no arquivo
    for linha in lista:
        # Escreve o conteúdo de cada linha seguido do separador
        saída.write("{}{}".format(linha, separador))

    # Fecha o arquivo no final do processamento
    saída.close()

def remove_linhas_com_apenas_espaços(conteúdo_do_arquivo):
    """
    Esta função irá checar se uma linha é composta apenas
    por espaços e, caso positivo, as remove da saída.

    As diversas funções de limpeza desse script, substituem
    os caracteres indesejados por espaço. Essa função limpa
    as linhas que ficaram vazias.
    """

    resultado = []  # Lista vazia para guardar o resultado

    for linha in conteúdo_do_arquivo:  # Percorre todas as linhas do arquivo

        # Essa condicional retornará verdadeiro caso ainda restam caracteres
        # na linha depois que tods os espaços foram apagados.
        if re.sub(' ', '', linha):

            # Caso ainda exista alguma coisa, colocamos no resultado
            resultado.append(linha)

    # Por fim, retornamos o resultado
    return resultado

def remove_separadores_de_palavra(conteúdo_do_arquivo):
    """
    Esta função recebe todo o conteúdo do arquivo na forma de uma lista
    de strings - conforme retornado pela função readlines - e remove seus
    separadores de palavra. Nominalmente, remove os caracteres de quebra de
    linha, pontos, vírgulas, exclamações, interrogações e ponto-e-vírgula.
    Adicionalmente, ela remove linhas vazias do resultado.
    """

    resultado = []  # Cria uma lista vazia para armazenar o resultado

    for linha in conteúdo_do_arquivo:  # Percorre todas as linhas do arquivo

        # A próxima linha utliza da biblioteca regex para
        # trocar os caractes indesejáveis por espaço
        linha = re.sub(r'[\b\r\n\.\?\!\;]', ' ', linha)

        # Adiciona a linha processada ao resultado
        resultado.append(linha)

    return resultado

def remove_tudo_o_que_não_for_letra(conteúdo_do_arquivo):
    """
    Esta função irá trocar todos os números e símbolos por espaços vazios
    """

    resultado = []  # Cria uma lista vazia para o resultado

    for linha in conteúdo_do_arquivo:  # Percorre todo o arquivo

        # Utiliza da biblioteca regex para remover caracteres que 
        # não sejam de palavras.
        # \W - Regex para 'qualquer coisa que não seja letra, dígito ou _'
        # \d - Regex para 'qualquer dígito'
        linha = re.sub(r'[\W\d]', ' ', linha)

        # Adiciona a linha ao resultado
        resultado.append(linha)

    return resultado


def main():
    """
    A função principal que executará todas as rotinas de limpeza e salvará
    os resultados com o formato nome_do_candidato_limpo.txt
    """

    # Laço que percorre todos os arquivos na pasta planos-de-governo
    for arquivo in listdir('planos-de-governo'):

        # Estamos lidando com um arquivo com a extensão .txt e que
        # não seja um arquivo já limpo?
        if arquivo.endswith('.txt') and not arquivo.endswith('_limpo.txt'):

            limpo = []  # Lista vazia para receber o resultado da limpeza

            # Monta o nome do arquivo com base no nome da pasta dos planos
            nome_do_arquivo = join(PLANOS_DE_GOVERNO, arquivo)

            # Lê o conteúdo do arquivo
            conteúdo_do_arquivo = open(nome_do_arquivo, 'r').readlines()

            # Ao processar o PDF, muitas linhas com apenas espaços são geradas.
            # Limpar os espaços no início diminui o tamanho das listas a serem
            # processadas a seguir
            limpo = remove_linhas_com_apenas_espaços(conteúdo_do_arquivo)

            # Executa a remoção dos separadores de palavra
            limpo = remove_separadores_de_palavra(limpo)

            # Remove tudo o que não for letra
            limpo = remove_tudo_o_que_não_for_letra(limpo)
            
            # Remove as linhas que contém apenas espaços
            limpo = remove_linhas_com_apenas_espaços(limpo)

            # Monta o nome do arquivo de saída
            saída = arquivo[:-4] + '_limpo.txt'

            # Salva o resultado da limpeza
            salva_lista(limpo, join(PLANOS_DE_GOVERNO, saída))


if __name__ == "__main__":
    main()