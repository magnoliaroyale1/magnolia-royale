import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { HelmetProvider } from 'react-helmet-async';
import { Blog } from '../pages/Blog';
import { useBlogPosts } from '../hooks/useBlogPosts';

vi.mock('../hooks/useBlogPosts', () => ({ useBlogPosts: vi.fn() }));
afterEach(cleanup);

const demo = [
  {
    id: '1', title: 'Conheça nosso espaço de cuidado',
    excerpt: 'Um ambiente preparado para receber você.',
    content: 'Texto integral do primeiro artigo.', image: '/clinic-demo.svg',
    author: 'Clínica Magnolia Jardins', clinicName: 'Clínica Magnolia Jardins',
    category: 'Bem-estar', readTime: 1, createdAt: new Date('2026-10-22T12:00:00'),
  },
  {
    id: '2', title: 'Conheça nosso espaço de cuidado',
    excerpt: 'Um ambiente preparado para receber você.',
    content: 'Texto integral do segundo artigo.', image: '/clinic-demo.svg',
    author: 'Essência Royale', clinicName: 'Essência Royale',
    category: 'Bem-estar', readTime: 1, createdAt: new Date('2026-10-22T12:00:00'),
  },
];

it('abre o artigo correto, mesmo quando as publicações de demonstração têm o mesmo título', async () => {
  vi.mocked(useBlogPosts).mockReturnValue({ posts: demo, loading: false } as ReturnType<typeof useBlogPosts>);
  render(<HelmetProvider><Blog /></HelmetProvider>);

  const second = screen.getByRole('button', { name: /ler artigo: conheça nosso espaço de cuidado — essência royale/i });
  fireEvent.click(second);
  const dialog = screen.getByRole('dialog');
  expect(within(dialog).getByText('Texto integral do segundo artigo.')).toBeInTheDocument();
  expect(within(dialog).getByText('Publicado por Essência Royale')).toBeInTheDocument();
  expect(within(dialog).queryByText('Texto integral do primeiro artigo.')).not.toBeInTheDocument();

  fireEvent.click(within(dialog).getByRole('button', { name: 'Fechar artigo' }));
  await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
});

it('permite abrir os artigos por teclado', () => {
  vi.mocked(useBlogPosts).mockReturnValue({ posts: demo, loading: false } as ReturnType<typeof useBlogPosts>);
  render(<HelmetProvider><Blog /></HelmetProvider>);
  fireEvent.keyDown(screen.getByRole('button', { name: /ler artigo: conheça nosso espaço de cuidado — clínica magnolia jardins/i }), { key: 'Enter' });
  expect(within(screen.getByRole('dialog')).getByText('Texto integral do primeiro artigo.')).toBeInTheDocument();
});
