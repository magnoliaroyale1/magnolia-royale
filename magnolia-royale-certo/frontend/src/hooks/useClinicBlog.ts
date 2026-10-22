import {api} from '../services/api';
import {useAction,useApiResource} from './useApi';
import type {BlogPost} from '../types';
export function useClinicBlogPosts(id:string){const r=useApiResource<BlogPost[]>(id?`/blog?clinicId=${id}`:null,[]);return {...r,posts:r.data};}
export function useCreateBlogPost(){const a=useAction(async(data:Omit<BlogPost,'id'>)=>{await api('/blog','POST',data);return true;},false);return{createPost:a.run,creating:a.loading};}
export function useUpdateBlogPost(){const a=useAction(async(id:string,data:Partial<BlogPost>)=>{await api(`/blog/${id}`,'PATCH',data);return true;},false);return{updatePost:a.run,updating:a.loading};}
export function useDeleteBlogPost(){const a=useAction(async(id:string)=>{await api(`/blog/${id}`,'DELETE');return true;},false);return{deletePost:a.run,deleting:a.loading};}
