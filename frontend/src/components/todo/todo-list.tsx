import TodoItem from '@/components/todo/todo-item';
import { Todo } from '@/types/todo';
import { motion, AnimatePresence } from 'framer-motion';

interface Props {
  todos: Todo[];
}

export default function TodoList({ todos }: Props) {
  return (
    <ul className="space-y-2" role="list">
      <AnimatePresence>
        {todos.map((todo) => (
          <motion.li
            key={todo.id}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.15 }}
          >
            <TodoItem todo={todo} />
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  );
}
