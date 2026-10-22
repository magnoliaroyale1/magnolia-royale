import {api} from '../services/api';
import {useApiResource} from './useApi';
import {useAuth} from '../context/AuthContext';
export interface AppNotification{id?:string;userId:string;type:'appointment_reminder'|'new_clinic'|'promotion'|'approval'|'message';title:string;message:string;link?:string;read:boolean;createdAt:Date;}
export function useNotifications(id:string){
 const {user}=useAuth();const r=useApiResource<AppNotification[]>(id&&user?.emailVerified?'/notifications':null,[],true);
 return{...r,notifications:r.data,unreadCount:r.data.filter(n=>!n.read).length,fetchNotifications:r.refetch,
 markAsRead:async(id:string)=>{try{await api(`/notifications/${id}`,'PATCH',{});}catch{}},
 markAllAsRead:async()=>{try{await api('/notifications','PATCH',{});}catch{}}};
}
