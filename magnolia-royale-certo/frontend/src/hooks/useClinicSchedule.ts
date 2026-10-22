import { api } from '../services/api';
import { useAction, useApiResource } from './useApi';
import type { ClinicSchedule } from '../types';
export const DEFAULT_SCHEDULE: ClinicSchedule = {daysOfWeek:[1,2,3,4,5], startTime:'09:00', endTime:'17:00', slotDuration:60, blockedDates:[]};
export function useClinicSchedule(id: string) {
  const resource = useApiResource<ClinicSchedule>(id ? `/clinics/${id}/schedule` : null, DEFAULT_SCHEDULE);
  return {...resource, schedule:resource.data};
}
export function useUpdateSchedule() {
  const action = useAction(async (id: string, data: ClinicSchedule) => { await api(`/clinics/${id}/schedule`, 'PUT', data); return true; }, false);
  return {updateSchedule:action.run, updating:action.loading};
}
// Prévia visual; disponibilidade e validação definitivas são calculadas no servidor.
export function generateTimeSlots(schedule: ClinicSchedule) {
  const minutes = (time: string) => { const [h,m] = time.split(':').map(Number); return h*60+m; };
  const result: string[] = [];
  if (schedule.slotDuration <= 0) return result;
  for (let m=minutes(schedule.startTime); m+schedule.slotDuration<=minutes(schedule.endTime); m+=schedule.slotDuration) result.push(`${String(Math.floor(m/60)).padStart(2,'0')}:${String(m%60).padStart(2,'0')}`);
  return result;
}
export const isBlockedDate = (schedule: ClinicSchedule, date: Date) => !schedule.daysOfWeek.includes(date.getDay()) || schedule.blockedDates.includes(date.toISOString().slice(0,10));
