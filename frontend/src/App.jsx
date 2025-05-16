import { useState } from 'react';
import axios from 'axios';

import URLInput from './components/URLInput';
import ImageGrid from './components/ImageGrid';
import ErrorList from './components/ErrorList';

function App() {
  const [urls, setUrls] = useState([]);
  const [results, setResults] = useState({});
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(urlArray) {
    setUrls(urlArray);
    setLoading(true);
    setResults({});
    setErrors([]);

    try {
      const response = await axios.post('https://hackthehaze.onrender.com/scrape', { urls: urlArray });
      const data = response.data;
      setResults(data.results || {});
      setErrors(data.errors || []);
    } catch (error) {
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

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-12 transition-all hover:shadow-2xl">
          <URLInput onSubmit={handleSubmit} />
        </div>

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

export default App;
