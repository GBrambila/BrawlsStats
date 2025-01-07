import requests
from bs4 import BeautifulSoup
import math  # Importa a biblioteca para logaritmos
import json
import os
import time

# =========================
# VARIÁVEIS GLOBAIS
# =========================

rankings_por_modo = {}
brawlers_potenciais = {}
brawlers_stats = {}
todos_brawlers_stats = {}
todos_brawlers_mapas = {}

todos_brawlers = {
    "Shelly", "Nita", "Colt", "Bull", "Brock", "Dynamike", "Bo", "El-Primo", "Barley",
    "Poco", "Rosa", "Rico", "Darryl", "Penny", "Carl", "Jacky", "8-BIT",
    "Tick", "Piper", "Pam", "Frank", "Bibi", "Bea", "Nani", "Edgar", "Griff",
    "Grom", "Bonnie", "Gus", "Buster", "Mandy", "Pearl", "Hank", "Maisie",
    "Mortis", "Tara", "Gene", "Max", "Mr-P", "Sprout", "Byron", "Squeak",
    "Buzz", "Fang", "Eve", "Janet", "Otis", "Gray", "Willow", "R-T",
    "Cordelius", "Doug", "Spike", "Crow", "Leon", "Sandy", "Amber", "Meg",
    "Chester", "Surge", "Colette", "Lola", "Belle", "Stu", "Ruffs", "Lou",
    "Emz", "Gale", "Chuck", "Charlie", "Mico", "Larry-and-Lawrie", "Kit",
    "Angelo", "Melodie", "Lily", "Draco", "Berry", "Clancy", "Moe", "Kenji",
    "Jessie"
}

meus_brawlers = {"Jessie", "Gus", "Bea", "Tick", "Byron", "Carl"}

modos_de_jogo = {
    "Gem Grab",
    "Brawl Ball",
    "Hot Zone",
    "Knockout",
    "Heist",
    "Bounty"
}

# Arquivos JSON
arquivo_json = "brawler_stats.json"
arquivo_mapas = "brawler_maps.json"

# =========================
# CONFIGURAÇÕES GLOBAIS
# =========================

COMPARAR_COM_QUAL_TOP = 3       # ex: 1 => top 1, 2 => top 2, 3 => top 3
TAMANHO_DO_TOP = 5             # quantos brawlers guardamos em cada modo
TOP_X_POTENCIAIS = 5           # quantos brawlers potenciais exibimos ao final
TOP_X_CADA_MODO = 5            # quantos exibimos para cada modo (meus brawlers)
TOP_X_TODOS_MODOS = 5          # quantos exibimos para cada modo (todos brawlers)
TOP_X_POR_MAPA = 5             # quantos exibimos por mapa
RANKING_MAPAS_APENAS_MEUS = True
COMPARAR_COM_QUAL_POSICAO_MAPA = 1

# Booleans
EXECUTAR_ANALISE_POTENCIAIS = True
EXECUTAR_EXIBIR_BRAWLER_DESEJADO = True
EXECUTAR_EXIBIR_TOP_CADA_MODO = True
EXECUTAR_EXIBIR_MELHORES_TODOS_MODOS = True
EXECUTAR_EXIBIR_TOP_POR_MAPA = True
EXECUTAR_TOP_GLOBAL_E_MEUS_MAPA = True

BRAWLER_DESEJADO = "Mandy"

EXECUTAR_POTENCIAIS_MAPAS = True
EXECUTAR_EXIBIR_MELHOR_DESEMPENHO_MAPAS = True
EXECUTAR_RANKING_MAPAS_COM_PARCEIRO_TOP = True

# =========================
# FUNÇÕES AUXILIARES
# =========================

def calcular_score(winrate, pickrate):
    try:
        wr = float(winrate.replace('%', ''))
        pr = float(pickrate.replace('%', ''))
        if pr <= 1.0:
            return 0.40 * wr - 6 * pr + 1.1 * (wr * pr)
        else:
            return 1.2956 * wr + 30 * math.log(pr) - 5.2688
    except ValueError:
        print(f"Valores inválidos para Winrate ({winrate}) ou Pickrate ({pickrate}). Usando score 0.")
        return 0.0

