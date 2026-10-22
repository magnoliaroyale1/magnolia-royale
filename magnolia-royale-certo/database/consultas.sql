-- Consultas didáticas equivalentes às usadas no RelatorioRepository.
-- Neste arquivo, variáveis MySQL facilitam executar os exemplos no Workbench.
-- Na API, os valores são parâmetros vinculados (:clinic, :start, :end).
USE magnolia_royale;
SET @clinica = 1;
SET @inicio = '2026-01-01';
SET @fim = '2026-12-31';

-- JOIN + WHERE + GROUP BY + ORDER BY: atendimentos concluídos por profissional.
SELECT p.id, p.name, COUNT(*) AS quantidade, SUM(a.valor) AS valor_total
FROM agendamentos a JOIN profissionais p ON p.id = a.professionalId
WHERE a.clinicId=@clinica AND a.status='completed' AND a.date BETWEEN @inicio AND @fim
GROUP BY p.id,p.name ORDER BY valor_total DESC;

-- CASE: histórico por cliente preservando a distinção entre reserva e atendimento.
SELECT u.id,u.displayName,
    SUM(CASE WHEN a.status='completed' THEN 1 ELSE 0 END) AS visitas_concluidas,
    SUM(CASE WHEN a.status='completed' THEN a.valor ELSE 0 END) AS valor_concluido
FROM usuarios u JOIN agendamentos a ON a.clientId=u.id
WHERE a.clinicId=@clinica GROUP BY u.id,u.displayName ORDER BY valor_concluido DESC;

-- CTE + LEFT JOIN: ranking de clínicas aprovadas, incluindo as sem avaliação.
WITH notas AS (
    SELECT clinicId, COUNT(*) AS quantidade, AVG(rating) AS media
    FROM avaliacoes GROUP BY clinicId
)
SELECT c.id,c.name,c.score,COALESCE(n.media,0) AS media,COALESCE(n.quantidade,0) AS quantidade
FROM clinicas c LEFT JOIN notas n ON n.clinicId=c.id
WHERE c.status='approved'
ORDER BY c.score DESC,media DESC,quantidade DESC,c.id;

-- Conferir persistência e histórico após gravar uma reserva na tela.
SELECT id,clientId,professionalId,clinicId,`procedure`,date,time,status,valor
FROM agendamentos WHERE clinicId=@clinica ORDER BY id DESC;
SELECT * FROM historico_agendamentos ORDER BY id DESC;
