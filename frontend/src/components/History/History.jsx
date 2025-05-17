import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { getUserHistory } from '../../lib/supabase';
import { ExternalLink, Calendar, Image } from 'lucide-react';

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchHistory = async () => {
      if (!user) return;
      
      try {
        setLoading(true);
        const { data, error } = await getUserHistory(user.id);
        
        if (error) {
          throw error;
        }
        
        setHistory(data || []);
      } catch (err) {
        console.error('Error fetching history:', err);
        setError('Failed to load history data');
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [user]);

  const formatDate = (dateString) => {
    const options = {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-red-50 p-4 rounded-lg text-red-700">
          <p>{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-2 px-4 py-2 bg-red-100 hover:bg-red-200 rounded-lg transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Your Scrape History</h1>
        <p className="text-gray-600 mt-2">Here's a record of your previous scraping activities</p>
      </div>

      {history.length === 0 ? (
        <div className="bg-white p-8 rounded-xl shadow-sm text-center">
          <h3 className="text-xl font-medium text-gray-700 mb-4">No history found</h3>
          <p className="text-gray-500 mb-6">You haven't scraped any images yet.</p>
          <Link 
            to="/" 
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Start Scraping
          </Link>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {history.map((record) => (
            <div key={record.id} className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
              <div className="border-b p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <Calendar size={16} />
                    <span>{formatDate(record.created_at)}</span>
                  </div>
                  <div className="flex items-center gap-1 bg-blue-50 text-blue-700 px-2 py-1 rounded-full text-sm">
                    <Image size={14} />
                    <span>{record.image_count} images</span>
                  </div>
                </div>
              </div>
              
              <div className="p-4">
                <h3 className="font-medium text-gray-800 mb-2">URLs Scraped:</h3>
                <ul className="space-y-2">
                  {record.urls.map((url, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <ExternalLink size={16} className="flex-shrink-0 mt-1 text-gray-400" />
                      <a 
                        href={url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm truncate"
                        title={url}
                      >
                        {url}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