def precisa_atualizar(arquivo_alvo):
    if not os.path.exists(arquivo_alvo):
        return True
    ultima_modificacao = os.path.getmtime(arquivo_alvo)
    tempo_atual = time.time()
    diferenca = tempo_atual - ultima_modificacao
    return diferenca >= 7 * 24 * 60 * 60

def diferenca_log(valor_maior, valor_menor):
    try:
        dif_log = 100 * (math.log(valor_maior) - math.log(valor_menor))
        return round(dif_log, 2)
    except ValueError:
        print(f"Erro ao calcular diferença logarítmica entre {valor_maior} e {valor_menor}.")
        return 0.0

def analisar_brawler(nome, dado):
    for modo, dados_top in rankings_por_modo.items():
        if modo not in dado:
            continue
        score_brawler = float(dado[modo]['Score'])
        print(f"{modo}:")
        print(f"  {nome}: {score_brawler:.2f}")

        print("  Top Guardado:")
        for i, brawler_info in enumerate(dados_top, start=1):
            print(f"    {i}. {brawler_info['Brawler']}: {brawler_info['Score']:.2f}")
        print()


# =========================
# SCRAPING: BRAWLER (MODOS)
# =========================

def exibir_topX_cada_modo(n):
    """
    Exibe o top X dos SEUS brawlers em cada modo de jogo,
    com base no dicionário global 'brawlers_stats', que já contém
    apenas os brawlers do usuário (filtrados anteriormente).

    :param n: Quantos brawlers exibir em cada modo (definido pela configuração TOP_X_CADA_MODO).
    """
    print(f"\n=== Exibindo TOP {n} (SEUS brawlers) em cada modo ===")

    # Para cada modo de jogo, ordena seus brawlers pelo Score.
    for modo in modos_de_jogo:
        brawlers_neste_modo = []

        # Percorre todos os seus brawlers para ver se há dados desse modo.
        for brawler, dados_brawler in brawlers_stats.items():
            if modo in dados_brawler:
                score = float(dados_brawler[modo]["Score"])
                brawlers_neste_modo.append((brawler, score))

        # Ordena a lista em ordem decrescente (maior Score primeiro).
        brawlers_neste_modo.sort(key=lambda x: x[1], reverse=True)

        print(f"\nModo: {modo}")
        if not brawlers_neste_modo:
            print("  Nenhum dos seus brawlers tem dados para este modo.")
        else:
            # Exibe apenas até 'n' (TOP X)
            for i, (brawler, score) in enumerate(brawlers_neste_modo[:n], start=1):
                print(f"  {i}. {brawler} (Score: {score:.2f})")

    print("-" * 40)


def exibir_dados_brawler(nome_brawler):
    """
    Exibe informações de um brawler específico, tais como:
    - Winrate
    - Pickrate
    - Score (tanto o calculado quanto o exibido originalmente no site)
    - Para cada modo de jogo disponível.

    :param nome_brawler: Nome do Brawler que será exibido
    """
    # Verifica se o brawler existe em 'todos_brawlers_stats'.
    if nome_brawler not in todos_brawlers_stats:
        print(f"Brawler '{nome_brawler}' não encontrado em 'todos_brawlers_stats'.")
        return

    dados_brawler = todos_brawlers_stats[nome_brawler]
    print(f"\n=== Dados do Brawler: {nome_brawler} ===")
    if not dados_brawler:
        print("Não há dados disponíveis para este Brawler.")
        print("-" * 40)
        return

    # Percorre cada modo para exibir Winrate, Pickrate, Score, etc.
    for modo, info_modo in dados_brawler.items():
        score_calculado = info_modo.get("Score", 0.0)
        win_rate = info_modo.get("Winrate", "N/A")
        pick_rate = info_modo.get("Pickrate", "N/A")
        score_original_site = info_modo.get("ScoreO", "N/A")

        print(f"\nModo: {modo}")
        print(f"  Win Rate: {win_rate}")
        print(f"  Pick Rate: {pick_rate}")
        print(f"  Score (Original - Site): {score_original_site}")
        print(f"  Score (Calculado): {score_calculado:.2f}")

    print("-" * 40)


