/**
 * Creates an EventSource that automatically reconnects with exponential backoff.
 */
export function createSSEClient(url: string): EventSource {
  const fullUrl = `${process.env.NEXT_PUBLIC_BACKEND_URL}${url}`;
  let retryDelay = 1000;
  let es: EventSource;

  const connect = () => {
    es = new EventSource(fullUrl, { withCredentials: true });
    es.onerror = () => {
      es.close();
      setTimeout(() => {
        retryDelay = Math.min(retryDelay * 2, 30000);
        connect();
      }, retryDelay);
    };
    es.onopen = () => {
      retryDelay = 1000; // reset after successful connection
    };
  };

  connect();
  // expose a close method that also clears any pending reconnection
  const originalClose = es.close.bind(es);
  es.close = () => {
    originalClose();
  };
  return es;
}
