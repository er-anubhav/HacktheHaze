import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useState } from 'react';
import { Menu, X, LogOut, History, Home } from 'lucide-react';

export default function Navbar() {
  const { user, signOut } = useAuth();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const NavLink = ({ to, children, icon: Icon }) => {
    const isActive = location.pathname === to;
    
    return (
      <Link
        to={to}
        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
          isActive 
            ? 'bg-blue-100 text-blue-700' 
            : 'hover:bg-gray-100 text-gray-700 hover:text-blue-600'
        }`}
      >
        {Icon && <Icon size={18} />}
        {children}
      </Link>
    );
  };

  const handleSignOut = async () => {
    await signOut();
  };

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <span className="text-2xl font-bold text-blue-600">HackTheHaze</span>
            </Link>
          </div>

          {/* Desktop menu */}
          <div className="hidden sm:ml-6 sm:flex sm:items-center sm:space-x-2">
            {user && (
              <>
                <NavLink to="/" icon={Home}>Home</NavLink>
                <NavLink to="/history" icon={History}>Scrape History</NavLink>
                <button
                  onClick={handleSignOut}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-red-600 transition-colors"
                >
                  <LogOut size={18} />
                  Sign Out
                </button>
                <div className="ml-4 px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                  {user.email}
                </div>
              </>
            )}
            
            {!user && (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center sm:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-100 focus:outline-none"
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="sm:hidden">
          <div className="pt-2 pb-4 space-y-1">
            {user ? (
              <>
                <div className="px-4 py-2 text-sm font-medium text-gray-500">
                  {user.email}
                </div>
                <Link
                  to="/"
                  className="block px-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-100"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Home
                </Link>
                <Link
                  to="/history"
                  className="block px-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-100"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Scrape History
                </Link>
                <button
                  onClick={handleSignOut}
                  className="block w-full text-left px-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-100"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="block px-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-100"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  className="block px-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-100"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
