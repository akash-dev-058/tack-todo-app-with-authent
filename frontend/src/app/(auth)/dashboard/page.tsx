import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiRequest } from '@/lib/api-client';
import TodoList from '@/components/todo/todo-list';
import TodoForm from '@/components/todo/todo-form';
import { useRealtimeTodos } from '@/hooks/use-realtime-todos';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/auth-context';

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const queryClient = useQueryClient();

  const {
    data: todos,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery(['todos'], () => apiRequest('/api/v1/todos'));

  const createMutation = useMutation(
    (newTodo: { title: string }) => apiRequest('/api/v1/todos', { method: 'POST', body: newTodo }),
    {
      onSuccess: () => queryClient.invalidateQueries(['todos']),
    }
  );

  useRealtimeTodos();

  if (authLoading) {
    return (
      <div className="flex justify-center items-center h-64" role="status" aria-live="polite">
        <div className="animate-pulse text-gray-500">Loading user…</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="text-center mt-10">
        <p className="text-lg">You must be logged in to view this page.</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="h-12 bg-gray-200 rounded animate-pulse" />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center text-red-600" role="alert">
        <p>Failed to load todos.</p>
        <button className="mt-2 px-4 py-2 bg-primary text-white rounded" onClick={() => refetch()}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <h1 className="text-2xl font-bold mb-4">Your Todos</h1>
      <TodoForm onSubmit={(data) => createMutation.mutate(data)} loading={createMutation.isLoading} />
      {todos && todos.length > 0 ? (
        <TodoList todos={todos} />
      ) : (
        <div className="text-center py-10 text-gray-500">
          <p className="mb-4">No todos yet. Add one above!</p>
          <button className="px-4 py-2 bg-secondary text-white rounded" onClick={() => document.getElementById('todo-title')?.focus()}>
            Add Todo
          </button>
        </div>
      )}
    </motion.div>
  );
}
