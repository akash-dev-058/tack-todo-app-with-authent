"use client";
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useAuth } from '@/context/auth-context';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/button';
import Input from '@/components/ui/input';

const schema = z.object({
  name: z.string().min(2).optional(),
  email: z.string().email(),
  password: z.string().min(8)
});

type FormData = z.infer<typeof schema>;

export default function RegisterPage() {
  const { register: registerUser, loading } = useAuth();
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    try {
      await registerUser(data.email, data.password, data.name);
      router.push('/dashboard');
    } catch (err) {
      console.error('Registration error', err);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-6 border rounded shadow-sm bg-white">
      <h2 className="text-2xl font-semibold mb-4 text-center">Create Account</h2>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="mb-4">
          <label htmlFor="name" className="block text-sm font-medium mb-1">Name (optional)</label>
          <Input id="name" type="text" {...register('name')} aria-invalid={!!errors.name} />
          {errors.name && <p className="mt-1 text-sm text-red-600" role="alert">{errors.name.message}</p>}
        </div>
        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium mb-1">Email</label>
          <Input id="email" type="email" {...register('email')} aria-invalid={!!errors.email} />
          {errors.email && <p className="mt-1 text-sm text-red-600" role="alert">{errors.email.message}</p>}
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block text-sm font-medium mb-1">Password</label>
          <Input id="password" type="password" {...register('password')} aria-invalid={!!errors.password} />
          {errors.password && <p className="mt-1 text-sm text-red-600" role="alert">{errors.password.message}</p>}
        </div>
        <Button type="submit" disabled={loading} className="w-full">{loading ? 'Creating…' : 'Create Account'}</Button>
      </form>
      <p className="mt-4 text-center text-sm">
        Already have an account? <a href="/login" className="text-primary hover:underline">Login</a>
      </p>
    </div>
  );
}
