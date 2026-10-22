import {useApiResource} from './useApi';
import {useAuth} from '../context/AuthContext';
import type {Clinic} from '../types';
import type {ClientPreferences} from './usePreferences';
export function useRecommendations(_preferences:ClientPreferences|null){
 const {user}=useAuth(); const r=useApiResource<Clinic[]>(user?'/recommendations':null,[]);
 return {...r,clinics:r.data};
}