def exibir_topX_todos_brawlers_por_modo(n):
    """
    Exibe o top X de TODOS os brawlers para cada modo de jogo,
    baseando-se no dicionário 'todos_brawlers_stats'.

    :param n: Quantos brawlers exibir em cada modo (definido pela configuração TOP_X_TODOS_MODOS).
    """
    print(f"\n=== Exibindo TOP {n} (TODOS os brawlers) em cada modo ===")

    for modo in modos_de_jogo:
        lista_scores = []

        # Monta a lista de (brawler, score) para cada modo, considerando TODOS brawlers.
        for brawler, dados_brawler in todos_brawlers_stats.items():
            if modo in dados_brawler:
                score = float(dados_brawler[modo]["Score"])
                lista_scores.append((brawler, score))

        # Ordena em ordem decrescente (maior Score primeiro).
        lista_scores.sort(key=lambda x: x[1], reverse=True)

        print(f"\nModo: {modo}")
        if not lista_scores:
            print("  Nenhum brawler tem dados para este modo.")
        else:
            # Exibe apenas até 'n' (TOP X)
            for i, (brawler, score) in enumerate(lista_scores[:n], start=1):
                print(f"  {i}. {brawler} (Score: {score:.2f})")

    print("-" * 40)


# =========================
# SCRAPING: BRAWLER (MODOS)
# =========================

def obter_dados_brawler(nome_brawler):
    nome_formatado = nome_brawler.lower().replace(' ', '-')
    url = f"https://www.noff.gg/brawl-stars/brawler/{nome_formatado}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/112.0.0.0 Safari/537.36"
    }

    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site para {nome_brawler}: {e}")
        return {}

    try:
        soup = BeautifulSoup(resposta.content, 'lxml')
        brawler_stats_local = {}

        tabela = soup.find('table')
        corpo = tabela.find('tbody') if tabela else None

        if corpo:
            linhas = corpo.find_all('tr')
            for linha in linhas:
                celulas = linha.find_all('td')
                # Corrigir a lógica para refletir a ordem real das colunas no site:
                if len(celulas) >= 4:
                    modo = celulas[0].get_text(strip=True)
                    score_tabela = celulas[1].get_text(strip=True)  # Aqui antes estava como Winrate
                    winrate = celulas[2].get_text(strip=True)  # Aqui antes estava como Pickrate
                    pickrate = celulas[3].get_text(strip=True)  # Aqui antes estava como Score

                    brawler_stats_local[modo] = {
                        "Winrate": winrate,
                        "Pickrate": pickrate,
                        "ScoreO": score_tabela,  # Score vindo do site
                        "Score": calcular_score(winrate, pickrate)  # Score calculado
                    }

        return brawler_stats_local

    except Exception as e:
        print(f"Erro ao processar os modos para {nome_brawler}: {e}")
        return {}


# =========================
# SCRAPING: BRAWLER (MAPAS)
# =========================

def obter_dados_mapas_brawler(nome_brawler):
    nome_formatado = nome_brawler.lower().replace(' ', '-')
    url = f"https://www.noff.gg/brawl-stars/brawler/{nome_formatado}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "Chrome/112.0.0.0 Safari/537.36"
    }
    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site para {nome_brawler}: {e}")
        return {}

    try:
        soup = BeautifulSoup(resposta.content, 'lxml')
        tabela_mapas = soup.find('table', id='mapsTable')
        if not tabela_mapas:
            return {}

        corpo_mapas = tabela_mapas.find('tbody')
        if not corpo_mapas:
            return {}

        linhas = corpo_mapas.find_all('tr')
        mapas_data = {}
        for linha in linhas:
            celulas = linha.find_all('td')
            if len(celulas) >= 4:
                nome_mapa = celulas[0].get_text(strip=True)
                win_rate = celulas[1].get_text(strip=True)
                pick_rate = celulas[2].get_text(strip=True)
                score_site = celulas[3].get_text(strip=True)
                score_float = calcular_score(win_rate, pick_rate)
                mapas_data[nome_mapa] = {
                    "Winrate": win_rate,
                    "Pickrate": pick_rate,
                    "ScoreSite": score_site,
                    "ScoreCalc": score_float
                }
        return mapas_data
    except Exception as e:
        print(f"Erro ao processar os mapas para {nome_brawler}: {e}")
        return {}

