import {api} from '../services/api';
import {useApiResource} from './useApi';
export interface SearchHistoryItem{id:string;query:string;term:string;filters:Record<string,string>;createdAt:Date;}
export function useSearchHistory(id:string){
 const r=useApiResource<SearchHistoryItem[]>(id?'/search-history':null,[]);
 return {...r,history:r.data,saveSearch:async(query:string,filters:Record<string,string>)=>{if(id)try{await api('/search-history','POST',{query,filters});}catch{}}};
}
