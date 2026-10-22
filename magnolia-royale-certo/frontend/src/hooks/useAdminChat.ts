import {useEffect,useState} from 'react';
import {api} from '../services/api';
import {useAction,useApiResource} from './useApi';
import type {Message} from '../types';
export interface SupportChat{id:string;userId:string;userName:string;userRole:'clinic'|'client';participants:string[];lastMessage?:string;lastMessageAt?:Date;unreadCount:number;createdAt:Date;}
export function useAdminSupportChats(){const r=useApiResource<SupportChat[]>('/support-chats',[],true);return{...r,chats:r.data};}
export function useAdminSupportMessages(id:string){const r=useApiResource<(Message&{senderName:string})[]>(id?`/chats/${id}/messages`:null,[],true);return{...r,messages:r.data};}
export function useSendAdminMessage(){const a=useAction(async(id:string,text:string)=>{await api(`/chats/${id}/messages`,'POST',{text});return true;},false);return{sendMessage:a.run};}
export function useUserSupportChat(userId:string,_name:string,_role:'clinic'|'client'){
 const [chatId,setChatId]=useState<string|null>(null);const [loading,setLoading]=useState(Boolean(userId));
 useEffect(()=>{let active=true;if(!userId){setLoading(false);return;}api('/support-chats','POST',{}).then(chat=>{if(active)setChatId(chat.id);}).catch(()=>{}).finally(()=>{if(active)setLoading(false);});return()=>{active=false;};},[userId]);
 return{chatId,loading};
}
export const useUserSupportMessages=(id:string|null)=>useAdminSupportMessages(id||'');
export function useSendUserSupportMessage(){const a=useAction(async(id:string,_senderId:string,_name:string,text:string)=>{await api(`/chats/${id}/messages`,'POST',{text});return true;},false);return{sendMessage:a.run};}
