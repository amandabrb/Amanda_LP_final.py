# Biblioteca para trabalhar com expressões regulares.
# É utilizada para localizar, substituir ou validar padrões de texto.
# Neste código, serve para remover espaços repetidos após a limpeza do texto.
import re

# Biblioteca para manipulação de caracteres Unicode.
# Permite identificar a categoria de cada caractere, como letra, número ou símbolo.
# Foi utilizada para verificar se um caractere pertence ao conjunto de letras.
import unicodedata

# Counter é uma estrutura especializada para contagem de ocorrências.
# Funciona como um dicionário onde as chaves são os elementos
# e os valores representam quantas vezes cada elemento aparece.
from collections import Counter


# Foi utilizada para verificar a existência do arquivo Ubirajara
# e realizar sua leitura.
from pathlib import Path

# Biblioteca principal de Processamento de Linguagem Natural (PLN).
# Disponibiliza corpora, tokenizadores, stopwords e outras ferramentas
# úteis para análise linguística.
import nltk

# gutenberg:
# Corpus do NLTK contendo obras literárias do Projeto Gutenberg.
# Foi utilizado para obter os textos em inglês analisados no trabalho.
#
# machado:
# Corpus do NLTK contendo obras de Machado de Assis.
# Foi utilizado para acessar "Memórias Póstumas de Brás Cubas".
#
# stopwords:
# Conjunto de palavras muito frequentes em uma língua
# (artigos, preposições, pronomes etc.).
# Foi utilizado para remover palavras pouco informativas das análises.
from nltk.corpus import gutenberg, machado, stopwords

# Nota importante: este código é para análise de texto, e depende do arquivo ubirajara.txt estar presente no mesmo diretório para comparar com Memórias Póstumas. Se o arquivo não estiver presente, ele irá avisar e pular a comparação.
# Para esse código a IA foi utilizada para tirar dúvidas e utilizar bibliotecas do Python úteis para a análise.
# Além disso, a IA sugeriu criar funções para chamá-las no main. Essa forma me ajudou a consertar os erros que eu não achava no código anterior.
# Por fim, a parte de prints para a visualização dos resultados foi feita totalmente com a IA, o que deixou a saída dos resultados mais organizada e fácil de entender.

def garantir_nltk_corpus(nome: str):
    """Garante que o corpus NLTK esteja disponível. Se não existir, tenta fazer o download."""
    # Tenta encontrar o corpus na instalação local do NLTK.
    try:
        nltk.data.find(f'corpora/{nome}')
    except LookupError:
        # Se não está disponível, baixa o corpus.
        nltk.download(nome, quiet=True)


def limpar(texto: str) -> str:
    """Remove caracteres não alfabéticos e devolve o texto em minúsculas."""
    # Primeiro transformamos tudo para minúsculas.
    texto = texto.lower()
    letras = []
    # Percorre cada caractere no texto.
    for ch in texto:
    # Se o caractere for uma letra, adiciona à lista. ( unicodedata.category começa com 'L' para letras)
        if unicodedata.category(ch).startswith('L'):
            letras.append(ch)
    # Junta a lista de letras em uma única string.
    # Este é o valor devolvido pela função.
    return ''.join(letras)


def limpar_texto_para_palavras(texto: str) -> str:
    """Substitui caracteres não-letra por espaços, mantendo separação entre palavras."""
    texto = texto.lower()
    resultado = []
    # Para cada caractere, decidimos se mantemos o caractere ou usamos espaço.
    for ch in texto:
        if unicodedata.category(ch).startswith('L'):
            resultado.append(ch) # Adiciona a letra à lista.
        else:
            resultado.append(' ') # Substitui por espaço para manter a separação entre palavras.
    # Junta a lista em uma string completa.
    texto = ''.join(resultado)
    # Substitui vários espaços por um único espaço e remove espaços extras (Utilizei a Inteligência Artificial para fazer essa parte, ela importou a biblioteca re).
    texto = re.sub(r'\s+', ' ', texto).strip()
    # Retorna o texto limpo, pronto para separar em palavras.
    return texto


