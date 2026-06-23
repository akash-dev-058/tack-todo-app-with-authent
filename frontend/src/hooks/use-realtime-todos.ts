import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { createSSEClient } from '@/lib/sse-client';

/**
 * Hook that connects to the backend SSE endpoint and invalidates the todo list
 * query whenever a change event is received.
 */
export function useRealtimeTodos() {
  const queryClient = useQueryClient();

  useEffect(() => {
    const sse = createSSEClient('/api/v1/events');
    const handleMessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'todo_updated') {
          queryClient.invalidateQueries(['todos']);
        }
      } catch (err) {
        console.error('Failed to parse SSE message', err);
      }
    };
    sse.addEventListener('message', handleMessage);
    return () => {
      sse.removeEventListener('message', handleMessage);
      sse.close();
    };
  }, [queryClient]);
}
