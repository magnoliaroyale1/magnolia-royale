import { useEffect, useState } from 'react';
import { Alert } from 'react-bootstrap';

export function ApiNotice() {
  const [message, setMessage] = useState('');
  useEffect(() => {
    const listener = (event: Event) => setMessage((event as CustomEvent<string>).detail);
    window.addEventListener('api-error', listener);
    return () => window.removeEventListener('api-error', listener);
  }, []);
  if (!message) return null;
  return <Alert variant="danger" role="alert" dismissible onClose={() => setMessage('')} className="position-fixed shadow" style={{ top: 90, left: '5%', right: '5%', zIndex: 2000 }}>{message}</Alert>;
}
