import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  title: z.string().min(1, { message: 'Title cannot be empty' }).max(200, { message: 'Title too long' }),
});

type FormData = z.infer<typeof schema>;

interface Props {
  onSubmit: (data: FormData) => void;
  defaultValues?: Partial<FormData>;
  loading: boolean;
}

export default function TodoForm({ onSubmit, defaultValues, loading }: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues,
  });

  const submit = (data: FormData) => {
    onSubmit(data);
    reset();
  };

  return (
    <form onSubmit={handleSubmit(submit)} className="flex space-x-2" noValidate>
      <input
        id="todo-title"
        placeholder="What needs to be done?"
        {...register('title')}
        aria-invalid={!!errors.title}
        className="flex-1 border rounded px-2 py-1"
      />
      <button type="submit" disabled={loading} className="px-4 py-1 bg-blue-600 text-white rounded">
        {loading ? 'Saving…' : 'Add'}
      </button>
      {errors.title && (
        <p className="mt-1 text-sm text-red-600" role="alert">
          {errors.title.message}
        </p>
      )}
    </form>
  );
}
