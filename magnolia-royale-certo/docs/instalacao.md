# Instalação e execução

## Windows: modo pronto para apresentação

Neste computador, execute `iniciar.cmd`. Na primeira preparação de outro computador, execute `preparar.cmd`. O preparador requer Python >=3.11 e internet. Ele baixa o Node.js v24.22.1 LTS portatil do site oficial, valida o SHA-256 e executa pnpm@11.19.0 com esse Node. Nao requer instalar Node ou pnpm globalmente, nem permissao de administrador para o Node. O Windows deve ser 64 bits.

As dependências ficam dentro do novo projeto. O gerenciador pnpm pode usar seu cache normal de pacotes. Não há instalação de um serviço MySQL do Windows. O download portátil é obtido do CDN oficial MySQL e verificado pelo script `scripts/download_mysql.py`.

## Usar um MySQL já instalado

Utilize MySQL 8.0 ou 8.4. Crie o banco principal com `utf8mb4` e uma conta com acesso a ele. Para rodar os testes, crie também `magnolia_royale_test` e dê acesso à conta de testes. Configure `backend/.env` a partir de `.env.example`; a senha no endereço de conexão deve ser codificada para URL se contiver caracteres especiais. Gere uma `SECRET_KEY` aleatória.

Na raiz do projeto, depois da configuração:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements-lock.txt
.\.venv\Scripts\python.exe -m backend.seed
.\.venv\Scripts\python.exe -m backend.app
```

No Linux/macOS, use `python3` para criar o ambiente e `.venv/bin/python` nos demais comandos. Instale o MySQL pelo método oficial do seu sistema. Os scripts portáteis `.cmd`/`.ps1` são específicos do Windows.

O seed cria tabelas inexistentes com `db.create_all()`. Se encontrar a conta administrativa dos exemplos, preserva os registros e não insere tudo novamente. Alterações futuras na estrutura de tabelas precisam de migração SQL; `create_all()` não altera tabelas existentes.

`database/schema.sql` contém o esquema equivalente para estudo ou criação manual em uma base vazia. Não é necessário executá-lo se usar o seed.

## Editar e recompilar o frontend

```powershell
cd frontend
& ..\.runtime\node-v24.22.1-win-x64\npx.cmd --yes pnpm@11.19.0 install --frozen-lockfile
& ..\.runtime\node-v24.22.1-win-x64\npm.cmd run build
```

Ou use `pnpm install --frozen-lockfile` e `pnpm build` se pnpm já estiver instalado. Vite é uma dependência do projeto; não precisa ser instalado globalmente.

Para desenvolvimento, mantenha a API em `http://127.0.0.1:5000` e execute `pnpm dev` na pasta frontend. Abra `http://127.0.0.1:5173`. O Vite encaminha `/api` para Flask. Configure `FRONTEND_URL=http://127.0.0.1:5173` no `.env` nesse modo para os links dos e-mails. Para a apresentação com as telas compiladas, use `FRONTEND_URL=http://127.0.0.1:5000`.

Use sempre o mesmo nome de host (`127.0.0.1`) para que o navegador mantenha a sessão. Reinicie a API depois de alterar Python ou `.env`; recompile e atualize a página depois de alterar as telas.

## Problemas comuns

- **A API não inicia:** confira `.env`, se MySQL está acessível e se as portas 5000/3307 estão livres. Logs do MySQL portátil ficam em `.runtime/mysql-process.log` e nos arquivos `.err` do diretório de dados.
- **Porta 3307 ocupada por outro programa:** não encerre o outro banco. Configure uma instância própria em outra porta e ajuste o `.env`, ou mude a porta da configuração portátil antes de iniciá-la.
- **Runtime do Visual C++ ausente:** MySQL para Windows pode exigir o Microsoft Visual C++ Redistributable x64 oficial. O ambiente validado já conseguiu executar o MySQL.
- **Confirmação de e-mail:** novos cadastros precisam abrir o link em `/demo-mailbox`. As contas prontas já estão verificadas.
- **Sem horário:** selecione um dia de funcionamento, um profissional vinculado ao procedimento e um horário futuro livre. Datas bloqueadas e reservas em aberto são consideradas.
- **Não pode avaliar:** precisa haver atendimento concluído da conta na clínica e, se escolhido, com aquele profissional. Há uma avaliação por cliente/clínica, editável no painel.
- **Sem relatório:** confira o período escolhido e o status concluído. Reserva pendente/confirmada/cancelada não entra na soma.

## E-mail e publicação

`DEMO_MODE=1` grava mensagens fictícias localmente. `DEMO_MODE=0` oculta a caixa e exige SMTP com STARTTLS, configurado pelas variáveis do exemplo. Envio SMTP e implantação pública não fizeram parte dos testes desta entrega. Para publicação, configure HTTPS, cookies seguros, credenciais próprias, tratamento operacional de uploads, backups e controles apropriados ao ambiente real.

## Preparador Node automatico

O script `scripts/ensure_node.ps1` usa Node.js 24.22.1 LTS em `.runtime/`, sem modificar o Node.js instalado no Windows. A verificacao usa a lista oficial `SHASUMS256.txt`. `scripts/prepare.ps1` antepoe o Node local ao `PATH` apenas durante a preparacao, executa `pnpm@11.19.0` pelo `npx.cmd` desse Node e compila o React pelo `npm.cmd` local.

Se a escola bloquear `nodejs.org` ou o registro do npm, sera preciso liberar esses enderecos ou realizar a preparacao numa maquina com acesso. Nao inclua `.runtime/`, `frontend/node_modules/` nem `.env` no GitHub.
