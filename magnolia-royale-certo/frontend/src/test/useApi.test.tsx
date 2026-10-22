import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { api } from '../services/api';
import { useApiResource } from '../hooks/useApi';
vi.mock('../services/api', () => ({ api: vi.fn() }));
beforeEach(() => vi.mocked(api).mockReset());
afterEach(cleanup);

it('ignora resposta atrasada de outra clínica após trocar a página', async () => {
  let finishFirst!: (value: string[]) => void;
  vi.mocked(api).mockImplementationOnce(() => new Promise(resolve => { finishFirst = resolve; }))
    .mockResolvedValueOnce(['Clínica B']);
  const { result, rerender } = renderHook(({ path }) => useApiResource<string[]>(path, []), { initialProps: { path: '/clinics/1' } });
  rerender({ path: '/clinics/2' });
  await waitFor(() => expect(result.current.data).toEqual(['Clínica B']));
  await act(async () => { finishFirst(['Clínica A']); });
  expect(result.current.data).toEqual(['Clínica B']);
});

it('atualiza o painel depois de uma gravação e remove dados ao sair da conta', async () => {
  vi.mocked(api).mockResolvedValueOnce(['pendente']).mockResolvedValueOnce(['cancelado']);
  const { result, rerender } = renderHook(({ path }) => useApiResource<string[]>(path, []), { initialProps: { path: '/appointments' as string | null } });
  await waitFor(() => expect(result.current.data).toEqual(['pendente']));
  act(() => { window.dispatchEvent(new Event('data-changed')); });
  await waitFor(() => expect(result.current.data).toEqual(['cancelado']));
  rerender({ path: null });
  await waitFor(() => expect(result.current.data).toEqual([]));
  expect(result.current.loading).toBe(false);
});
