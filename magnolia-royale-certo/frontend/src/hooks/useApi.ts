import { useCallback, useEffect, useRef, useState } from 'react';
import { api } from '../services/api';

export function useApiResource<T>(path: string | null, initial: T, polling = false) {
  const initialRef = useRef(initial);
  const [data, setData] = useState<T>(initial);
  const [loading, setLoading] = useState(Boolean(path));
  const [error, setError] = useState('');
  const generation = useRef(0);
  const refetch = useCallback(async () => {
    const current = ++generation.current;
    if (!path) { setData(initialRef.current); setLoading(false); return; }
    try {
      const value = await api<T>(path);
      if (current === generation.current) { setData(value); setError(''); }
    } catch (e) { if (current === generation.current) setError((e as Error).message); }
    finally { if (current === generation.current) setLoading(false); }
  }, [path]);
  useEffect(() => {
    setLoading(Boolean(path)); setData(initialRef.current); void refetch();
    const reload = () => { void refetch(); };
    window.addEventListener('data-changed', reload);
    const timer = polling && path ? window.setInterval(reload, 5000) : undefined;
    return () => { ++generation.current; window.removeEventListener('data-changed', reload); if (timer) window.clearInterval(timer); };
  }, [refetch, path, polling]);
  return { data, loading, error, refetch };
}

export function useAction<A extends unknown[], R>(work: (...args: A) => Promise<R>, fallback: R) {
  const [loading, setLoading] = useState(false);
  const latest = useRef(work); latest.current = work;
  const run = useCallback(async (...args: A): Promise<R> => {
    setLoading(true);
    try { return await latest.current(...args); } catch { return fallback; } finally { setLoading(false); }
  }, [fallback]);
  return { run, loading };
}
