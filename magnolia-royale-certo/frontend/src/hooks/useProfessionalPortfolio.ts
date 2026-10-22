import {api} from '../services/api';
import {useAction,useApiResource} from './useApi';
import type {ProfessionalPortfolio} from '../types';
export function useProfessionalPortfolio(id:string){const r=useApiResource<ProfessionalPortfolio[]>(id?`/professionals/${id}/portfolio`:null,[]);return{...r,portfolio:r.data};}
export function useAddPortfolioItem(){const a=useAction(async(id:string,data:{imageUrl:string;procedure:string;description:string})=>{await api(`/professionals/${id}/portfolio`,'POST',data);return true;},false);return{addItem:a.run,adding:a.loading};}
export function useDeletePortfolioItem(){const a=useAction(async(_professionalId:string,id:string)=>{await api(`/portfolio/${id}`,'DELETE');return true;},false);return{deleteItem:a.run,deleting:a.loading};}
