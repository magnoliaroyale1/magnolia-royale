import {api} from '../services/api';
import {useAction} from './useApi';
export interface AssessmentData {
  documentacao: {
    cnpjFile?: string;
    alvaraFile?: string;
    licencaSanitaria?: string;
    registroVigilancia?: string;
  };
  profissionais: {
    quantidade: number;
    lista: { nome: string; certificacao: string; certificadoFile?: string }[];
  };
  estrutura: {
    fotos: string[];
    equipamentos: string[];
    metragem: string;
  };
  horarios: {
    diasSemana: string[];
    abertura: string;
    fechamento: string;
    atendeFimSemana: boolean;
    horarioFimSemana?: string;
  };
  status: 'pending' | 'completed';
}

const INITIAL_ASSESSMENT: AssessmentData = {
  documentacao: { cnpjFile: '', alvaraFile: '', licencaSanitaria: '', registroVigilancia: '' },
  profissionais: { quantidade: 1, lista: [{ nome: '', certificacao: '', certificadoFile: '' }] },
  estrutura: { fotos: [], equipamentos: [], metragem: '' },
  horarios: { diasSemana: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'], abertura: '08:00', fechamento: '18:00', atendeFimSemana: false },
  status: 'pending'
};


export function useClinicAssessment(id:string){
 const a=useAction(async(data:AssessmentData)=>{await api(`/clinics/${id}/assessment`,'PUT',data);return true;},false);
 return{saveAssessment:a.run,saving:a.loading,getAssessment:()=>api<AssessmentData|null>(`/clinics/${id}/assessment`)};
}
export {INITIAL_ASSESSMENT};
