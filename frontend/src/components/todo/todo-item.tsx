import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiRequest } from '@/lib/api-client';
import { Todo } from '@/types/todo';
import { useState } from 'react';
import TodoForm from '@/components/todo/todo-form';

interface Props {
  todo: Todo;
}

export default function TodoItem({ todo }: Props) {
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);

  const toggleMutation = useMutation(
    () =>
      apiRequest(`/api/v1/todos/${todo.id}`, {
        method: 'PUT',
        body: { is_completed: !todo.is_completed },
      }),
    {
      onSuccess: () => queryClient.invalidateQueries(['todos']),
    }
  );

  const deleteMutation = useMutation(
    () => apiRequest(`/api/v1/todos/${todo.id}`, { method: 'DELETE' }),
    {
      onSuccess: () => queryClient.invalidateQueries(['todos']),
    }
  );

  const handleToggle = () => {
    toggleMutation.mutate();
  };

  const handleDelete = () => {
    if (confirm('Delete this todo?')) {
      deleteMutation.mutate();
    }
  };

  const handleEdit = (data: { title: string }) => {
    apiRequest(`/api/v1/todos/${todo.id}`, { method: 'PUT', body: data })
      .then(() => {
        queryClient.invalidateQueries(['todos']);
        setIsEditing(false);
      })
      .catch((err) => console.error('Update failed', err));
  };

  return (
    <div className="flex items-center justify-between p-3 border rounded bg-white hover:shadow">
      <div className="flex items-center space-x-2">
        <button
          aria-label={todo.is_completed ? 'Mark as incomplete' : 'Mark as complete'}
          onClick={handleToggle}
          disabled={toggleMutation.isLoading}
          className={todo.is_completed ? 'text-green-600' : 'text-gray-600'}
        >
          {todo.is_completed ? '✅' : '⬜'}
        </button>
        <span className={todo.is_completed ? 'line-through text-gray-500' : ''}>{todo.title}</span>
      </div>
      <div className="flex items-center space-x-1">
        <button aria-label="Edit" onClick={() => setIsEditing(true)} className="text-blue-600">
          ✏️
        </button>
        <button aria-label="Delete" onClick={handleDelete} className="text-red-600" disabled={deleteMutation.isLoading}>
          🗑️
        </button>
      </div>
      {isEditing && (
        <div className="mt-2 w-full">
          <TodoForm defaultValues={{ title: todo.title }} onSubmit={handleEdit} loading={false} />
        </div>
      )}
    </div>
  );
}
