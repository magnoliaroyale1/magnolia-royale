import { useApiResource } from './useApi';
import { queryString } from '../services/api';
export function useProfessionalAvailability(clinicId: string, professionalId: string, date: string) {
  const resource = useApiResource<string[]>(clinicId && professionalId && date ? `/clinics/${clinicId}/availability?` + queryString({professionalId,date}) : null, [], true);
  return {...resource, availableSlots:resource.data};
}
