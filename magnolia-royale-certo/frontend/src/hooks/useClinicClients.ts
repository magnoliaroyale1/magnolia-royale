import { useApiResource } from './useApi';
import type { ClientSummary } from '../types';
export function useClinicClients(id:string) {const r=useApiResource<ClientSummary[]>(id?`/clinics/${id}/clients`:null,[]);return {...r,clients:r.data};}