def ocorrencias(texto: str):
    """Cria um dicionário de ocorrências de letras e devolve a lista ordenada por frequência."""
    # Primeiro limpa o texto para ficar só com letras.
    texto_limpo = limpar(texto)
    contagem = {}
    # Conta cada letra do texto limpo.
    for letra in texto_limpo:
        if letra in contagem:
            contagem[letra] += 1
        else:
            contagem[letra] = 1
    # Cria uma lista de pares (letra, frequência) para ordenar.
    lista_ordenada = list(contagem.items())
    # Ordena a lista por frequência decrescente e, em empate, por letra. (Aqui também utilizei a Inteligência Artificial para fazer a ordenação, ela usou a função sort com uma chave personalizada do dicionário).
    lista_ordenada.sort(key=lambda item: (-item[1], item[0]))
    # Retorna o dicionário de contagem e a lista ordenada.
    return contagem, lista_ordenada


def contar_palavras(texto: str):
    """Conta as palavras de um texto e retorna um Counter com as frequências."""
    # Limpa o texto, substituindo tudo que não é letra por espaço.
    texto_limpo = limpar_texto_para_palavras(texto)
    # Separa o texto em palavras usando os espaços.
    palavras = texto_limpo.split()
    contagem = {}
    # Conta cada palavra encontrada.
    for palavra in palavras:
        if palavra in contagem:
            contagem[palavra] += 1
        else:
            contagem[palavra] = 1
    # Transforma o dicionário em Counter para facilitar o uso em outras partes. Counter é uma ferrmaenta do Python que facilita a contagem de palavras.
    return Counter(contagem)


def riqueza_lexical(contador_palavras: Counter) -> float: # Recebe um Counter com a contagem de palavras e devolve a riqueza lexical como um número decimal.
    """Calcula a riqueza lexical: tipos / total de tokens."""
    # total_palavras é o número de palavras no texto.
    total_palavras = sum(contador_palavras.values())
    # tipos é o número de palavras diferentes.
    tipos = len(contador_palavras)
    # Se não houver palavras, devolve 0.0 para evitar erro.
    if total_palavras == 0:
        return 0.0
    # Retorna a divisão: palavras diferentes dividido pelo total de palavras.
    return tipos / total_palavras


def hapax_legomena(contador_palavras: Counter):
    """Retorna a lista de palavras que ocorrem apenas uma vez no texto."""
    palavras = []
    # Vê cada palavra e sua frequência.
    for palavra, frequencia in contador_palavras.items():
        if frequencia == 1:
            palavras.append(palavra)
    # Ordena a lista de palavras únicas antes de devolver.
    return sorted(palavras)


def top_n(counter: Counter, n=20):
    """Retorna as n palavras ou letras mais frequentes."""
    # most_common já devolve os itens mais frequentes.
    return counter.most_common(n)


def bottom_n(counter: Counter, n=20):
    """Retorna as n palavras ou letras menos frequentes."""
    itens = list(counter.items())
    # Ordena pelo menor valor primeiro e, em caso de empate, pela letra ou palavra.
    itens.sort(key=lambda item: (item[1], item[0]))
    # Retorna apenas os primeiros n itens.
    return itens[:n]


def imprimir_top_20_palavras(contador: Counter, titulo: str):
    """Imprime as 20 palavras mais frequentes de um contador."""
    print(f'--- {titulo} ---')
    # Pega as 20 palavras ou letras mais frequentes.
    for palavra, frequencia in top_n(contador, n=20):
        print(f'{palavra}: {frequencia}')
    print()


def alfabeto_do_texto(texto: str):
    """Retorna o conjunto de letras usadas em um texto."""
    # Limpa o texto para obter só letras e então cria um conjunto.
    # O conjunto elimina letras repetidas.
    return set(limpar(texto))


def letras_unicas(alfabeto1: set, alfabeto2: set):
    """Retorna letras presentes em um alfabeto e não no outro."""
    # Subtrai o segundo conjunto do primeiro.
    letras = alfabeto1 - alfabeto2
    return sorted(letras)


