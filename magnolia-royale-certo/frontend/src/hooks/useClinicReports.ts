import { useApiResource } from './useApi';
import { queryString } from '../services/api';
import type { MonthlyRevenue,RevenueByProfessional,ProcedureCount } from '../types';
const empty={monthlyRevenue:[] as MonthlyRevenue[],revenueByProfessional:[] as RevenueByProfessional[],procedureCounts:[] as ProcedureCount[],totalRevenue:0,averageTicket:0,completedCount:0};
export function useClinicReports(id:string,start='',end='') {
  const r=useApiResource(id?`/clinics/${id}/reports?${queryString({start,end})}`:null,empty);
  return {...r,...r.data};
}
