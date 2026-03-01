import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { useLanguage } from '../hooks/useLanguage';

const REQUIRED_COLUMNS = ['date', 'product_name', 'quantity_sold', 'price', 'revenue'];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export function UploadData() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string[][]>([]);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const { language, setLanguage, t } = useLanguage();

  const validateCSV = (content: string): { valid: boolean; error?: string; preview?: string[][] } => {
    const lines = content.trim().split('\n');
    if (lines.length < 2) {
      return { valid: false, error: t('errorInvalidCSV') };
    }

    // Normalize headers to lowercase for case-insensitive comparison
    const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
    const missingColumns = REQUIRED_COLUMNS.filter(col => !headers.includes(col));
    
    if (missingColumns.length > 0) {
      return { valid: false, error: `${t('errorMissingColumns')}: ${missingColumns.join(', ')}` };
    }

    const previewRows = lines.slice(0, 6).map(line => line.split(',').map(cell => cell.trim()));
    return { valid: true, preview: previewRows };
  };

  const handleFile = (selectedFile: File) => {
    setError('');
    setPreview([]);

    if (!selectedFile.name.endsWith('.csv')) {
      setError(t('errorInvalidCSV'));
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError(t('errorLargeFile'));
    }

    setFile(selectedFile);

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      const validation = validateCSV(content);
      
      if (!validation.valid) {
        setError(validation.error || t('errorInvalidCSV'));
        setFile(null);
      } else {
        setPreview(validation.preview || []);
      }
    };
    reader.readAsText(selectedFile);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setError('');

    try {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const csvText = e.target?.result as string;
        
        try {
          const response = await api.post('/generate-insights', {
            csv_text: csvText,
            language
          });

          localStorage.setItem('lastInsights', JSON.stringify(response.data));
          localStorage.setItem('lastFilename', file.name);
          localStorage.setItem('lastLanguage', language);
          localStorage.setItem('lastAnalysisTime', Date.now().toString());

          // Trigger storage event for same-window refresh
          window.dispatchEvent(new Event('storage'));
          
          // Force navigation with state to trigger refresh
          setTimeout(() => {
            navigate('/', { replace: true, state: { refresh: Date.now() } });
          }, 100);
        } catch (err: any) {
          setError(err?.response?.data?.message || t('errorInvalidCSV'));
        } finally {
          setLoading(false);
        }
      };
      reader.readAsText(file);
    } catch (err) {
      setError(t('errorInvalidCSV'));
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 page-transition">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{t('uploadTitle')}</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          {t('uploadSubtitle')}
        </p>
      </div>

      {/* Language Selector */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-lg hover-lift">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          {t('outputLanguage')}
        </label>
        <select
          value={language}
          onChange={e => setLanguage(e.target.value as any)}
          className="w-full sm:w-auto px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 transition-all"
        >
          <option value="en">English 🇮🇳</option>
          <option value="hi">हिंदी 🇮🇳</option>
          <option value="mr">मराठी 🇮🇳</option>
        </select>
      </div>

      {/* Upload Area */}
      <div
        className={`bg-white dark:bg-gray-800 rounded-xl p-8 border-2 border-dashed transition-all shadow-lg ${
          dragActive
            ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20 scale-105'
            : 'border-gray-300 dark:border-gray-600 hover:border-indigo-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <div className="text-center">
          <div className="text-6xl mb-4 animate-float">📤</div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {t('dropFile')}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            {t('orClickBrowse')}
          </p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={e => e.target.files && handleFile(e.target.files[0])}
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold px-6 py-2 rounded-lg transition-all transform hover:scale-105"
          >
            {t('browseFiles')}
          </button>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-4">
            {t('requiredColumns')}
          </p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 animate-slide-up">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <p className="text-red-800 dark:text-red-200">{error}</p>
          </div>
        </div>
      )}

      {/* File Info + Preview */}
      {file && preview.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 space-y-4 shadow-lg animate-slide-up">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                <span>✅</span>
                {file.name}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {(file.size / 1024).toFixed(2)} KB
              </p>
            </div>
            <button
              onClick={() => {
                setFile(null);
                setPreview([]);
                setError('');
              }}
              className="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 text-sm font-medium transition-colors"
            >
              {t('remove')}
            </button>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">{t('preview')}</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    {preview[0]?.map((header, i) => (
                      <th key={i} className="text-left py-2 px-3 font-semibold text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700/50">
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {preview.slice(1).map((row, i) => (
                    <tr key={i} className="border-b border-gray-100 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
                      {row.map((cell, j) => (
                        <td key={j} className="py-2 px-3 text-gray-700 dark:text-gray-300">
                          {cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-semibold px-6 py-3 rounded-lg transition-all transform hover:scale-105 disabled:hover:scale-100 shadow-lg"
          >
            {loading ? `⏳ ${t('analyzing')}` : `🚀 ${t('analyzeData')}`}
          </button>
        </div>
      )}

      {/* Success Message */}
      {loading && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 animate-slide-up">
          <div className="flex items-center gap-3">
            <div className="animate-spin text-2xl">⚙️</div>
            <div className="flex-1">
              <h3 className="font-semibold text-blue-800 dark:text-blue-200">
                {t('analyzing')}
              </h3>
              <p className="text-sm text-blue-700 dark:text-blue-300">
                {language === 'en' 
                  ? 'Analyzing your data with AI... This may take 10-30 seconds.'
                  : language === 'hi'
                  ? 'AI के साथ आपके डेटा का विश्लेषण कर रहे हैं... इसमें 10-30 सेकंड लग सकते हैं।'
                  : 'AI सह तुमच्या डेटाचे विश्लेषण करत आहोत... यास 10-30 सेकंद लागू शकतात.'}
              </p>
              <div className="mt-2 w-full bg-blue-200 dark:bg-blue-800 rounded-full h-2">
                <div className="bg-blue-600 dark:bg-blue-400 h-2 rounded-full animate-pulse" style={{width: '70%'}}></div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
