import {api} from '../services/api';
import {useAction} from './useApi';
export function useCheckout(){
 const create=useAction(async(clinicId:string,plan:'basic'|'professional'|'premium',_price:number):Promise<string|null>=>{const result=await api(`/clinics/${clinicId}/checkouts`,'POST',{plan});return result.id;},null);
 const complete=useAction(async(clinicId:string,id:string,paymentMethod:'credit_card'|'boleto'|'pix')=>{await api(`/clinics/${clinicId}/checkouts/${id}`,'PATCH',{paymentMethod});return true;},false);
 return{createCheckoutSession:create.run,completeCheckout:complete.run,processing:create.loading||complete.loading};
}
