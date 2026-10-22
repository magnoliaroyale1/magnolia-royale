import { createContext, useContext, useEffect, useState, useCallback, type ReactNode } from 'react';
import { api, getSession, notifyError } from '../services/api';
import type { User } from '../types';

interface AuthContextType {
  user: User | null; loading: boolean; demoMode: boolean;
  isAdmin: boolean; isClinic: boolean; isClient: boolean; isProfessional: boolean;
  register: (email: string, password: string, name: string, role: User['role']) => Promise<void>;
  registerClinic: (data: unknown) => Promise<void>;
  login: (email: string, password: string) => Promise<User>;
  logout: () => Promise<void>;
  sendVerificationEmail: () => Promise<void>;
  deleteAccount: (password: string) => Promise<void>;
  refreshUser: () => Promise<User | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [demoMode, setDemoMode] = useState(false);
  const refreshUser = useCallback(async () => {
    const session = await getSession(); setUser(session.user); setDemoMode(session.demoMode); return session.user;
  }, []);
  useEffect(() => { refreshUser().catch(notifyError).finally(() => setLoading(false)); }, [refreshUser]);
  const register = async (email: string, password: string, name: string, role: User['role']) => setUser(await api('/auth/register', 'POST', { email, password, name, role }));
  const registerClinic = async (data: unknown) => setUser(await api('/clinics', 'POST', data));
  const login = async (email: string, password: string) => { const result = await api<User>('/auth/login', 'POST', { email, password }); setUser(result); return result; };
  const logout = async () => { await api('/auth/logout', 'POST', {}); setUser(null); };
  const sendVerificationEmail = async () => { await api('/auth/verification-request', 'POST', {}); };
  const deleteAccount = async (password: string) => { await api('/auth/me', 'DELETE', { password }); setUser(null); };
  return <AuthContext.Provider value={{ user, loading, demoMode, register, registerClinic, login, logout, sendVerificationEmail, deleteAccount, refreshUser,
    isAdmin: user?.role === 'admin', isClinic: user?.role === 'clinic', isClient: user?.role === 'client', isProfessional: user?.role === 'professional' }}>{children}</AuthContext.Provider>;
}
export function useAuth() { const context = useContext(AuthContext); if (!context) throw new Error('AuthProvider ausente'); return context; }
