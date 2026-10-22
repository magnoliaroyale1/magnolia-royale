import { api } from '../services/api';
import { useApiResource } from './useApi';
import type { Clinic,User,DashboardStats } from '../types';
export function useAdminStats(){const r=useApiResource<DashboardStats>('/admin/stats',{totalClinics:0,approvedClinics:0,pendingClinics:0,totalClients:0,estimatedRevenue:0});return {...r,stats:r.data};}
export function usePendingClinics(status="pending"){
  const r=useApiResource<Clinic[]>('/clinics?status='+status,[]);
  const change=(id:string,status:string,feedback='')=>api(`/clinics/${id}/approval`,'PATCH',{status,feedback});
  return {...r,clinics:r.data,approveClinic:(id:string,feedback?:string)=>change(id,'approved',feedback),rejectClinic:(id:string,feedback:string)=>change(id,'rejected',feedback),requestInfo:(id:string,feedback:string)=>change(id,'pending',feedback)};
}
export function useApprovedClinics(){const r=useApiResource<Clinic[]>('/clinics?status=approved',[]);return {...r,clinics:r.data};}
export function useClients(){const r=useApiResource<User[]>('/admin/clients',[]);return {...r,clients:r.data};}
