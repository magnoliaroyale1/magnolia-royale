from decimal import Decimal
from sqlalchemy import text
from backend.database import db


class RelatorioRepository:
    """Consultas de Banco de Dados 2, sempre com parâmetros vinculados."""
    def consultar(self, sql, parameters=None):
        rows = db.session.execute(text(sql), parameters or {}).mappings().all()
        return [{k: float(v) if isinstance(v, Decimal) else v.isoformat() if hasattr(v, 'isoformat') else v for k, v in row.items()} for row in rows]

    def financeiro(self, clinic_id, start, end):
        parameters = {'clinic': clinic_id, 'start': start, 'end': end}
        where = "clinicId = :clinic AND status = 'completed' AND date BETWEEN :start AND :end"
        total = self.consultar(f'SELECT COALESCE(SUM(valor),0) AS totalRevenue, COALESCE(AVG(valor),0) AS averageTicket, COUNT(*) AS completedCount FROM agendamentos WHERE {where}', parameters)[0]
        total['monthlyRevenue'] = self.consultar(f"SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(valor) AS revenue, COUNT(*) AS count FROM agendamentos WHERE {where} GROUP BY DATE_FORMAT(date, '%Y-%m') ORDER BY month", parameters)
        total['revenueByProfessional'] = self.consultar("""
            SELECT p.id, p.name, SUM(a.valor) AS revenue, COUNT(*) AS count
            FROM agendamentos a JOIN profissionais p ON p.id = a.professionalId
            WHERE a.clinicId = :clinic AND a.status = 'completed' AND a.date BETWEEN :start AND :end
            GROUP BY p.id, p.name ORDER BY revenue DESC, p.name
        """, parameters)
        total['procedureCounts'] = self.consultar(f'SELECT procedureId AS id, `procedure` AS name, COUNT(*) AS count, SUM(valor) AS revenue FROM agendamentos WHERE {where} GROUP BY procedureId, `procedure` ORDER BY count DESC, name', parameters)
        return total

    def clientes(self, clinic_id):
        return self.consultar("""
            SELECT u.id AS clientId, u.displayName AS name, u.email, u.phone,
                   SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) AS totalVisits,
                   SUM(CASE WHEN a.status = 'completed' THEN a.valor ELSE 0 END) AS totalSpent,
                   MIN(CASE WHEN a.status = 'completed' THEN a.date END) AS firstVisit,
                   MAX(CASE WHEN a.status = 'completed' THEN a.date END) AS lastVisit
            FROM usuarios u JOIN agendamentos a ON a.clientId = u.id
            WHERE a.clinicId = :clinic
            GROUP BY u.id, u.displayName, u.email, u.phone ORDER BY lastVisit DESC, name
        """, {'clinic': clinic_id})

    def ranking(self):
        return self.consultar("""
            WITH notas AS (
                SELECT clinicId, COUNT(*) AS quantidade, AVG(rating) AS media
                FROM avaliacoes GROUP BY clinicId
            )
            SELECT c.id, c.score, COALESCE(n.media,0) AS media, COALESCE(n.quantidade,0) AS quantidade
            FROM clinicas c LEFT JOIN notas n ON n.clinicId = c.id
            WHERE c.status = 'approved'
            ORDER BY c.score DESC, media DESC, quantidade DESC, c.id
        """)

    def publico(self):
        return self.consultar("""
            SELECT (SELECT COUNT(*) FROM clinicas WHERE status = 'approved') AS clinics,
                (SELECT COUNT(*) FROM avaliacoes a JOIN clinicas c ON c.id=a.clinicId WHERE c.status='approved') AS reviews,
                (SELECT COUNT(*) FROM usuarios WHERE role='client' AND active=1) AS clients,
                (SELECT COUNT(*) FROM clinicas WHERE status='approved' AND verified=1) AS verified
        """)[0]

    def administrativo(self):
        data = self.consultar("""
            SELECT COUNT(*) AS totalClinics,
                COALESCE(SUM(status = 'approved'),0) AS approvedClinics,
                COALESCE(SUM(status = 'pending'),0) AS pendingClinics,
                COALESCE(SUM(CASE WHEN status = 'approved' THEN
                    CASE plan WHEN 'premium' THEN 397 WHEN 'professional' THEN 197 ELSE 97 END
                    ELSE 0 END),0) AS estimatedRevenue
            FROM clinicas
        """)[0]
        data['totalClients'] = self.consultar("SELECT COUNT(*) AS total FROM usuarios WHERE role = 'client' AND active = 1")[0]['total']
        return data
