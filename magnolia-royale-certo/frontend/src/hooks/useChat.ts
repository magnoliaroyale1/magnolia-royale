import {api} from '../services/api';
import {useAction,useApiResource} from './useApi';
import type {Chat,Message} from '../types';
export function useChats(id:string){const r=useApiResource<Chat[]>(id?'/chats':null,[],true);return{...r,chats:r.data};}
export function useMessages(id:string){const r=useApiResource<Message[]>(id?`/chats/${id}/messages`:null,[],true);return{...r,messages:r.data};}
export function useSendMessage(){const a=useAction(async(id:string,_senderId:string,text:string)=>{await api(`/chats/${id}/messages`,'POST',{text});return true;},false);return{sendMessage:a.run};}
export function useCreateChat(){const a=useAction(async(_clientId:string,clinicId:string,_clientName:string,_clinicName:string):Promise<string|null>=>{const result=await api('/chats','POST',{clinicId});return result.id;},null);return{createChat:a.run};}
export function useMarkAsRead(){return{markAsRead:async(id:string,_userId:string)=>{try{await api(`/chats/${id}/messages`,'PATCH',{});}catch{}}};}
