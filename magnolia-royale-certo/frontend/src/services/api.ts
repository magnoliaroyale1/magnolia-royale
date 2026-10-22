let csrfToken = '';
let sessionRequest: Promise<any> | null = null;

export function decodeDates(key: string, value: unknown): unknown {
  if (typeof value !== 'string') return value;
  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*Z$/.test(value)) return new Date(value);
  if (['date', 'firstVisit', 'lastVisit'].includes(key) && /^\d{4}-\d{2}-\d{2}$/.test(value)) return new Date(value + 'T12:00:00');
  return value;
}

export function notifyError(error: unknown) {
  window.dispatchEvent(new CustomEvent('api-error', { detail: error instanceof Error ? error.message : 'Não foi possível concluir a operação.' }));
}

export async function getSession() {
  if (!sessionRequest) {
    sessionRequest = fetch('/api/auth/session', { credentials: 'same-origin' })
      .then(async response => {
        if (!response.ok) throw new Error('Não foi possível conectar à API.');
        const data = JSON.parse(await response.text(), decodeDates);
        csrfToken = data.csrfToken;
        return data;
      }).finally(() => { sessionRequest = null; });
  }
  return sessionRequest;
}

export async function api<T = any>(path: string, method = 'GET', body?: unknown): Promise<T> {
  try {
    if (method !== 'GET' && !csrfToken) await getSession();
    const headers: Record<string, string> = {};
    if (method !== 'GET') headers['X-CSRF-Token'] = csrfToken;
    if (body !== undefined && !(body instanceof FormData)) headers['Content-Type'] = 'application/json';
    const response = await fetch('/api' + path, { method, credentials: 'same-origin', headers,
      body: body === undefined ? undefined : body instanceof FormData ? body : JSON.stringify(body) });
    const raw = await response.text();
    let data;
    try { data = raw ? JSON.parse(raw, decodeDates) : null; }
    catch { throw new Error('Resposta inesperada do servidor. Verifique se a API está funcionando.'); }
    if (!response.ok) throw new Error(data?.error || 'Não foi possível concluir a operação.');
    if (path === '/auth/logout' || (path === '/auth/me' && method === 'DELETE')) csrfToken = '';
    if (method !== 'GET') window.dispatchEvent(new Event('data-changed'));
    return data;
  } catch (error) { notifyError(error); throw error; }
}

export function queryString(params: Record<string, unknown>) {
  const result = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => { if (value !== undefined && value !== null && value !== '') result.set(key, String(value)); });
  return result.toString();
}
