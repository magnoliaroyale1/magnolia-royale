import { api } from '../services/api';
import { useAction, useApiResource } from './useApi';
import type { Clinic } from '../types';
export function useClinicProfile(clinicId: string) {
  const resource = useApiResource<Clinic | null>(clinicId ? `/clinics/${clinicId}` : null, null);
  const action = useAction(async (data: Partial<Clinic>) => { await api(`/clinics/${clinicId}`, 'PATCH', data); return true; }, false);
  return { ...resource, clinic: resource.data, updateClinic: action.run, updating: action.loading,
    addImage: (url: string) => action.run({ images: [...(resource.data?.images || []), url] }),
    removeImage: (index: number) => action.run({ images: (resource.data?.images || []).filter((_, i) => i !== index) }) };
}