# =========================
# EXIBIÇÃO DE MAPAS
# =========================

def exibir_topN_em_cada_mapa(n):
    mapas_dict = {}
    for brawler, mapas_brawler in todos_brawlers_mapas.items():
        if RANKING_MAPAS_APENAS_MEUS and brawler not in meus_brawlers:
            continue
        for nome_mapa, dados_mapa in mapas_brawler.items():
            score = dados_mapa["ScoreCalc"]
            if nome_mapa not in mapas_dict:
                mapas_dict[nome_mapa] = []
            mapas_dict[nome_mapa].append((brawler, score))

    print(f"\n=== Top {n} Brawlers em Cada Mapa (com base no ScoreCalc) ===")
    if RANKING_MAPAS_APENAS_MEUS:
        print("(Apenas os meus brawlers)\n")
    else:
        print("(Considerando todos os brawlers)\n")

    for nome_mapa, lista in mapas_dict.items():
        lista_ordenada = sorted(lista, key=lambda x: x[1], reverse=True)
        print(f"Mapa: {nome_mapa}")
        for i, (b, sc) in enumerate(lista_ordenada[:n], start=1):
            print(f"  {i}. {b}: {sc:.2f}")
        print("-" * 40)

def exibir_dados_mapa_especifico(nome_mapa, top_n=5):
    """
    Exibe os dados de um mapa específico, incluindo:
      - Top N global de brawlers no mapa
      - Seus próprios brawlers nesse mapa
    """
    print(f"\n=== Dados do Mapa: {nome_mapa} ===")
    # Descobrir se existe
    existe_mapa = False
    for brawler, mapas_info in todos_brawlers_mapas.items():
        if nome_mapa in mapas_info:
            existe_mapa = True
            break

    if not existe_mapa:
        print("Mapa não encontrado ou sem dados disponíveis.")
        print("-" * 40)
        return

    # Top N global
    lista_global = []
    for brawler, mapas_info in todos_brawlers_mapas.items():
        if nome_mapa in mapas_info:
            score = mapas_info[nome_mapa]["ScoreCalc"]
            lista_global.append((brawler, score))
    lista_global_sorted = sorted(lista_global, key=lambda x: x[1], reverse=True)

    print(f"\nTop {top_n} Brawlers Globais no Mapa:")
    for i, (b, sc) in enumerate(lista_global_sorted[:top_n], start=1):
        print(f"  {i}. {b}: {sc:.2f}")

    # Seus brawlers no mapa
    lista_meus = []
    for brawler in meus_brawlers:
        if brawler in todos_brawlers_mapas and nome_mapa in todos_brawlers_mapas[brawler]:
            sc = todos_brawlers_mapas[brawler][nome_mapa]["ScoreCalc"]
            lista_meus.append((brawler, sc))
    lista_meus_sorted = sorted(lista_meus, key=lambda x: x[1], reverse=True)

    print(f"\nSeus Brawlers no Mapa (Top {top_n}):")
    if not lista_meus_sorted:
        print("  Você não tem brawlers neste mapa.")
    else:
        for i, (b, sc) in enumerate(lista_meus_sorted[:top_n], start=1):
            print(f"  {i}. {b}: {sc:.2f}")

    print("-" * 40)

# =========================
# FUNÇÕES SOBRE POTENCIAIS E MODOS
# =========================

