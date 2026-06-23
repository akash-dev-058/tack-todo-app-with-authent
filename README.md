# AuthTodoPro Frontend

A production‑ready Todo application built with **Next.js 14**, **TypeScript**, **Tailwind CSS**, **TanStack Query**, and **Zod**.

## Features
- Secure authentication (JWT stored in HttpOnly cookies)
- Real‑time task sync via Server‑Sent Events
- Optimistic UI updates with TanStack Query
- Accessible, responsive UI built with Tailwind
- Form validation with React Hook Form + Zod
- Global error handling and loading skeletons

## Getting Started
bash
# Clone the repo
git clone <repo-url>
cd auth-todo-pro/frontend

# Install dependencies
npm ci

# Set environment variables
cp .env.example .env.local
# Edit .env.local if needed

# Run the development server
npm run dev


The app will be available at `http://localhost:3000` and expects the backend API at `http://localhost:8000`.

## Scripts
- `npm run dev` – Start Next.js in development mode
- `npm run build` – Create an optimized production build
- `npm start` – Run the production build
- `npm run lint` – Lint the codebase
- `npm run type-check` – Run TypeScript type checking

## Architecture Overview
- **src/app** – Next.js App Router pages and layout
- **src/context** – Authentication context provider
- **src/lib** – API client and SSE client utilities
- **src/hooks** – Custom React hooks (auth, realtime)
- **src/components** – UI primitives and feature components
- **src/components/providers** – React Query provider

## License
MIT
