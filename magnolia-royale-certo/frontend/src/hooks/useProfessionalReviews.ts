import { useReviews } from './useReviews';
import { useAuth } from '../context/AuthContext';
export function useProfessionalReviews(id:string) {
  const {user}=useAuth(); const r=useReviews(user?.clinicId||'');
  const reviews=r.reviews.filter(review=>review.professionalId===id);
  return {...r,reviews,reviewCount:reviews.length,avgRating:reviews.length?reviews.reduce((sum,r)=>sum+r.rating,0)/reviews.length:0};
}
