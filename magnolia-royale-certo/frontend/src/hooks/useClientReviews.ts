import { api } from '../services/api';
import { useAction,useApiResource } from './useApi';
import type { Review } from '../types';
export function useClientReviews(id:string) {
  const r=useApiResource<(Review & {clinicName?:string})[]>(id?'/reviews/me':null,[]);
  return {...r,reviews:r.data};
}
export function useEditReview() {
  const a=useAction(async (_clinicId:string,id:string,data:{rating?:number;comment?:string})=>{await api(`/reviews/${id}`,'PATCH',data);return true;},false);
  return {editReview:a.run,editing:a.loading};
}
