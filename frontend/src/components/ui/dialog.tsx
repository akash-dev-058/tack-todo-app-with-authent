import { ReactNode, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { XIcon } from '@/components/ui/icons';
import Button from '@/components/ui/button';

interface Props {
  children: ReactNode;
  title: string;
  onClose: () => void;
}

export default function Dialog({ children, title, onClose }: Props) {
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [onClose]);

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === overlayRef.current) onClose();
  };

  return createPortal(
    <div
      ref={overlayRef}
      onClick={handleOverlayClick}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
    >
      <div className="bg-white rounded-lg shadow-lg max-w-md w-full p-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-medium">{title}</h2>
          <Button variant="ghost" onClick={onClose} aria-label="Close dialog">
            <XIcon />
          </Button>
        </div>
        {children}
      </div>
    </div>,
    document.body
  );
}
