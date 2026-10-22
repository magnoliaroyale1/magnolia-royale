# Matriz das 20 funcionalidades implementadas

Cada funcionalidade abaixo possui execução na interface React, chamada ao Flask, Controller em classe, Service por caso de uso, Model/Repository e MySQL.
Os nomes de Service correspondem a classes nos arquivos `backend/services/casos_de_uso/<recurso>/`.
A matriz descreve **a implementação**; a aprovação operacional após a reorganização depende dos testes com MySQL no computador da escola.

| Nº | Caso de uso | Tela | API Flask | Controller | Service | Persistência |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cadastrar cliente | /register | POST /api/auth/register | AuthController | CadastrarClienteService | Usuario |
| 2 | Fazer login | /login | POST /api/auth/login | AuthController | AutenticarUsuarioService | Usuario |
| 3 | Recuperar senha | /login (Esqueci minha senha), /reset-password | POST /api/auth/password-request; POST /api/auth/reset | AuthController | SolicitarRedefinicaoSenhaService; RedefinirSenhaService | Usuario, TokenConta |
| 4 | Cadastrar clínica | /register-clinic | POST /api/clinics | ClinicaController | CadastrarClinicaService | Usuario, Clinica, Agenda, Procedimento |
| 5 | Aprovar ou rejeitar clínica | Painel Admin → Aprovações | PATCH /api/clinics/:id/approval | AprovacaoController | AprovarClinicaService / RejeitarClinicaService / SolicitarAjustesClinicaService | Clinica, Notificacao |
| 6 | Editar dados da clínica | Painel Clínica → Perfil | PATCH /api/clinics/:id | ClinicaController | AtualizarClinicaService | Clinica, Procedimento, AvaliacaoRepository |
| 7 | Pesquisar clínicas | /clinics | GET /api/clinics | ClinicaController | PesquisarClinicasService | ClinicaRepository |
| 8 | Recomendar clínicas | Meu Painel → Favoritos | GET /api/recommendations | RecomendacaoController | RecomendarClinicasService | Usuario, ClinicaRepository |
| 9 | Cadastrar profissional | Painel Clínica → Profissionais | POST /api/professionals | ProfissionalController | CadastrarProfissionalService | Usuario, Profissional, ProfissionalProcedimento |
| 10 | Editar profissional | Painel Clínica → Profissionais | PATCH /api/professionals/:id | ProfissionalController | AtualizarProfissionalService | Profissional, Usuario, ProfissionalProcedimento |
| 11 | Gerenciar procedimentos e preços | Painel Clínica → Perfil | PATCH /api/clinics/:id | ClinicaController | SalvarProcedimentosService (via AtualizarClinicaService) | Procedimento |
| 12 | Configurar agenda | Painel Clínica → Agenda | PUT /api/clinics/:id/schedule | AgendaController | AtualizarAgendaService | Agenda, Agendamento |
| 13 | Solicitar agendamento | Página da clínica | POST /api/appointments | AgendamentoController | CriarAgendamentoService | Agendamento, AgendamentoRepository |
| 14 | Confirmar ou concluir agendamento | Painel Clínica/Profissional | PATCH /api/appointments/:id | AgendamentoController | ConfirmarAgendamentoService / ConcluirAgendamentoService | Agendamento, HistoricoAgendamento |
| 15 | Remarcar agendamento | Meu Painel → Agendamentos | PATCH /api/appointments/:id | AgendamentoController | RemarcarAgendamentoService | Agendamento, AgendamentoRepository |
| 16 | Cancelar agendamento | Meu Painel → Agendamentos | PATCH /api/appointments/:id | AgendamentoController | CancelarAgendamentoService | Agendamento, HistoricoAgendamento |
| 17 | Publicar avaliação | Página da clínica → Avaliações | POST /api/clinics/:id/reviews | AvaliacaoController | CriarAvaliacaoService | Avaliacao, Agendamento, AvaliacaoRepository |
| 18 | Adicionar clínica aos favoritos | Página da clínica | PUT /api/favorites/:clinic_id | FavoritoController | AdicionarFavoritoService | Favorito, Clinica, Usuario |
| 19 | Salvar preferências | Meu Painel → Preferências | PATCH /api/auth/me | AuthController | SalvarPreferenciasService | Usuario |
| 20 | Consultar relatórios financeiros | Painel Clínica → Relatórios | GET /api/clinics/:id/reports | RelatorioController | GerarRelatorioFinanceiroService | RelatorioRepository |

## Organização e limites

- Controllers: `backend/controllers/` recbem corpo/parametrização HTTP, escolhem o Service apropriado e devolvem JSON por `ApiController`.
- Services: uma classe por ação, com método `executar()`; há classes auxiliares sem endpoint em `backend/services/auxiliares/` para compartilhar permissões e validações.
- Models: todas herdam de `CrudModel`, que herda de `db.Model` e cetraliza `salvar()`, `atualizar()`, `deletar()`, `listar_todos()`, `buscar_por_id()`.
- Repositories: somente filtros composts, ordenações, junções, relatórios e outras consultas especiais. Nenhum Controller executa SQL.
- Transação: uma requisição tem um commit ao terminar, com rollback em erro.
- Os filtros são validados no Service e os resultados são consultados no MySQL.