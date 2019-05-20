# iMiner

Projeto desenvolvido para a disciplina de Inteligência Artificial (INE5430).

### Requisitos
- Python 3.7
- Poetry 0.12

### Configuração
Para instalar as dependências, utilize:
`poetry install`

### Execução
Primeiramente acesse o ambiente de desenvolvimento:
`poetry shell`

Para rodar o programa com um agente específico, em um dado mapa, execute:

```python3 miner/app.py ./tests/example.map LDS 10```

Onde example.map é o arquivo contendo a configuração do mapa, LDS é o algoritmo utilizado pelo agente, e 10 é o limite do algoritmo (quando necessário).

Algoritmos implementados:
- LDS: Limited Depth Search
- BFS: Breath First Search
- Astar: A* com heurística Distância de Manhattan
- ImprovedAstar: A* com heurística e estratégia melhorada

