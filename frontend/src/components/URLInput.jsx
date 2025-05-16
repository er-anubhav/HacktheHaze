import React, { useState } from 'react';

export default function URLInput({ onSubmit }) {
  const [input, setInput] = useState('');
  const [isHovered, setIsHovered] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    let urls = input.split(/[\n,]+/).map(url => url.trim()).filter(url => url !== '');
    onSubmit(urls);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="relative">
        <textarea
          rows={5}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter URLs separated by commas or new lines"
          className="w-full p-5 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-800 text-gray-800 dark:text-white focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all shadow-sm font-medium"
        />
        <div className="absolute inset-0 rounded-xl pointer-events-none bg-gradient-to-r from-blue-500/5 to-purple-500/5 opacity-0 transition-opacity duration-300 hover:opacity-100"></div>
      </div>
      
      <button
        type="submit"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className={`w-full py-4 px-6 rounded-xl text-lg relative overflow-hidden transition-all duration-300 ${
          isHovered ? 'shadow-lg shadow-blue-500/20' : 'shadow-md'
        }`}
        style={{
          background: 'linear-gradient(90deg,rgb(251, 253, 255), #8b5cf6)',
          transform: isHovered ? 'translateY(-2px)' : 'none',
        }}
      >
        <div className="relative z-10 flex items-center justify-center gap-2">
          <span className="text-xl">🚀</span>
          <span>Scrape Images</span>
        </div>
        <div 
          className={`absolute inset-0 transition-opacity duration-300 ${
            isHovered ? 'opacity-100' : 'opacity-0'
          }`}
          style={{ 
            background: 'linear-gradient(90deg,rgb(244, 244, 244), #7c3aed)',
          }}
        ></div>
      </button>
      
      <div className="text-sm text-white text-center mt-2">
        Paste website URLs to scrape images from those sites
      </div>
    </form>
  );
}
