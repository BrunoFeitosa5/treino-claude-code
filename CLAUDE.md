
# CLAUDE.md



## Sobre o projeto

Projeto de treino para aprender Claude Code. Sistema simples de lista de tarefas (todo list).



- **Stack:** Python + Flask (backend), HTML/CSS/JS (frontend)

- **Banco:** tarefas.json (local) e PostgreSQL Neon (produção)

- **Deploy:** Vercel

- **Idioma:** Sempre pt-BR — código, comentários e mensagens



## Comandos importantes

- `python app.py` — inicia o servidor Flask local (porta 5000)

- `pip install -r requirements.txt` — instala dependências



## Estrutura do projeto

- `app.py` — backend Flask, rotas da API

- `templates/` — frontend HTML

- `tarefas.json` — dados locais de tarefas

- `mcp-tarefas/` — MCP customizado (listar e adicionar tarefas)

- `vercel.json` — configuração de deploy



## Regras

- Nunca deletar `tarefas.json` diretamente

- Sempre testar localmente antes de fazer deploy

- Commits em português no formato: feat/fix/chore: descrição



## MCP disponível

- `mcp-tarefas` — ferramentas: `listar_tarefas` e `adicionar_tarefa`

