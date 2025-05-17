import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';
import axios from 'axios';

export default function AuthDebugger() {
  const { user } = useAuth();
  const [token, setToken] = useState(null);
  const [authCheckResult, setAuthCheckResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function getToken() {
      try {
        const { data } = await supabase.auth.getSession();
        setToken(data.session?.access_token || null);
      } catch (err) {
        console.error("Error getting token:", err);
      }
    }
    
    getToken();
  }, [user]);

  const testAuth = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get('https://hackthehaze.onrender.com/auth-check', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      setAuthCheckResult(response.data);
    } catch (err) {
      setError(err.message);
      console.error("Auth check error:", err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Authentication Debugger</h2>
      
      <div className="mb-4">
        <h3 className="text-lg font-medium mb-2">Current User</h3>
        {user ? (
          <div className="bg-gray-100 p-3 rounded">
            <p><strong>ID:</strong> {user.id}</p>
            <p><strong>Email:</strong> {user.email}</p>
          </div>
        ) : (
          <p className="text-red-500">Not authenticated</p>
        )}
      </div>
      
      <div className="mb-4">
        <h3 className="text-lg font-medium mb-2">Authentication Token</h3>
        {token ? (
          <div className="bg-gray-100 p-3 rounded">
            <p className="text-xs overflow-auto whitespace-normal break-all">{token}</p>
          </div>
        ) : (
          <p className="text-red-500">No token available</p>
        )}
      </div>
      
      <button 
        onClick={testAuth}
        disabled={loading || !token}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Testing...' : 'Test Authentication'}
      </button>
      
      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          <p><strong>Error:</strong> {error}</p>
        </div>
      )}
      
      {authCheckResult && (
        <div className="mt-4">
          <h3 className="text-lg font-medium mb-2">Authentication Check Result</h3>
          <pre className="bg-gray-100 p-3 rounded overflow-auto">
            {JSON.stringify(authCheckResult, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
