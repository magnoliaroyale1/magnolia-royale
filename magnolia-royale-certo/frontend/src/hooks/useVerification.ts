import {api} from '../services/api';
import {useAction} from './useApi';
import type {Clinic} from '../types';
export interface VerificationCriteria{documentacaoValida:boolean;profissionaisQualificados:boolean;boasAvaliacoes:boolean;assessmentCompleto:boolean;}
export function useVerification(){const a=useAction(async(id:string,criteria:VerificationCriteria,_clinic:Partial<Clinic>)=>{await api(`/clinics/${id}/verification`,'PATCH',{criteria});return true;},false);return{updateVerification:a.run,updating:a.loading};}