def calcular_potenciais_contra_topN(n):
    potenciais_n = {}
    for modo in modos_de_jogo:
        if modo not in rankings_por_modo or len(rankings_por_modo[modo]) < n:
            continue
        score_ref = rankings_por_modo[modo][n-1]["Score"]
        for b, dados_brawler in todos_brawlers_stats.items():
            if b in meus_brawlers:
                continue
            if modo in dados_brawler:
                if "Score" in dados_brawler[modo]:
                    score_externo = dados_brawler[modo]["Score"]
                    if score_externo > score_ref:
                        diff = diferenca_log(score_externo, score_ref)
                        if b in potenciais_n:
                            potenciais_n[b] += diff
                        else:
                            potenciais_n[b] = diff

    potenciais_n_sorted = sorted(potenciais_n.items(), key=lambda x: x[1], reverse=True)
    return potenciais_n_sorted

def exibir_topX_potenciais_n(n, top_x):
    potenciais = calcular_potenciais_contra_topN(n)
    topX = potenciais[:top_x]
    print(f"\n=== Top {top_x} Campeões (Comparando com o Top {n} dos MEUS brawlers em cada modo) ===")
    if not topX:
        print("Nenhum brawler potencial encontrado.")
    else:
        for i, (brawler, valor) in enumerate(topX, start=1):
            print(f"{i}. {brawler:<10} | Dif Log (Somada): {valor:.2f}")
    print("-" * 40)

# =========================
# FUNÇÃO POTENCIAIS EM MAPAS
# =========================

def encontrar_brawlers_potenciais_mapas(posicao=1):
    potenciais = {}
    mapas_dict_meus = {}
    for brawler, mapas_brawler in todos_brawlers_mapas.items():
        if brawler not in meus_brawlers:
            continue
        for nome_mapa, dados_mapa in mapas_brawler.items():
            score = dados_mapa["ScoreCalc"]
            if nome_mapa not in mapas_dict_meus:
                mapas_dict_meus[nome_mapa] = []
            mapas_dict_meus[nome_mapa].append((brawler, score))

    for nome_mapa, lista in mapas_dict_meus.items():
        lista.sort(key=lambda x: x[1], reverse=True)

    for nome_mapa, minha_lista_map in mapas_dict_meus.items():
        if len(minha_lista_map) < posicao:
            continue
        score_referencia = minha_lista_map[posicao - 1][1]

        for b, mapas_brawler in todos_brawlers_mapas.items():
            if b in meus_brawlers:
                continue
            if nome_mapa in mapas_brawler:
                score_novo = mapas_brawler[nome_mapa]["ScoreCalc"]
                if score_novo > score_referencia:
                    diff = diferenca_log(score_novo, score_referencia)
                    if b in potenciais:
                        potenciais[b] += diff
                    else:
                        potenciais[b] = diff

    potenciais_ordenados = sorted(potenciais.items(), key=lambda x: x[1], reverse=True)
    return potenciais_ordenados

# =========================
# NOVA FUNÇÃO
# =========================

def exibir_melhor_desempenho_mapas(posicao=3):
    """
    Exibe, para cada mapa, QUAL brawler externo tem a MAIOR diferença
    em relação ao brawler do usuário que ocupa 'posicao' (1=top1, 2=top2,...).
    Só considera brawlers que superem esse score de referência.
    """
    # ...
    # (Mantém o mesmo conteúdo que você já tinha na função)
    pass

