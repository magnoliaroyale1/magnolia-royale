import { beforeEach, afterEach, expect, it, vi } from 'vitest';

beforeEach(() => vi.resetModules());
afterEach(() => vi.unstubAllGlobals());
const response = (data: unknown, ok = true) => ({ ok, text: async () => JSON.stringify(data) });

it('obtém proteção de sessão e só avisa atualização depois da gravação confirmada', async () => {
  const fetchMock = vi.fn()
    .mockResolvedValueOnce(response({ csrfToken: 'teste' }))
    .mockResolvedValueOnce(response({ id: '15', date: '2026-09-25' }));
  vi.stubGlobal('fetch', fetchMock);
  const changed = vi.fn();
  window.addEventListener('data-changed', changed);
  try {
    const { api } = await import('../services/api');
    const result = await api('/appointments', 'POST', { time: '10:00' });
    expect(fetchMock.mock.calls[0][0]).toBe('/api/auth/session');
    expect(fetchMock.mock.calls[1][1].headers['X-CSRF-Token']).toBe('teste');
    expect(result.date.getDate()).toBe(25);
    expect(changed).toHaveBeenCalledTimes(1);
  } finally { window.removeEventListener('data-changed', changed); }
});

it('exibe rejeições de agendamento da API sem anunciar que gravou', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValueOnce(response({ csrfToken: 'teste' }))
    .mockResolvedValueOnce(response({ error: 'Horário indisponível.' }, false)));
  const failed = vi.fn(); const changed = vi.fn();
  window.addEventListener('api-error', failed); window.addEventListener('data-changed', changed);
  try {
    const { api } = await import('../services/api');
    await expect(api('/appointments', 'POST', {})).rejects.toThrow('Horário indisponível.');
    expect(failed.mock.calls[0][0].detail).toBe('Horário indisponível.');
    expect(changed).not.toHaveBeenCalled();
  } finally { window.removeEventListener('api-error', failed); window.removeEventListener('data-changed', changed); }
});

it('preserva a data civil do atendimento e interpreta horários UTC', async () => {
  const { decodeDates, queryString } = await import('../services/api');
  const decoded = JSON.parse('{"date":"2026-09-25","createdAt":"2026-09-25T02:00:00Z","name":"2026-09-25"}', decodeDates);
  expect(decoded.date.getDate()).toBe(25);
  expect(decoded.createdAt.toISOString()).toBe('2026-09-25T02:00:00.000Z');
  expect(decoded.name).toBe('2026-09-25');
  expect(queryString({ minPrice: 0, verifiedOnly: false, location: 'São Paulo', unused: undefined })).toBe('minPrice=0&verifiedOnly=false&location=S%C3%A3o+Paulo');
});

it('mantém a agenda no dia brasileiro quando já passou da meia-noite UTC', async () => {
  const { todayAgenda, dateInput } = await import('../utils/date');
  expect(todayAgenda(new Date('2026-09-20T01:00:00Z'))).toBe('2026-09-19');
  expect(todayAgenda(new Date('2026-09-20T03:00:00Z'))).toBe('2026-09-20');
  expect(dateInput(new Date(2026,8,25,12))).toBe('2026-09-25');
});
