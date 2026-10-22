import {useMemo} from 'react';
import {api} from '../services/api';
import {useAction,useApiResource} from './useApi';
export interface ClientPreferences {procedures:string[];cities:string[];verifiedOnly:boolean;minRating:number;}
export function usePreferences(id:string){
 const r=useApiResource<{preferences:Partial<ClientPreferences>}>(id?'/auth/me':null,{preferences:{procedures:[],cities:[],verifiedOnly:false,minRating:0}});
 const a=useAction(async(preferences:ClientPreferences)=>{await api('/auth/me','PATCH',{preferences});return true;},false);
 const preferences=useMemo(()=>({procedures:[],cities:[],verifiedOnly:false,minRating:0,...r.data.preferences}),[r.data.preferences]);
 return {...r,preferences,savePreferences:a.run};
}
