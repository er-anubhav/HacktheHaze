import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';

// Components
import URLInput from './components/URLInput';
import ImageGrid from './components/ImageGrid';
import ErrorList from './components/ErrorList';
import Navbar from './components/Nav/Navbar';
import Login from './components/Auth/Login';
import SignUp from './components/Auth/SignUp';
import History from './components/History/History';
import AuthDebugger from './components/Debug/AuthDebugger';

// Context
import { AuthProvider, useAuth } from './contexts/AuthContext';

// Supabase
import { saveHistory, supabase } from './lib/supabase';

function HomePage() {
  const [urls, setUrls] = useState([]);
  const [results, setResults] = useState({});
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  async function handleSubmit(urlArray) {
    if (!user) {
      // Redirect to login if not authenticated
      return;
    }
    
    setUrls(urlArray);
    setLoading(true);
    setResults({});
    setErrors([]);

    try {
      // Get current session to retrieve token
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;
      
      // Include token in Authorization header
      const response = await axios.post(
        'https://hackthehaze.onrender.com/scrape', 
        { urls: urlArray },
        { 
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      const data = response.data;
      setResults(data.results || {});
      setErrors(data.errors || []);
      
      // Save to history if results found
      if (data.results && Object.keys(data.results).length > 0) {
        const totalImages = Object.values(data.results).reduce(
          (sum, images) => sum + images.length, 0
        );
        
        await saveHistory(user.id, urlArray, totalImages);
      }
    } catch (error) {
      console.error("API Error:", error.response?.status, error.response?.data || error.message);
      setErrors([{ url: 'General', error: error.message }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="font-serif min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-purple-900 transition-colors duration-300">
      <div className="w-full px-6 py-12 max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-black text-transparent bg-clip-text text-white mb-4">
            Image Scraper
          </h1>
          <p className="text-gray-600 dark:text-gray-300 text-xl max-w-2xl mx-auto">
            Enter website URLs below to extract and view all images.
          </p>
        </div>

        {!user ? (
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 text-center">
            <h2 className="text-xl font-bold mb-4">Sign in to continue</h2>
            <p className="mb-6 text-gray-600 dark:text-gray-300">
              You need to sign in to use the image scraper and save your history.
            </p>
            <div className="flex justify-center space-x-4">
              <a 
                href="/login" 
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                Sign In
              </a>
              <a 
                href="/signup" 
                className="px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition"
              >
                Sign Up
              </a>
            </div>
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-12 transition-all hover:shadow-2xl">
            <URLInput onSubmit={handleSubmit} />
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-blue-500"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-300 font-medium">Fetching images...</p>
          </div>
        )}

        {!loading && Object.keys(results).length > 0 && (
          <div className="mt-8">
            <ImageGrid results={results} />
          </div>
        )}

        {!loading && errors.length > 0 && (
          <div className="mt-8">
            <ErrorList errors={errors} />
          </div>
        )}
      </div>
    </div>
  );
}

// Protected route component
function ProtectedRoute({ children }) {
  const { user, isLoading } = useAuth();
  
  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-blue-500"></div>
      </div>
    );
  }
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  return children;
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-grow">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<SignUp />} />
              <Route 
                path="/history" 
                element={
                  <ProtectedRoute>
                    <History />
                  </ProtectedRoute>
                } 
              />
              <Route path="/debug" element={<AuthDebugger />} />
              <Route path="/" element={<HomePage />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
