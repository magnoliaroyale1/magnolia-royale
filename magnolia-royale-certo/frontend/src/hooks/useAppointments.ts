import { api, queryString } from '../services/api';
import { useAction, useApiResource } from './useApi';
import type { Appointment } from '../types';
function useAppointments(id: string, filters: Record<string, string>) {
  const resource = useApiResource<Appointment[]>(id ? '/appointments?' + queryString(filters) : null, [], true);
  return { ...resource, appointments: resource.data };
}
export const useAppointmentsByClient = (id: string) => useAppointments(id, {clientId: id});
export const useAppointmentsByClinic = (id: string) => useAppointments(id, {clinicId: id});
export const useAppointmentsByProfessional = (id: string) => useAppointments(id, {professionalId: id});
export const usePendingAppointments = (id: string) => useAppointments(id, {clinicId: id, status: 'pending'});
export function useCreateAppointment() {
  const action = useAction(async (data: Omit<Appointment, 'id'>) => { await api('/appointments', 'POST', data); return true; }, false);
  return { createAppointment: action.run, creating: action.loading };
}
export function useUpdateAppointmentStatus() {
  const action = useAction(async (id: string, status: Appointment['status']) => { await api(`/appointments/${id}`, 'PATCH', {status}); return true; }, false);
  return { updateStatus: action.run };
}
export function useCancelAppointment() {
  const action = useAction(async (id: string, reason?: string) => { await api(`/appointments/${id}`, 'PATCH', {action: 'cancel', reason}); return true; }, false);
  return { cancelAppointment: action.run, cancelling: action.loading };
}
export function useRescheduleAppointment() {
  const action = useAction(async (id: string, date: Date, time: string) => { await api(`/appointments/${id}`, 'PATCH', {action: 'reschedule', date, time}); return true; }, false);
  return { rescheduleAppointment: action.run, rescheduling: action.loading };
}
