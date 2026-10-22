import { useApiResource } from './useApi';
import type { Clinic } from '../types';
export function useClinics(status?: string) {
  const resource = useApiResource<Clinic[]>('/clinics' + (status ? `?status=${status}` : ''), []);
  return { ...resource, clinics: resource.data };
}
