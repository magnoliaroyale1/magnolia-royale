# Magnolia Royale

**Plataforma web de descoberta e gestão de clínicas estéticas**

O **Magnolia Royale** é uma aplicação web que aproxima pessoas interessadas em procedimentos estéticos de clínicas cadastradas na plataforma. Os clientes podem pesquisar estabelecimentos, receber recomendações com base em suas preferências e solicitar agendamentos. As clínicas contam com ferramentas para administrar seu perfil, profissionais, procedimentos, horários e atendimentos; a equipe administrativa analisa os pedidos de aprovação.
O projeto foi desenvolvido como aplicação **frontend + API + banco de dados**, com separação das responsabilidades em camadas, conforme a arquitetura proposta na disciplina. O selo de aprovação indica uma **verificação interna do cadastro pela administração da plataforma**, não uma certificação oficial de órgãos de saúde.

## Tecnologias utilizadas

| Camada | Tecnologias |
| --- | --- |
| Interface | CSS e Vite |
| API | Python 3.11+, Flask |
| Persistência e mapeamento | Flask-SQLAlchemy, SQLAlchemy, PyMySQL |
| Banco de dados | MySQL 8.4 (instância local portátil na configuração automática) |
| Testes | pytest, Vitest e React Testing Library |

## Arquitetura da aplicação

Cada funcionalidade é executada por meio do fluxo:

**Interface React → API Flask → Controller → Service → Model/Repository → MySQL**

- **Interface:** apresenta formulários, listagens e ações do usuário, consumindo os endpoints HTTP da API.
- **Controllers:** classes organizadas por recurso, responsáveis por interpretar requisições, acionar o caso de uso correspondente e construir a resposta HTTP, sem implementar regras de negócio.
- **Services:** classes específicas para cada caso de uso, com método público `executar()`, responsáveis pelas validações, autorizações e coordenação das operações.
- **Models:** representam as entidades do domínio e seus relacionamentos. Herdam de `CrudModel`, baseada em `db.Model`, que disponibiliza `salvar()`, `atualizar()`, `deletar()`, `listar_todos()` e `buscar_por_id()`.
- **Repositories:** concentram consultas especializadas, como filtros de clínicas, disponibilidade de horários, recomendações, rankings e relatórios, evitando a criação de camadas de acesso redundantes para o CRUD convencional.
- **Banco de dados:** armazena os registros no MySQL; alterações transacionais são confirmadas após a execução bem-sucedida do caso de uso, com reversão em caso de falha.

A definição das rotas da API está em `backend/routes.py`. A matriz de rastreabilidade de cada funcionalidade, com telas, endpoints, Controllers, Services e persistência, está em [`docs/funcionalidades.md`](docs/funcionalidades.md).

## Funcionalidades Implementadas

As 20 funcionalidades principais da entrega estão organizadas abaixo por operação. Todas possuem componentes de interface, chamadas à API Flask e implementação no backend com acesso aos dados.

1. **Cadastrar cliente** — criação de conta com validação de dados, senha protegida por hash e confirmação de e-mail no ambiente de demonstração.
2. **Fazer login** — autenticação de clientes, clínicas, profissionais e administradores, com controle de acesso conforme o perfil.
3. **Recuperar senha** — solicitação de redefinição por token temporário e cadastro de uma nova senha.
4. **Cadastrar clínica** — registro de dados empresariais, responsável, localização e procedimentos, com análise administrativa antes da publicação.
5. **Aprovar ou rejeitar clínica** — decisão administrativa sobre solicitações, com atualização do status do estabelecimento.
6. **Editar dados da clínica** — manutenção de informações de contato, descrição, endereço e apresentação pública.
7. **Pesquisar clínicas** — consulta por critérios como cidade, procedimento, preço e avaliação.
8. **Recomendar clínicas** — seleção de estabelecimentos a partir das preferências salvas pelo cliente.
9. **Cadastrar profissional** — registro de profissionais vinculados a uma clínica e aos procedimentos realizados.
10. **Editar profissional** — atualização de informações profissionais, biografia e serviços vinculados.
11. **Gerenciar procedimentos e preços** — manutenção do catálogo de serviços e dos valores oferecidos pela clínica.
12. **Configurar agenda** — definição de dias e horários de atendimento, intervalos e datas bloqueadas.
13. **Solicitar agendamento** — escolha de clínica, procedimento, profissional, data e horário disponível.
14. **Confirmar ou concluir agendamento** — gerenciamento do status do atendimento pela clínica ou profissional autorizado.
15. **Remarcar agendamento** — alteração de data ou horário com validação de disponibilidade e registro da mudança.
16. **Cancelar agendamento** — cancelamento sujeito às regras do sistema, com justificativa e atualização da disponibilidade.
17. **Publicar avaliação** — registro de nota e comentário após atendimento concluído, com atualização da avaliação da clínica.
18. **Adicionar clínica aos favoritos** — armazenamento de clínicas favoritas na conta do cliente.
19. **Salvar preferências do cliente** — registro de interesses por procedimentos, cidades e critérios utilizados nas recomendações.
20. **Consultar relatório financeiro** — consulta de indicadores e valores de atendimentos concluídos por período, a partir de dados persistidos.

### Organização das funcionalidades

As operações estão divididas entre os painéis de **cliente**, **clínica**, **profissional** e **administrador**. O projeto contém também recursos complementares de consulta e remoção de favoritos, edição de avaliações, chat, notificações, blog, portfólio e contato. Esses recursos não substituem as 20 funcionalidades enumeradas acima.

A correspondência entre interface, API, Controller, Service e Model/Repository de cada item está documentada em [`docs/funcionalidades.md`](docs/funcionalidades.md).

