import { api } from '../services/api';
import { useAction, useApiResource } from './useApi';
import type { Review } from '../types';
export function useReviews(clinicId: string) {
  const r=useApiResource<Review[]>(clinicId ? `/clinics/${clinicId}/reviews` : null, []);
  return {...r,reviews:r.data};
}
export function useCheckCanReview() {
  return {checkCanReview: (clinicId:string, _clientId:string) => api<{canReview:boolean;reason:string}>(`/clinics/${clinicId}/review-eligibility`)};
}
export function useSubmitReview() {
  const a=useAction(async (clinicId:string,_clientId:string,_clientName:string,rating:number,comment:string,images?:string[],professionalId?:string) => {
    await api(`/clinics/${clinicId}/reviews`,'POST',{rating,comment,images:images||[],professionalId}); return true;
  },false);
  return {submitReview:a.run,submitting:a.loading};
}
