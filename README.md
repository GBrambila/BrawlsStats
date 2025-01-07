## Analisador de Brawlers e Mapas no Brawl Stars
**Brawlers Stats** é script em Python permite analisar e classificar os **brawlers** do jogo [Brawl Stars](https://brawlstars.com/) com base em estatísticas obtidas através de scraping de dados do noff.gg.

## Funcionalidades

- **Scraping de Dados**: Coleta estatísticas de brawlers e mapas.
- **Cálculo de Scores**: Aplica fórmulas matemáticas para determinar a eficácia de cada brawler em diferentes modos e mapas.
- **Rankings Personalizados**: Gera rankings baseados nas preferências do usuário, incluindo top brawlers em modos específicos e mapas.
- **Análise de Potenciais**: Identifica brawlers potenciais que podem superar os atuais favoritos do jogador.
- **Interação com o Usuário**: Permite ao usuário visualizar dados de mapas específicos conforme sua necessidade.

## Configuração

O script possui várias configurações globais que podem ser ajustadas conforme as preferências do usuário. Estas configurações estão definidas na seção **CONFIGURAÇÕES GLOBAIS** do código.

### Variáveis Globais

- **Brawlers**:
  - `todos_brawlers`: Conjunto contendo todos os nomes dos brawlers disponíveis.
  - `meus_brawlers`: Conjunto contendo os brawlers preferidos do usuário.

- **Modos de Jogo**:
  - `modos_de_jogo`: Conjunto dos diferentes modos de jogo disponíveis (e.g., Gem Grab, Brawl Ball).

- **Arquivos JSON**:
  - `arquivo_json`: Nome do arquivo para armazenar estatísticas dos brawlers.
  - `arquivo_mapas`: Nome do arquivo para armazenar estatísticas dos mapas.

### Configurações Globais

- **Comparação e Rankings**:
  - `COMPARAR_COM_QUAL_TOP`: Define com qual posição no top será feita a comparação (1 => top 1, 2 => top 2, etc.).
  - `TAMANHO_DO_TOP`: Número de brawlers armazenados em cada modo.
  - `TOP_X_POTENCIAIS`: Quantidade de brawlers potenciais a serem exibidos no final.
  - `TOP_X_CADA_MODO`: Quantidade de brawlers exibidos para cada modo (meus brawlers).
  - `TOP_X_TODOS_MODOS`: Quantidade de brawlers exibidos para cada modo (todos os brawlers).
  - `TOP_X_POR_MAPA`: Quantidade de brawlers exibidos por mapa.

- **Opções Booleanas**:
  - `EXECUTAR_ANALISE_POTENCIAIS`: Ativa a análise de brawlers potenciais.
  - `EXECUTAR_EXIBIR_BRAWLER_DESEJADO`: Exibe dados de um brawler específico.
  - `EXECUTAR_EXIBIR_TOP_CADA_MODO`: Exibe o top X de meus brawlers em cada modo.
  - `EXECUTAR_EXIBIR_MELHORES_TODOS_MODOS`: Exibe o top X de todos os brawlers em cada modo.
  - `EXECUTAR_EXIBIR_TOP_POR_MAPA`: Exibe o top X de brawlers em cada mapa.
  - `EXECUTAR_TOP_GLOBAL_E_MEUS_MAPA`: Exibe rankings globais e pessoais por mapa.
  - `EXECUTAR_POTENCIAIS_MAPAS`: Ativa a busca por brawlers potenciais que superem os atuais nos mapas.
  - `EXECUTAR_EXIBIR_MELHOR_DESEMPENHO_MAPAS`: Exibe o melhor desempenho externo por mapa.
  - `EXECUTAR_RANKING_MAPAS_COM_PARCEIRO_TOP`: Exibe o ranking de mapas com base na lista de brawlers potenciais.

- **Outras Configurações**:
  - `BRAWLER_DESEJADO`: Nome do brawler específico que o usuário deseja analisar.
  - `COMPARAR_COM_QUAL_POSICAO_MAPA`: Define a posição no ranking do mapa para comparação.

## Funcionamento do Sistema de Score

### Resumo da Ideia por Trás do Score

O **objetivo principal** do sistema de **score** é **avaliar e comparar brawlers** em diferentes modos de jogo, ajudando a identificar **lacunas** na sua **pool de campeões** e **oportunidades estratégicas** para reforçar fraquezas.

---

### 1. Objetivos do Sistema de Score

1. **Avaliar Viabilidade Competitiva**  
   - Medir a **eficiência** de cada brawler em diferentes modos de jogo com base em **Win Rate (WR)** e **Pick Rate (PR)**.

2. **Identificar Deficiências**  
   - Comparar os scores de brawlers disponíveis com os brawlers que você **não possui** para ver onde há **potencial de melhoria**.

3. **Evitar Supervalorização de Diferenças Extremas**  
   - Reduzir o impacto de **diferenças exageradas** em modos onde você já tem brawlers fortes, priorizando modos onde sua **pool é fraca**.

4. **Fornecer Comparações Flexíveis e Inteligentes**  
   - Valorizar diferenças pequenas em brawlers com scores mais baixos, enquanto **achatando** diferenças grandes em brawlers com scores altos, refletindo que melhorias em níveis mais baixos são mais significativas.

---

### 2. Fórmula Base do Score

O sistema de score é baseado em **Win Rate (WR)** e **Pick Rate (PR)**. Foi criada uma fórmula segmentada para lidar com **PR baixos e altos** de forma diferenciada:

- PR ≤ 1% (Pouco Usados):
Usamos um modelo linear + interação para premiar brawlers raros com desempenho alto:
Score = 0.40 * WR - 6 * PR + 1.1 * (WR * PR)

- PR > 1% (Popular):
Usamos um modelo logarítmico para evitar explosões em brawlers muito populares e valorizar o WinRate:
Score = 1.2956 * WR + 30 * ln(PR) - 5.2688

**Resultado esperado:**  
- Campeões pouco usados, mas eficientes, recebem **reconhecimento** sem inflar valores.
- Campeões populares têm **crescimento desacelerado** no score para evitar que dominem a lista por PickRate.

---

### 3. Comparação entre Brawlers

Ao comparar os brawlers disponíveis com os que você **não possui**, o foco é:

1. **Analisar Diferenças de Score**  
   - Ver onde novos brawlers podem **preencher lacunas**.

2. **Evitar Impacto Excessivo de Diferenças Grandes**  
   - Por exemplo, se você já possui um brawler com score **110**, um brawler com score **180** no mesmo modo **não deve pesar muito** se outros modos estão carentes.

3. **Valorizar Melhorias em Bases Menores**  
   - Diferenças em scores mais baixos (ex.: 110 → 130) devem ser mais relevantes do que em scores altos (ex.: 130 → 150).

---

### 4. Ajustes para Diferenças

Para que diferenças muito grandes **não dominem as decisões**, foram aplicadas funções de **ajuste de diferença** (achatamento):

#### 4.1. Logarítmica (Redução Suave):  
Achata valores altos e dá **mais peso** a diferenças menores:  
Δ_ef = a * ln(Δ + 1)

#### 4.2. Relativa (Proporcional ao Score Base):  
Valoriza mais os ganhos em scores **menores** do que em scores **altos**:  
Δ_rel = Diferença Real / Score Antigo

#### 4.3. Logaritmo na Razão:  
Usa o logaritmo das razões dos scores, tornando a diferença proporcional:  
Δ_log = ln(Score Novo / Score Atual)

Esses métodos garantem que:
- **Grandes diferenças** sejam achatadas.
- **Diferenças pequenas** continuem sendo relevantes.
- Brawlers com **scores mais baixos** tenham suas melhorias valorizadas.

---

### 5. Aplicações Práticas do Sistema

1. **Análise de Modos de Jogo:**  
   - Avaliar se vale mais a pena reforçar um modo **carente** ou melhorar ainda mais um modo onde você já está forte.

2. **Sugestão de Prioridades:**  
   - Recomendar brawlers para serem desbloqueados ou melhorados com base no **maior impacto estratégico**.

3. **Flexibilidade para Ajustes:**  
   - As fórmulas permitem ajustes de coeficientes (\(a, b, k\)) para adaptar o sistema a **novos dados** ou **preferências pessoais**.

4. **Acompanhamento Contínuo:**  
   - Atualizar a avaliação conforme o meta do jogo muda ou novos brawlers são adicionados.

---

### 6. Conclusão

Este sistema de **score** e comparação foi projetado para ser **robusto**, **flexível** e **estrategicamente relevante**, permitindo:

1. **Identificar Pontos Fracos:** Avaliar modos onde sua pool é deficiente.
2. **Evitar Saturação em Modos Fortes:** Reduzir a influência de brawlers fora da curva.
3. **Valorizar Melhorias Significativas:** Reconhecer acréscimos menores em bases baixas como mais impactantes.
4. **Ser Facilmente Ajustável:** Adaptar fórmulas e escalas conforme o jogo evolui.

Combinando essas ideias, o sistema oferece uma abordagem **inteligente** e **balanceada** para analisar **brawlers**, focando em cobrir **lacunas estratégicas** em vez de supervalorizar opções já dominantes.

---

### Personalização

Para personalizar o script de acordo com suas preferências:

1. **Edite a lista de brawlers favoritos**:

    ```python
    meus_brawlers = {"Jessie", "Gus", "Bea", "Tick", "Byron", "Carl"}
    ```

2. **Ajuste as configurações globais conforme necessário**:

    ```python
    COMPARAR_COM_QUAL_TOP = 3
    TAMANHO_DO_TOP = 5
    # ... e assim por diante
    ```



**Passos de Execução**:

1. **Atualização de Dados**: O script verifica se os arquivos JSON estão atualizados (última modificação há mais de 7 dias). Se necessário, realiza scraping para atualizar os dados.

2. **Geração de Rankings**: Baseado nas configurações, o script gera rankings de brawlers por modo e por mapa.

3. **Análises Adicionais**: Dependendo das opções ativadas, o script pode realizar análises de potenciais brawlers, exibir dados específicos de brawlers ou mapas, entre outras funcionalidades.

4. **Interação com o Usuário**: Após as análises iniciais, o script permite ao usuário visualizar dados de mapas específicos conforme desejado.

**Exemplo de Saída**:

```plaintext
=== Top 5 Brawlers em Cada Mapa (com base no ScoreCalc) ===
(Apenas os meus brawlers)

Mapa: Gem Mine
  1. Jessie: 85.50
  2. Tick: 80.30
  3. Carl: 75.20
  4. Gus: 70.10
  5. Byron: 65.00
----------------------------------------
```

## Estrutura do Código

O código está organizado em várias seções principais:

1. **Importações**: Bibliotecas necessárias para execução (requests, BeautifulSoup, etc.).
2. **Variáveis Globais**: Definição de conjuntos e dicionários para armazenar dados de brawlers e mapas.
3. **Configurações Globais**: Parâmetros ajustáveis que controlam o comportamento do script.
4. **Funções Auxiliares**: Funções de suporte para cálculos e verificações.
5. **Scraping de Dados**:
    - `obter_dados_brawler`: Coleta estatísticas de modos de jogo para um brawler específico.
    - `obter_dados_mapas_brawler`: Coleta estatísticas de mapas para um brawler específico.
6. **Exibição de Dados**:
    - Funções para exibir rankings, dados de mapas específicos, análises de potenciais, etc.
7. **Funções sobre Potenciais e Modos**: Cálculo e exibição de brawlers potenciais que podem melhorar os rankings atuais.
8. **Main**: Função principal que orquestra a execução do script, chamando as funções apropriadas conforme as configurações.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

