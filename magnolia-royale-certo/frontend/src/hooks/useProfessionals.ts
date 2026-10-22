import { api } from '../services/api';
import { useAction, useApiResource } from './useApi';
import type { Professional } from '../types';
export function useProfessionalsByClinic(clinicId: string) {
  const resource = useApiResource<Professional[]>(clinicId ? `/professionals?clinicId=${clinicId}` : null, []);
  return { ...resource, professionals: resource.data };
}
export function useProfessional(uid: string) {
  const resource = useApiResource<Professional | null>(uid ? '/professionals/me' : null, null);
  return { ...resource, professional: resource.data };
}
export function useCreateProfessional() {
  const action = useAction(async (data: {clinicId: string; name: string; email: string; password: string; bio: string; procedures: string[]}) => { await api('/professionals', 'POST', data); return true; }, false);
  return { createProfessional: action.run, creating: action.loading };
}
export function useUpdateProfessional() {
  const action = useAction(async (id: string, data: Partial<Professional>) => { await api(`/professionals/${id}`, 'PATCH', data); return true; }, false);
  return { updateProfessional: action.run, updating: action.loading };
}
export function useDeleteProfessional() {
  const action = useAction(async (id: string) => { await api(`/professionals/${id}`, 'DELETE'); return true; }, false);
  return { deleteProfessional: action.run, deleting: action.loading };
}
