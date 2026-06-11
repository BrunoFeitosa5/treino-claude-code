---
name: rodar
description: Use when o usuário pede para rodar, iniciar ou subir o servidor Flask do projeto de todo list.
---

# Rodar

Inicia o servidor Flask do projeto e confirma que está no ar.

## Passos

Execute em sequência:

1. **Verificar Flask** — cheque se o Flask está instalado:
   ```powershell
   python -c "import flask"
   ```
   Se falhar, instale com `pip install flask` antes de continuar.

2. **Encerrar instância anterior** (se houver) — mate qualquer processo Python já rodando na porta 5000 para evitar conflito:
   ```powershell
   $proc = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
   if ($proc) { Stop-Process -Id $proc -Force }
   ```

3. **Iniciar o servidor** — suba `app.py` em background redirecionando os logs:
   ```powershell
   Start-Process -NoNewWindow -FilePath "python" `
     -ArgumentList "C:\Users\Bruno\Documents\treino-claude-code\app.py" `
     -RedirectStandardOutput "C:\Users\Bruno\Documents\treino-claude-code\flask.log" `
     -RedirectStandardError  "C:\Users\Bruno\Documents\treino-claude-code\flask.err"
   Start-Sleep -Seconds 2
   ```

4. **Confirmar que está no ar** — faça uma requisição de teste:
   ```powershell
   (Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -UseBasicParsing).StatusCode
   ```
   - Se retornar `200`: informe que o servidor está rodando e diga ao usuário para abrir **http://localhost:5000**.
   - Se falhar: leia `flask.err` e mostre o erro para o usuário.