## Estrutura do projeto

```text
magnolia-royale/
├── backend/
│   ├── controllers/           # Recebimento das requisições e respostas da API
│   ├── services/
│   │   ├── casos_de_uso/      # Classes Service para ações individuais
│   │   └── auxiliares/        # Validações e regras compartilhadas
│   ├── models/                # Entidades SQLAlchemy e métodos CRUD
│   ├── repositories/          # Consultas especializadas ao MySQL
│   ├── tests/                 # Testes de arquitetura e integração
│   ├── app.py                 # Configuração e inicialização do Flask
│   ├── routes.py              # Endpoints da API
│   └── seed.py                # Dados fictícios para demonstração
├── frontend/
│   ├── src/                   # Páginas, componentes, hooks e testes React
│   └── package.json
├── database/                  # Esquema SQL e consultas de referência
├── docs/                      # Documentação e diagrama de classes
├── scripts/                   # Preparação e execução local
├── preparar.cmd               # Instalação automatizada para Windows
├── iniciar.cmd                # Inicialização da aplicação
├── parar-mysql.cmd            # Encerramento da instância MySQL local
└── README.md
```

## Requisitos e execução local

A forma de execução prevista para a apresentação utiliza **Windows 64 bits**, **Python 3.11 ou superior**, conexão com a internet durante a instalação e espaço disponível para as dependências. O preparador obtém automaticamente versões portáteis do **Node.js 24** e do **MySQL 8.4**, sem exigir uma instalação global desses programas. O gerenciador de pacotes do frontend é o **pnpm**.

### 1. Preparar o ambiente

Extraia o projeto em uma pasta local e, no terminal PowerShell aberto na raiz do projeto, execute:

```powershell
.\preparar.cmd
```

O procedimento cria o ambiente Python, instala as dependências, configura o MySQL local, cria os bancos necessários, inclui dados fictícios de demonstração e compila o frontend. Os arquivos gerados ficam em `.venv/`, `.runtime/` e `frontend/node_modules/`; não precisam ser incluídos no repositório.

### 2. Iniciar a aplicação

Após o término da preparação:

```powershell
.\iniciar.cmd
```

Acesse a aplicação em **http://127.0.0.1:5000**. A API pode ser verificada em **http://127.0.0.1:5000/api/health**.

Mantenha o terminal do servidor aberto durante o uso. Para interromper a API, utilize `Ctrl+C`. Para encerrar a instância portátil do banco, utilize `parar-mysql.cmd`.

A configuração automática utiliza a porta `5000` para a aplicação e a porta `3307` para o MySQL local. Essas portas precisam estar disponíveis no computador de execução.

Para usar uma instalação própria do MySQL ou configurar o sistema em outro ambiente, consulte [`docs/instalacao.md`](docs/instalacao.md).

## Contas para demonstração

O preparador cria contas fictícias verificadas para permitir o acesso aos diferentes painéis.

| Perfil | E-mail | Senha |
| --- | --- | --- |
| Cliente | `cliente@magnolia.test` | `Magnolia@123` |
| Clínica | `clinica@magnolia.test` | `Magnolia@123` |
| Profissional | `profissional@magnolia.test` | `Magnolia@123` |
| Administrador | `admin@magnolia.test` | `Magnolia@123` |

As credenciais acima destinam-se **somente ao ambiente local de demonstração**. Novos cadastros podem confirmar o e-mail e recuperar senhas por meio da caixa de mensagens fictícias disponível em `/demo-mailbox`, quando o modo de demonstração estiver ativo.

## Testes e validação

O projeto dispõe de testes automatizados para a organização da arquitetura, fluxos da API e componentes do frontend.
Na raiz do projeto, após `preparar.cmd`, execute:

**Arquitetura e integração (Python/Flask/MySQL):**

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests -q
```

Os testes de integração utilizam o banco **`magnolia_royale_test`**, separado do banco principal **`magnolia_royale`**. A variável `TEST_DATABASE_URL` deve apontar exclusivamente para o banco de testes; a preparação local gera essa configuração no arquivo `backend/.env`.

**Testes do frontend e compilação:**

```powershell
cd frontend
& ..\.runtime\node-v24.22.1-win-x64\npm.cmd test
& ..\.runtime\node-v24.22.1-win-x64\npm.cmd run build
```

Além dos testes automatizados, a validação funcional deve incluir a execução das 20 operações pela interface, conferindo mensagens de retorno, permissões de cada perfil e persistência dos dados após atualizar a página.

## Documentação

- **[Matriz das 20 funcionalidades](docs/funcionalidades.md):** telas, endpoints, Controllers, Services e entidades ou Repositories utilizados.
- **[Instalação e configuração](docs/instalacao.md):** execução automática, utilização de MySQL externo, recompilação do frontend e solução de problemas.
- **[Diagrama de classes UML](docs/diagrama_classes.md):** classes do domínio, principais atributos, relacionamentos e herança.

## Considerações sobre o ambiente

O Magnolia Royale é uma aplicação acadêmica preparada para execução e avaliação em ambiente local. O banco é inicializado com **dados fictícios**, e a confirmação de e-mail é simulada em uma caixa de mensagens interna. O módulo de checkout, quando utilizado, é demonstrativo e não realiza cobranças reais; os relatórios financeiros são baseados nos valores registrados em atendimentos concluídos.

As configurações sensíveis são armazenadas em `backend/.env`, criado localmente pelo preparador. O repositório deve conter apenas `backend/.env.example`, **sem credenciais, arquivos de banco gerados ou dependências instaladas**. O arquivo `.gitignore` contempla `.env`, `.runtime/`, `.venv/`, `node_modules/` e artefatos de compilação.
