import React, { useState, useMemo, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { InsightsData, Product } from '../types';
import { useLanguage } from '../hooks/useLanguage';

export function Dashboard() {
  const [selectedProduct, setSelectedProduct] = useState<string>('');
  const [explainProduct, setExplainProduct] = useState<Product | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const { t } = useLanguage();
  const location = useLocation();

  // Force refresh when navigating from upload or when localStorage changes
  useEffect(() => {
    const handleStorageChange = () => {
      setRefreshKey(prev => prev + 1);
    };
    
    // Refresh on navigation with state
    if (location.state?.refresh) {
      setRefreshKey(prev => prev + 1);
    }
    
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [location]);

  const storedData = localStorage.getItem('lastInsights');
  const storedFilename = localStorage.getItem('lastFilename');
  const insights: InsightsData | null = useMemo(() => 
    storedData ? JSON.parse(storedData) : null, 
    [storedData, refreshKey]
  );

  const products = useMemo(() => {
    if (!insights) return [];
    
    // Handle multiple possible response structures
    // Direct products array
    if (Array.isArray(insights)) {
      return insights;
    }
    // Nested: insights.insights.products
    if (insights.insights && Array.isArray(insights.insights.products)) {
      return insights.insights.products;
    }
    // Flat: insights.products
    if (Array.isArray(insights.products)) {
      return insights.products;
    }
    
    console.warn('Unexpected insights structure:', insights);
    return [];
  }, [insights, refreshKey]);

  const productsAnalyzed = products.length;
  const alertsCount = products.filter(p => p.anomalies && p.anomalies.length > 0).length;
  const avgConfidence = products.length > 0
    ? Math.round(products.reduce((sum, p) => sum + p.confidence_score, 0) / products.length)
    : 0;
  const topReorder = products.length > 0
    ? [...products].sort((a, b) => (b.reorder?.quantity || 0) - (a.reorder?.quantity || 0))[0]?.product_name || 'N/A'
    : 'N/A';

  const selectedProductData = useMemo(() => {
    if (!selectedProduct) return null;
    return products.find(p => p.product_name === selectedProduct);
  }, [selectedProduct, products]);

  const chartData = useMemo(() => {
    if (!selectedProductData?.forecast) return [];
    return selectedProductData.forecast.map(f => ({
      date: new Date(f.ds).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      forecast: Math.round(f.yhat),
      lower: f.yhat_lower ? Math.round(f.yhat_lower) : undefined,
      upper: f.yhat_upper ? Math.round(f.yhat_upper) : undefined,
    }));
  }, [selectedProductData]);

  const getConfidenceBadge = (score: number) => {
    if (score > 80) return { color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400', label: 'High' };
    if (score >= 60) return { color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400', label: 'Medium' };
    return { color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400', label: 'Low' };
  };

  if (!insights) {
    return (
      <div className="max-w-4xl mx-auto page-transition">
        <div className="bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 rounded-xl p-12 text-center border border-gray-200 dark:border-gray-700 shadow-xl">
          <div className="text-6xl mb-4 animate-float">📊</div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{t('noDataYet')}</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6 flex items-center justify-center gap-2">
            <span>🚀</span>
            {t('uploadToStart')}
            <span>✨</span>
          </p>
          <Link
            to="/upload"
            className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold px-6 py-3 rounded-lg transition-all transform hover:scale-105 shadow-lg"
          >
            <span>📤</span>
            {t('uploadDataBtn')}
            <span>→</span>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6 page-transition">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{t('dashboardTitle')}</h1>
        {storedFilename && (
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {t('uploadTitle')}: {storedFilename}
          </p>
        )}
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-lg p-6 border border-blue-200 dark:border-blue-700 hover:shadow-lg transition-all hover:scale-105">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm font-medium text-blue-600 dark:text-blue-400">{t('productsAnalyzed')}</div>
            <span className="text-2xl">📦</span>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white">{productsAnalyzed}</div>
        </div>
        <div className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 rounded-lg p-6 border border-amber-200 dark:border-amber-700 hover:shadow-lg transition-all hover:scale-105">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm font-medium text-amber-600 dark:text-amber-400">{t('alertsCount')}</div>
            <span className="text-2xl">⚠️</span>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white">{alertsCount}</div>
        </div>
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-lg p-6 border border-green-200 dark:border-green-700 hover:shadow-lg transition-all hover:scale-105">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm font-medium text-green-600 dark:text-green-400">{t('avgConfidence')}</div>
            <span className="text-2xl">✅</span>
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white">{avgConfidence}%</div>
        </div>
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg p-6 border border-purple-200 dark:border-purple-700 hover:shadow-lg transition-all hover:scale-105">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm font-medium text-purple-600 dark:text-purple-400">{t('topReorderItem')}</div>
            <span className="text-2xl">🔝</span>
          </div>
          <div className="text-lg font-bold text-gray-900 dark:text-white truncate">{topReorder}</div>
        </div>
      </div>

      {/* Product Selector + Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-lg">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">{t('forecast7Day')}</h2>
          <select
            value={selectedProduct}
            onChange={e => setSelectedProduct(e.target.value)}
            className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 transition-all"
          >
            <option value="">{t('selectProduct')}</option>
            {products.map(p => (
              <option key={p.product_name} value={p.product_name}>
                {p.product_name}
              </option>
            ))}
          </select>
        </div>

        {selectedProduct && chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="date" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }}
                labelStyle={{ color: '#F3F4F6' }}
              />
              <Legend />
              <Area type="monotone" dataKey="upper" stackId="1" stroke="#6366F1" fill="#6366F1" fillOpacity={0.1} name="Upper Bound" />
              <Area type="monotone" dataKey="forecast" stackId="2" stroke="#6366F1" fill="#6366F1" fillOpacity={0.6} name="Forecast" />
              <Area type="monotone" dataKey="lower" stackId="3" stroke="#6366F1" fill="#6366F1" fillOpacity={0.1} name="Lower Bound" />
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
            {selectedProduct ? 'No forecast data available' : 'Select a product to view forecast'}
          </div>
        )}
      </div>

      {/* Insights Table */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">{t('productInsights')}</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Product</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">{t('confidence')}</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">{t('reorder')}</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">{t('urgency')}</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">{t('alerts')}</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">{t('actions')}</th>
              </tr>
            </thead>
            <tbody>
              {products.map(product => {
                const badge = getConfidenceBadge(product.confidence_score);
                return (
                  <tr key={product.product_name} className="border-b border-gray-100 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
                    <td className="py-3 px-4 font-medium text-gray-900 dark:text-white">{product.product_name}</td>
                    <td className="py-3 px-4">
                      <span className={`inline-block px-2 py-1 rounded text-xs font-semibold ${badge.color}`}>
                        {product.confidence_score}% {badge.label}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-700 dark:text-gray-300">
                      {product.reorder?.quantity || 'N/A'}
                    </td>
                    <td className="py-3 px-4">
                      {product.reorder?.urgency && (
                        <span className={`inline-block px-2 py-1 rounded text-xs font-semibold ${
                          product.reorder.urgency === 'high'
                            ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                            : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                        }`}>
                          {product.reorder.urgency}
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      {product.anomalies && product.anomalies.length > 0 ? (
                        <div className="flex flex-wrap gap-1">
                          {product.anomalies.map((a, i) => (
                            <span key={i} className="inline-block px-2 py-1 rounded text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400">
                              {a.type}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <span className="text-gray-500 dark:text-gray-400 text-sm">None</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <button
                        onClick={() => setExplainProduct(product)}
                        className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 text-sm font-medium transition-colors"
                      >
                        {t('why')}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Explainability Drawer */}
      {explainProduct && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm" onClick={() => setExplainProduct(null)}>
          <div className="bg-white dark:bg-gray-800 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6 shadow-2xl transform transition-all" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span className="text-3xl">🔍</span>
                {explainProduct.product_name}
              </h3>
              <button
                onClick={() => setExplainProduct(null)}
                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-2xl hover:scale-110 transition-transform"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div className="bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-700">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                  <span>📈</span>
                  Demand Reasoning
                </h4>
                <p className="text-gray-700 dark:text-gray-300">
                  {explainProduct.demand_reasoning || 'Based on historical sales patterns and forecasting models, we predict future demand trends.'}
                </p>
              </div>

              <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-lg p-4 border border-green-200 dark:border-green-700">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                  <span>📦</span>
                  Reorder Logic
                </h4>
                <p className="text-gray-700 dark:text-gray-300">
                  {explainProduct.reorder_logic || `Recommended quantity: ${explainProduct.reorder?.quantity || 'N/A'}. This is calculated based on forecasted demand plus a safety stock buffer to prevent stockouts.`}
                </p>
              </div>

              <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg p-4 border border-purple-200 dark:border-purple-700">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                  <span>🎯</span>
                  Confidence Explanation
                </h4>
                <p className="text-gray-700 dark:text-gray-300">
                  {explainProduct.confidence_explanation || `Confidence score of ${explainProduct.confidence_score}% is based on data quality, forecast accuracy, and historical pattern consistency.`}
                </p>
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
                <p className="text-sm text-blue-800 dark:text-blue-200 flex items-center gap-2">
                  <span className="text-lg">💡</span>
                  These insights are AI-generated. Please verify with your business knowledge before making decisions.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