def exibir_ranking_mapas_com_parceiro_top(brawlers_potenciais_lista, top_n=3):
    """
    Para cada mapa:
      1) Seleciona o primeiro brawler da lista 'brawlers_potenciais_lista' que possui dados para o mapa.
      2) Exibe esse brawler e seu ScoreCalc.
      3) Exibe o Top N dos meus brawlers no mapa, ordenados por ScoreCalc.
    """
    # 1) Construir estrutura de (brawler, scoreCalc) para cada mapa (global).
    mapas_global = {}
    for brawler, mapas_info in todos_brawlers_mapas.items():
        for nome_mapa, dados_map in mapas_info.items():
            score = dados_map["ScoreCalc"]
            if nome_mapa not in mapas_global:
                mapas_global[nome_mapa] = []
            mapas_global[nome_mapa].append((brawler, score))

    # 2) Construir estrutura somente dos meus brawlers
    mapas_meus = {}
    for brawler, mapas_info in todos_brawlers_mapas.items():
        if brawler not in meus_brawlers:
            continue
        for nome_mapa, dados_map in mapas_info.items():
            score = dados_map["ScoreCalc"]
            if nome_mapa not in mapas_meus:
                mapas_meus[nome_mapa] = []
            mapas_meus[nome_mapa].append((brawler, score))

    # 3) Para cada mapa, pegar o top1 global da lista 'brawlers_potenciais_lista' que tenha dados, e top N dos meus
    print(f"\n=== Top {top_n} dos meus Brawlers comparados com o Parceiro Top da Lista Potencial ===\n")

    for nome_mapa, lista_global in mapas_global.items():
        # Encontrar o primeiro brawler da lista 'brawlers_potenciais_lista' que tem dados pro mapa
        parceiro_top = None
        score_parceiro_top = 0.0
        for brawler_pot in brawlers_potenciais_lista:
            if brawler_pot in todos_brawlers_mapas and nome_mapa in todos_brawlers_mapas[brawler_pot]:
                parceiro_top = brawler_pot
                score_parceiro_top = todos_brawlers_mapas[brawler_pot][nome_mapa]["ScoreCalc"]
                break

        if not parceiro_top:
            parceiro_top = "Nenhum da lista potencial tem dados"
            score_parceiro_top = "N/A"

        # Ordenar meus brawlers
        lista_meus = mapas_meus.get(nome_mapa, [])
        lista_meus_sorted = sorted(lista_meus, key=lambda x: x[1], reverse=True)

        print(f"Mapa: {nome_mapa}")
        print(f"  Parceiro Top da Lista Potencial: {parceiro_top} (Score: {score_parceiro_top if isinstance(score_parceiro_top, str) else f'{score_parceiro_top:.2f}'})")

        if len(lista_meus_sorted) == 0:
            print("  Você não tem brawlers neste mapa.")
        else:
            print(f"  Seus brawlers (Top {top_n}):")
            for i, (my_b, my_score) in enumerate(lista_meus_sorted[:top_n], start=1):
                print(f"    {i}. {my_b} ({my_score:.2f})")

        print("-" * 40)


# =========================
# MAIN
# =========================

