export const toDate = (value: Date | string | undefined | null): Date | null => {
  if (!value) return null;
  const result = value instanceof Date ? value : new Date(/^\d{4}-\d{2}-\d{2}$/.test(value) ? value+'T12:00:00' : value);
  return Number.isNaN(result.getTime()) ? null : result;
};
export const formatDateBR = (value: Date | string | undefined | null) => toDate(value)?.toLocaleDateString('pt-BR') || '';
export const formatTimeBR = (value: Date | string | undefined | null) => toDate(value)?.toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'}) || '';
export const dateInput = (value: Date) => `${value.getFullYear()}-${String(value.getMonth()+1).padStart(2,'0')}-${String(value.getDate()).padStart(2,'0')}`;
// A agenda da API trabalha em UTC-3, mesmo quando o computador usa outro fuso.
export const todayAgenda = (now = new Date()) => new Date(now.getTime()-3*60*60*1000).toISOString().slice(0,10);
