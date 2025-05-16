import { useEffect, useState } from 'react';
import { useTransition, animated } from '@react-spring/web';

function Masonry({ data, onClick }) {
  const [mounted, setMounted] = useState(false);
  const [columns, setColumns] = useState(5);

  // Responsive column count based on viewport width
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 640) {
        setColumns(2);
      } else if (window.innerWidth < 768) {
        setColumns(3);
      } else if (window.innerWidth < 1024) {
        setColumns(4);
      } else {
        setColumns(5);
      }
    };

    handleResize(); // Set initial value
    window.addEventListener('resize', handleResize);
    
    const timeout = setTimeout(() => setMounted(true), 50);
    return () => {
      clearTimeout(timeout);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const transitions = useTransition(data, {
    keys: (item) => item.id,
    from: { opacity: 0, transform: 'translateY(30px)' },
    enter: { opacity: 1, transform: 'translateY(0)' },
    leave: { opacity: 0, transform: 'translateY(-30px)' },
    config: { mass: 5, tension: 500, friction: 100 },
    trail: 25,
  });

  return (
    <div
      className={`w-full px-4 transition-opacity duration-700 ease-in ${
        mounted ? 'opacity-100' : 'opacity-0'
      }`}
      style={{
        columnCount: columns,
        columnGap: '1rem',
      }}
    >
      {transitions((style, item) => (
        <animated.div
          key={item.id}
          style={style}
          className="mb-4 break-inside-avoid group relative overflow-hidden rounded-xl"
          onClick={() => onClick && onClick(item.image)}
        >
          <div className="relative overflow-hidden  rounded-xl shadow-lg">
            <img
              src={item.image}
              alt=""
              className="w-full h-auto object-cover rounded-xl transition-transform duration-500 ease-in-out group-hover:scale-105"
              style={{
                backgroundColor: 'rgba(0,0,0,0.03)',
              }}
              loading="lazy"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="absolute bottom-0 left-0 right-0 p-3 text-white transform translate-y-full group-hover:translate-y-0 transition-transform duration-300">
              <button className="bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-white/30 transition-colors">
                View
              </button>
            </div>
          </div>
        </animated.div>
      ))}
    </div>
  );
}

export default Masonry;
