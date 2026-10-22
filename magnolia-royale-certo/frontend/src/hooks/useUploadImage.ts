import {useState} from 'react';
import {api} from '../services/api';
export function useUploadImage(){
 const [uploading,setUploading]=useState(false);const [progress,setProgress]=useState(0);const [error,setError]=useState<string|null>(null);
 const uploadImage=async(file:File,path:string):Promise<string|null>=>{
  setUploading(true);setProgress(0);setError(null);
  try{const data=new FormData();data.append('file',file);data.append('context',/document|assessment/.test(path)||file.type==='application/pdf'?'document':'image');
   const result=await api<{url:string}>('/files','POST',data);setProgress(100);return result.url;
  }catch(e){setError((e as Error).message);return null;}finally{setUploading(false);}
 };
 return{uploadImage,uploading,progress,error};
}
export function useUploadClinicImages(){const r=useUploadImage();return{...r,uploadClinicImage:(file:File,id:string)=>r.uploadImage(file,`clinics/${id}`)};}
