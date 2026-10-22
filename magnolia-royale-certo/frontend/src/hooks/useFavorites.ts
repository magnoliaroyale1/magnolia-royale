import { api } from '../services/api';
import { useApiResource } from './useApi';
import { useAuth } from '../context/AuthContext';
import type { Clinic } from '../types';
export function useFavoriteClinics(userId:string) {
  const {isClient}=useAuth();
  const r=useApiResource<Clinic[]>(userId&&isClient?'/favorites':null,[]);
  return {...r,clinics:r.data};
}
export function useFavorites(userId:string) {
  const r=useFavoriteClinics(userId); const favorites=r.clinics.map(c=>c.id);
  return {...r,favorites,isFavorite:(id:string)=>favorites.includes(id),toggleFavorite:async(id:string)=>{
    try {await api(`/favorites/${id}`,favorites.includes(id)?'DELETE':'PUT');} catch { /* Mensagem exibida pelo ApiNotice. */ }
  }};
}