def main():
    global rankings_por_modo
    global brawlers_stats
    global todos_brawlers_stats
    global todos_brawlers_mapas

    # 1) Carrega ou atualiza brawlers (modos)
    if precisa_atualizar(arquivo_json):
        temp_bstats = {}
        for brawler in todos_brawlers:
            temp_bstats[brawler] = obter_dados_brawler(brawler)
        with open(arquivo_json, "w") as file:
            json.dump(temp_bstats, file, indent=4)
        todos_brawlers_stats = temp_bstats
    else:
        with open(arquivo_json, "r") as file:
            todos_brawlers_stats = json.load(file)

    # 2) Carrega ou atualiza brawlers (mapas)
    if precisa_atualizar(arquivo_mapas):
        temp_bmaps = {}
        for brawler in todos_brawlers:
            temp_bmaps[brawler] = obter_dados_mapas_brawler(brawler)
        with open(arquivo_mapas, "w") as file:
            json.dump(temp_bmaps, file, indent=4)
        todos_brawlers_mapas = temp_bmaps
    else:
        with open(arquivo_mapas, "r") as file:
            todos_brawlers_mapas = json.load(file)

    # 3) Montar brawlers_stats apenas com meus brawlers
    brawlers_stats.clear()
    for b, dados in todos_brawlers_stats.items():
        if b in meus_brawlers:
            brawlers_stats[b] = dados

    # 4) Montar ranking de cada modo => rankings_por_modo
    rankings_por_modo.clear()
    for modo in modos_de_jogo:
        dados_ordenados = sorted(
            [
                (b, stats_modo[modo]['Score'])
                for b, stats_modo in brawlers_stats.items()
                if modo in stats_modo
            ],
            key=lambda x: x[1],
            reverse=True
        )
        rankings_por_modo[modo] = [
            {"Brawler": b, "Score": score}
            for b, score in dados_ordenados[:TAMANHO_DO_TOP]
        ]

    # 5) Se quisermos analisar potenciais (modos)
    if EXECUTAR_ANALISE_POTENCIAIS:
        pot_mod = calcular_potenciais_contra_topN(COMPARAR_COM_QUAL_TOP)
        topX_mod = pot_mod[:TOP_X_POTENCIAIS]
        print(f"=== Análise de Potenciais (Comparando com Top {COMPARAR_COM_QUAL_TOP}) ===")
        if not topX_mod:
            print("Nenhum brawler potencial encontrado para este critério.")
        else:
            for i, (brawler, valor) in enumerate(topX_mod, start=1):
                print(f"{i}. {brawler:<10} | Dif Log: {valor:.2f}")
        print("-" * 40)

        if topX_mod:
            melhor_brawler = topX_mod[0]
            if melhor_brawler[0] in todos_brawlers_stats:
                print(f"\n=== Analisando Brawler Potencial: {melhor_brawler[0]} ===\n")
                analisar_brawler(melhor_brawler[0], todos_brawlers_stats[melhor_brawler[0]])

    # 6) Exibir top X (meus brawlers) em cada modo
    if EXECUTAR_EXIBIR_TOP_CADA_MODO:
        exibir_topX_cada_modo(TOP_X_CADA_MODO)

    # 7) Exibir dados de um brawler específico
    if EXECUTAR_EXIBIR_BRAWLER_DESEJADO:
        exibir_dados_brawler(BRAWLER_DESEJADO)

    # 8) Exibir top X de todos os brawlers em cada modo
    if EXECUTAR_EXIBIR_MELHORES_TODOS_MODOS:
        exibir_topX_todos_brawlers_por_modo(TOP_X_TODOS_MODOS)

    # 9) Exibir top N brawlers em cada mapa
    if EXECUTAR_EXIBIR_TOP_POR_MAPA:
        exibir_topN_em_cada_mapa(TOP_X_POR_MAPA)

    # 10) Encontrar brawlers potenciais que superem meu top <posicao> do mapa
    brawlers_potenciais_lista = []
    if EXECUTAR_POTENCIAIS_MAPAS:
        pot_map = encontrar_brawlers_potenciais_mapas(COMPARAR_COM_QUAL_POSICAO_MAPA)
        print(f"\n=== Brawlers que superam o meu top{COMPARAR_COM_QUAL_POSICAO_MAPA} em cada mapa (Somando diferenças) ===")
        if not pot_map:
            print("Nenhum brawler externo superou seus brawlers nos mapas.")
        else:
            for i, (b, soma) in enumerate(pot_map, start=1):
                print(f"{i}. {b:<10} | Dif Log (Somada): {soma:.2f}")
            # Aqui definimos brawlers_potenciais_lista automaticamente
            brawlers_potenciais_lista = [item[0] for item in pot_map]

        print("-" * 40)

    # 11) Exibir o melhor desempenho externo por mapa
    if EXECUTAR_EXIBIR_MELHOR_DESEMPENHO_MAPAS:
        # Se quiser usar a mesma lista de potenciais do top3 do Mapa, etc.
        # (Código da função poderia aproveitar brawlers_potenciais_lista, se desejado)
        pass  # Substitua com a chamada da sua função exibir_melhor_desempenho_mapas(posicao=COMPARAR_COM_QUAL_POSICAO_MAPA)

    # 12) Exibir o ranking de mapas com base na brawlers_potenciais_lista (se não estiver vazia)
    if EXECUTAR_RANKING_MAPAS_COM_PARCEIRO_TOP and brawlers_potenciais_lista:
        exibir_ranking_mapas_com_parceiro_top(brawlers_potenciais_lista, top_n=3)

    # 13) Exemplo de exibir dados de um mapa específico
    while True:
        escolha = input("\nDeseja exibir dados de um mapa específico? (s/n): ").strip().lower()
        if escolha == 's':
            mapa_escolhido = input("Digite o nome do mapa: ").strip()
            exibir_dados_mapa_especifico(mapa_escolhido, top_n=TOP_X_POR_MAPA)
        elif escolha == 'n':
            break
        else:
            print("Entrada inválida. Por favor, digite 's' ou 'n'.")

if __name__ == "__main__":
    main()
