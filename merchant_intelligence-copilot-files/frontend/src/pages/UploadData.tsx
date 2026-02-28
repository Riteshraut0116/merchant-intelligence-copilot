import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';

const REQUIRED_COLUMNS = ['date', 'product_name', 'quantity_sold', 'price', 'revenue'];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export function UploadData() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string[][]>([]);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState(() => localStorage.getItem('lastLanguage') || 'en');
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const validateCSV = (content: string): { valid: boolean; error?: string; preview?: string[][] } => {
    const lines = content.trim().split('\n');
    if (lines.length < 2) {
      return { valid: false, error: 'CSV file must have at least a header row and one data row' };
    }

    const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
    const missingColumns = REQUIRED_COLUMNS.filter(col => !headers.includes(col));
    
    if (missingColumns.length > 0) {
      return { valid: false, error: `Missing required columns: ${missingColumns.join(', ')}` };
    }

    const previewRows = lines.slice(0, 6).map(line => line.split(',').map(cell => cell.trim()));
    return { valid: true, preview: previewRows };
  };

  const handleFile = (selectedFile: File) => {
    setError('');
    setPreview([]);

    if (!selectedFile.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError('File size exceeds 10MB. Large files may take longer to process.');
    }

    setFile(selectedFile);

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      const validation = validateCSV(content);
      
      if (!validation.valid) {
        setError(validation.error || 'Invalid CSV format');
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

          navigate('/');
        } catch (err: any) {
          setError(err?.response?.data?.message || 'Failed to analyze data. Please check your API connection.');
        } finally {
          setLoading(false);
        }
      };
      reader.readAsText(file);
    } catch (err) {
      setError('Failed to read file');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Upload Sales Data</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Upload your CSV file with sales history to generate AI-powered insights
        </p>
      </div>

      {/* Language Selector */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Output Language
        </label>
        <select
          value={language}
          onChange={e => setLanguage(e.target.value)}
          className="w-full sm:w-auto px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        >
          <option value="en">English</option>
          <option value="hi">Hindi (हिंदी)</option>
          <option value="mr">Marathi (मराठी)</option>
        </select>
      </div>

      {/* Upload Area */}
      <div
        className={`bg-white dark:bg-gray-800 rounded-xl p-8 border-2 border-dashed transition-colors ${
          dragActive
            ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20'
            : 'border-gray-300 dark:border-gray-600'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <div className="text-center">
          <div className="text-6xl mb-4">📤</div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Drop your CSV file here
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            or click to browse
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
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-2 rounded-lg transition-colors"
          >
            Browse Files
          </button>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-4">
            Required columns: date, product_name, quantity_sold, price, revenue
          </p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">{error}</p>
        </div>
      )}

      {/* File Info + Preview */}
      {file && preview.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white">{file.name}</h3>
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
              className="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 text-sm font-medium"
            >
              Remove
            </button>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">Preview (first 5 rows)</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    {preview[0]?.map((header, i) => (
                      <th key={i} className="text-left py-2 px-3 font-semibold text-gray-700 dark:text-gray-300">
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {preview.slice(1).map((row, i) => (
                    <tr key={i} className="border-b border-gray-100 dark:border-gray-700/50">
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
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold px-6 py-3 rounded-lg transition-colors"
          >
            {loading ? 'Analyzing...' : 'Analyze Data'}
          </button>
        </div>
      )}
    </div>
  );
}
