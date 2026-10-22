import {api} from '../services/api';
import {useAction} from './useApi';
export function useSubmitReport(){const a=useAction(async(clinicId:string,_reporterId:string,reason:string,description:string)=>{await api('/reports','POST',{clinicId,reason,description});return true;},false);return{submitReport:a.run,submitting:a.loading};}