def carregar_texto_arquivo(caminho: Path) -> str:
    """Lê o texto de um arquivo local e retorna o conteúdo."""
    # Lê todo o conteúdo do arquivo com codificação utf-8.
    # Ignora erros de leitura de caracteres estranhos.
    return caminho.read_text(encoding='utf-8', errors='ignore')


def imprimir_contagem_letras(nome: str, texto: str, n=10):
    """Calcula e imprime as letras mais frequentes de um texto."""
    # Chama ocorrencias para obter a lista ordenada de letras.
    _, lista_ordenada = ocorrencias(texto)
    print(f'--- {nome} ---')
    # Imprime as primeiras n letras da lista ordenada.
    for letra, frequencia in lista_ordenada[:n]:
        print(f'{letra}: {frequencia}')
    print()


def main():
    # Preparação: garante os corpora NLTK necessários.
    # Isso permite usar os livros do Gutenberg, Machado de Assis e stopwords.
    garantir_nltk_corpus('gutenberg')
    garantir_nltk_corpus('machado')
    garantir_nltk_corpus('stopwords')
    garantir_nltk_corpus('punkt_tab')

    # Exercício 1: contar letras de um texto simples
    print('1. Exercício 1: Contar letras no texto')
    texto_exemplo = 'Os alunos leram 23 livros no ano passado'
    # A função ocorrencias limpa o texto e conta as letras.
    contagem_exemplo, lista_exemplo = ocorrencias(texto_exemplo)
    print('   Texto usado:', texto_exemplo)
    print('   Letras encontradas e frequências:')
    for letra, frequencia in lista_exemplo:
        print(f'     {letra}: {frequencia}')
    print() # Isso aqui deixa um espaço entre os resultados.

    # Exercício 2: comparar dois livros em inglês do Gutenberg
    print('2. Exercício 2: Contagem de letras em dois livros do Gutenberg')
    textos_ingles = {
        'Emma (Jane Austen)': gutenberg.raw('austen-emma.txt'),
        'Moby Dick (Herman Melville)': gutenberg.raw('melville-moby_dick.txt'),
    }
    for numero, (titulo, texto) in enumerate(textos_ingles.items(), start=1):
        print(f'   2.{numero} Livro: {titulo}')
        # Para cada livro, mostra as letras mais frequentes.
        imprimir_contagem_letras(titulo, texto, n=10)
    print()

    # Exercício 3: comparar inglês e português
    print('3. Exercício 3: Comparar inglês e português')
    
    # Tenta carregar Machado, se não conseguir, usa um texto alternativo
    try:
        texto_machado = machado.raw('romance/marm05.txt')
    except:
        # Se falhar, usa arquivo local se disponível, caso contrário usa um texto em português
        caminho_machado = Path('Ubirajara.txt')
        if caminho_machado.exists():
            texto_machado = carregar_texto_arquivo(caminho_machado)
        else:
            print('   Aviso: Não foi possível carregar corpus Machado de Assis.')
            print('   Pulando Exercício 3 e continuando...')
            print()
            texto_machado = None
    
    texto_ingles = gutenberg.raw('austen-emma.txt')
    
    if texto_machado:
        alfabeto_ingles = alfabeto_do_texto(texto_ingles)
        alfabeto_portugues = alfabeto_do_texto(texto_machado)

        print(f'   3.1 Tamanho do alfabeto em inglês: {len(alfabeto_ingles)}')
        print(f'   3.2 Tamanho do alfabeto em português: {len(alfabeto_portugues)}')
        print(f'   3.3 Letras em inglês e não em português: {letras_unicas(alfabeto_ingles, alfabeto_portugues)}')
        print(f'   3.4 Letras em português e não em inglês: {letras_unicas(alfabeto_portugues, alfabeto_ingles)}')
        print('   3.5 Letras mais frequentes em inglês:')
        imprimir_contagem_letras('Inglês - Emma', texto_ingles, n=10)
        print('   3.6 Letras mais frequentes em português:')
        imprimir_contagem_letras('Português - Ubirajara/Machado', texto_machado, n=10)
        print('   3.7 Letras menos frequentes em inglês:')
        contador_ingles = Counter(limpar(texto_ingles))
        for letra, frequencia in bottom_n(contador_ingles, n=10):
            print(f'     {letra}: {frequencia}')
        print('   3.8 Letras menos frequentes em português:')
        contador_portugues = Counter(limpar(texto_machado))
        for letra, frequencia in bottom_n(contador_portugues, n=10):
            print(f'     {letra}: {frequencia}')
        print()

        # Exercício 4: análise de Memórias Póstumas de Brás Cubas
        print('4. Exercício 4: Análise do Texto em Português')
        numero_caracteres = len(texto_machado)
        contador_palavras_machado = contar_palavras(texto_machado)
        riqueza = riqueza_lexical(contador_palavras_machado)

        print(f'   4.1 Número de caracteres: {numero_caracteres}')
        print(f'   4.2 Número total de palavras: {sum(contador_palavras_machado.values())}')
        print(f'   4.3 Número de tipos de palavras: {len(contador_palavras_machado)}')
        print(f'   4.4 Riqueza lexical: {riqueza:.4f}')
        print()
    else:
        contador_palavras_machado = None
        print()

    # Exercícios 5 e 6: comparação com Ubirajara, se o arquivo existir
    caminho_ubirajara = Path('ubirajara.txt')
    if caminho_ubirajara.exists() and contador_palavras_machado is not None:
        print('5. Exercício 5: Comparar palavras com Ubirajara')
        texto_ubirajara = carregar_texto_arquivo(caminho_ubirajara)
        contador_ubirajara = contar_palavras(texto_ubirajara)

        imprimir_top_20_palavras(contador_palavras_machado, 'Top 20 Memórias Póstumas')
        imprimir_top_20_palavras(contador_ubirajara, 'Top 20 Ubirajara')

        stopwords_portugues = set(stopwords.words('portuguese'))
        # Remove palavras comuns de parada para ver apenas palavras mais informativas.
        palavras_sem_stop_machado = [p for p, _ in top_n(contador_palavras_machado, n=100) if p not in stopwords_portugues]
        palavras_sem_stop_ubirajara = [p for p, _ in top_n(contador_ubirajara, n=100) if p not in stopwords_portugues]

        print('   5.1 Palavras mais frequentes sem stopwords em Memórias Póstumas:')
        print('     ', palavras_sem_stop_machado[:20])
        print('   5.2 Palavras mais frequentes sem stopwords em Ubirajara:')
        print('     ', palavras_sem_stop_ubirajara[:20])
        print()

        print('6. Exercício 6: Hápax legômena nos dois textos')
        hapaxes_machado = hapax_legomena(contador_palavras_machado)
        hapaxes_ubirajara = hapax_legomena(contador_ubirajara)
        comuns = sorted(set(hapaxes_machado) & set(hapaxes_ubirajara))

        print(f'   6.1 Hápax em Memórias Póstumas: {len(hapaxes_machado)}')
        print(f'   6.2 Hápax em Ubirajara: {len(hapaxes_ubirajara)}')
        print(f'   6.3 Hápax comuns entre os dois: {len(comuns)}')
        print('     ', comuns[:50])
        print()
    else: # Tive muitos problemas para baixar o arquivo de Ubirajara, então deixei essa mensagem para quem for testar o código. (A mensagem me ajudou bastante)
        print('5. Exercício 5 e 6: arquivo Ubirajara não encontrado')
        print('   Copie o arquivo ubirajara.txt para o diretório para executar as comparações.')
        print()



if __name__ == '__main__':
    main()

# Os comentários abaixo são os mesmos do topo do código. Escrevo aqui para ter certeza que sejam vistos!
# Nota importante: este script é para análise de texto, e depende do arquivo ubirajara.txt estar presente no mesmo diretório para comparar com Memórias Póstumas. Se o arquivo não estiver presente, ele irá avisar e pular a comparação.
# Para esse código a IA foi utilizada para tirar dúvidas e utilizar bibliotecas do Python úteis para a análise.
# Além disso, a IA sugeriu criar funções para chamá-las no main. Essa forma me ajudou a consertar os erros que eu não achava no código anterior.
# Por fim, a parte de prints para a visualização dos resultados foi feita totalmente com a IA, o que deixou a saída dos resultados mais organizada e fácil de entender.
