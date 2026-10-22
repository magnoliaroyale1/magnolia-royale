import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { ClinicPage } from '../pages/ClinicPage';
import { api } from '../services/api';

vi.mock('../context/AuthContext', () => {
  const user = { uid: '2', role: 'client', displayName: 'Marina', emailVerified: true };
  return { useAuth: () => ({ user }) };
});
vi.mock('../services/api', async importOriginal => ({
  ...await importOriginal<typeof import('../services/api')>(), api: vi.fn(),
}));
afterEach(cleanup);

it('envia o ID da ficha profissional na avaliação, mesmo sendo diferente do ID da conta', async () => {
  vi.mocked(api).mockImplementation(async (path, method) => {
    if (method === 'POST') return { id: '17' };
    if (path === '/clinics/1') return { id:'1', name:'Magnolia', address:{city:'São Paulo',state:'SP',street:'Rua',number:'1'}, images:[], procedures:['Peeling'],services:[{name:'Peeling',price:250}],rating:0,reviewCount:0,score:0 };
    if (path.startsWith('/professionals?')) return [{ id:'11',uid:'97',name:'Dra. Camila Alves',procedures:['Peeling'],clinicId:'1',bio:'' }];
    if (path.endsWith('/review-eligibility')) return { canReview:true,reason:'' };
    return [];
  });
  render(<HelmetProvider><MemoryRouter initialEntries={['/clinic/1']}><Routes><Route path="/clinic/:id" element={<ClinicPage/>}/></Routes></MemoryRouter></HelmetProvider>);
  fireEvent.click(await screen.findByRole('tab', { name:'Avaliações (0)' }));
  const professional = await screen.findByRole('option', { name:'Dra. Camila Alves' });
  fireEvent.change(professional.parentElement!, { target: { value:'11' } });
  fireEvent.click(screen.getByRole('button', { name:'5 estrelas' }));
  fireEvent.change(screen.getByPlaceholderText('Conte sua experiência...'), { target:{value:'Atendimento de demonstração.'} });
  fireEvent.click(screen.getByRole('button', { name:'Enviar Avaliação' }));
  await waitFor(() => expect(api).toHaveBeenCalledWith('/clinics/1/reviews','POST',{
    rating:5,comment:'Atendimento de demonstração.',images:[],professionalId:'11',
  }));
});
