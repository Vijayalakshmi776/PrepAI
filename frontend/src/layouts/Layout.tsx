import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { Navbar } from '../components/Navbar';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-background text-primary-text">
      <Navbar />
      <motion.main
        className="mx-auto w-full max-w-7xl px-4 pb-16 pt-8 sm:px-6 lg:px-8"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -12 }}
        transition={{ duration: 0.35 }}
      >
        {children}
      </motion.main>
    </div>
  );
}
