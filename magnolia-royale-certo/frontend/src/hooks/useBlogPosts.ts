import {useApiResource} from './useApi';
import type {BlogPost} from '../types';
export function useBlogPosts(clinicId?:string){const r=useApiResource<BlogPost[]>('/blog'+(clinicId?`?clinicId=${clinicId}`:''),[]);return {...r,posts:r.data};}
