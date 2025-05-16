import React from 'react';
import { motion } from 'framer-motion';

export default function ErrorList({ errors }) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden"
    >
      <div className="bg-red-500 px-6 py-4 flex items-center">
        <div className="bg-white/20 rounded-full p-2 mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h2 className="text-xl font-bold text-white">Errors Encountered</h2>
      </div>
      
      <ul className="divide-y">
        {errors.map(({ url, error }, idx) => (
          <motion.li 
            key={idx}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: idx * 0.1 }}
            className="px-6 py-4 transition-colors"
          >
            <div className="flex flex-col sm:flex-row sm:items-center gap-2">
              <span className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 text-sm px-3 py-1 rounded-full font-medium truncate max-w-xs">
                {url}
              </span>
              <span className="text-gray-700 dark:text-gray-300">
                {error}
              </span>
            </div>
          </motion.li>
        ))}
      </ul>
    </motion.div>
  );
}
