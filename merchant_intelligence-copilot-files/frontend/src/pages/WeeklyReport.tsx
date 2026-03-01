import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';
import { InsightsData } from '../types';
import { useLanguage } from '../hooks/useLanguage';

interface ReportData {
  priorities: Array<{
    title: string;
    description: string;
    impact: string;
  }>;
  risks: string[];
  quick_wins?: string[];
  generated_at: string;
  summary_text?: string;
}

export function WeeklyReport() {
  const [report, setReport] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { t, language } = useLanguage();

  useEffect(() => {
    fetchReport();
  }, [language]);

  const fetchReport = async () => {
    setLoading(true);
    setError('');

    try {
      // Get insights from localStorage
      const storedData = localStorage.getItem('lastInsights');
      if (!storedData) {
        setError(t('noDataYet') || 'No insights data available. Please upload and analyze data first.');
        setLoading(false);
        return;
      }

      const insights: InsightsData = JSON.parse(storedData);

      // Call backend to generate report
      const response = await api.post('/weekly-report', {
        insights: insights,
        language: language
      });

      setReport(response.data.report);
    } catch (err: any) {
      console.error('Report generation error:', err);
      // Fallback to client-side report
      generateClientSideReport();
    } finally {
      setLoading(false);
    }
  };

  const generateClientSideReport = () => {
    const storedData = localStorage.getItem('lastInsights');
    if (!storedData) {
      setError(t('noDataYet') || 'No insights data available. Please upload and analyze data first.');
      return;
    }

    const insights: InsightsData = JSON.parse(storedData);
    const products = insights.insights?.products || insights.products || [];

    const highUrgency = products.filter(p => p.reorder?.urgency === 'high');
    const alerts = products.filter(p => p.anomalies && p.anomalies.length > 0);
    const lowConfidence = products.filter(p => p.confidence_score < 60);
    const priceOpps = products.filter(p => p.price_hint?.action === 'increase' || p.price_hint?.action === 'discount');

    const priorities = [
      {
        title: t('highPriorityReorders') || 'High Priority Reorders',
        description: highUrgency.length > 0
          ? `${highUrgency.length} products need urgent reordering: ${highUrgency.slice(0, 3).map(p => p.product_name).join(', ')}`
          : 'No urgent reorders needed this week',
        impact: highUrgency.length > 0 ? 'Prevent stockouts and maintain sales' : 'Maintain current inventory levels'
      },
      {
        title: t('demandAnomalies') || 'Demand Anomalies',
        description: alerts.length > 0
          ? `${alerts.length} products showing unusual patterns: ${alerts.slice(0, 3).map(p => p.product_name).join(', ')}`
          : 'All products showing normal demand patterns',
        impact: alerts.length > 0 ? 'Adjust inventory and pricing strategy' : 'Continue current operations'
      },
      {
        title: t('priceOptimization') || 'Price Optimization',
        description: priceOpps.length > 0
          ? `${priceOpps.length} products have pricing opportunities`
          : 'Current pricing is optimal',
        impact: priceOpps.length > 0 ? 'Increase revenue through strategic pricing' : 'Maintain current pricing'
      }
    ];

    const risks = [];
    if (highUrgency.length > 5) risks.push('Multiple products at risk of stockout');
    if (alerts.length > 3) risks.push('Unusual demand patterns detected across multiple products');
    if (lowConfidence.length > products.length * 0.3) risks.push('Data quality issues affecting forecast accuracy');
    if (risks.length === 0) risks.push('No significant risks identified');

    const quick_wins = [];
    if (highUrgency.length > 0) quick_wins.push(`Order ${highUrgency[0].product_name} immediately`);
    if (priceOpps.length > 0) quick_wins.push(`Adjust price for ${priceOpps[0].product_name}`);
    if (lowConfidence.length > 0) quick_wins.push('Review low confidence items for data quality');

    setReport({
      priorities,
      risks,
      quick_wins,
      generated_at: new Date().toISOString()
    });
  };

  const copyToClipboard = () => {
    if (!report) return;

    const markdown = `# ${t('weeklyReport') || 'Weekly Business Report'}
${t('generated') || 'Generated'}: ${new Date(report.generated_at).toLocaleDateString()}

## ${t('topPriorities') || 'Top 3 Priorities'}

${report.priorities.map((p, i) => `### ${i + 1}. ${p.title}
${p.description}

**${t('expectedImpact') || 'Expected Impact'}:** ${p.impact}
`).join('\n')}

## ${t('risksAlerts') || 'Risks & Alerts'}

${report.risks.map(r => `- ${r}`).join('\n')}

${report.quick_wins && report.quick_wins.length > 0 ? `## ${t('quickWins') || 'Quick Wins'}\n\n${report.quick_wins.map(q => `- ${q}`).join('\n')}` : ''}

---
*${t('generatedBy') || 'Generated by'} Merchant Intelligence Copilot*
`;

    navigator.clipboard.writeText(markdown);
    alert(t('reportCopied') || 'Report copied to clipboard as Markdown!');
  };

  const exportToPDF = () => {
    if (!report) return;

    // Create printable HTML content
    const printContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>${t('weeklyReport') || 'Weekly Business Report'}</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 800px;
      margin: 40px auto;
      padding: 20px;
      color: #333;
    }
    h1 {
      color: #4F46E5;
      border-bottom: 3px solid #4F46E5;
      padding-bottom: 10px;
    }
    h2 {
      color: #6366F1;
      margin-top: 30px;
      border-bottom: 2px solid #E0E7FF;
      padding-bottom: 8px;
    }
    h3 {
      color: #4338CA;
      margin-top: 20px;
    }
    .priority {
      background: #F5F3FF;
      border-left: 4px solid #6366F1;
      padding: 15px;
      margin: 15px 0;
      border-radius: 4px;
    }
    .risk {
      background: #FEF3C7;
      border-left: 4px solid #F59E0B;
      padding: 10px;
      margin: 10px 0;
      border-radius: 4px;
    }
    .quick-win {
      background: #D1FAE5;
      border-left: 4px solid #10B981;
      padding: 10px;
      margin: 10px 0;
      border-radius: 4px;
    }
    .meta {
      color: #6B7280;
      font-size: 14px;
      margin-bottom: 20px;
    }
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #E5E7EB;
      text-align: center;
      color: #9CA3AF;
      font-size: 12px;
    }
    @media print {
      body { margin: 0; padding: 20px; }
    }
  </style>
</head>
<body>
  <h1>📊 ${t('weeklyReport') || 'Weekly Business Report'}</h1>
  <div class="meta">${t('generated') || 'Generated'}: ${new Date(report.generated_at).toLocaleDateString()}</div>
  
  <h2>🎯 ${t('topPriorities') || 'Top 3 Priorities'}</h2>
  ${report.priorities.map((p, i) => `
    <div class="priority">
      <h3>${i + 1}. ${p.title}</h3>
      <p>${p.description}</p>
      <p><strong>${t('expectedImpact') || 'Expected Impact'}:</strong> ${p.impact}</p>
    </div>
  `).join('')}
  
  <h2>⚠️ ${t('risksAlerts') || 'Risks & Alerts'}</h2>
  ${report.risks.map(r => `<div class="risk">⚠️ ${r}</div>`).join('')}
  
  ${report.quick_wins && report.quick_wins.length > 0 ? `
    <h2>⚡ ${t('quickWins') || 'Quick Wins'}</h2>
    ${report.quick_wins.map(q => `<div class="quick-win">✓ ${q}</div>`).join('')}
  ` : ''}
  
  <div class="footer">
    ${t('generatedBy') || 'Generated by'} Merchant Intelligence Copilot<br>
    ${t('aiDisclaimer') || 'Automated insights. Review with your business knowledge.'}
  </div>
</body>
</html>
    `;

    // Open print dialog
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(printContent);
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => {
        printWindow.print();
      }, 250);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto page-transition">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-12 text-center border border-gray-200 dark:border-gray-700 shadow-lg">
          <div className="text-6xl mb-4 animate-float">⏳</div>
          <p className="text-gray-600 dark:text-gray-400">{t('loading') || 'Loading weekly report...'}</p>
        </div>
      </div>
    );
  }

  if (error && !report) {
    return (
      <div className="max-w-4xl mx-auto page-transition">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-12 text-center border border-gray-200 dark:border-gray-700 shadow-lg">
          <div className="text-6xl mb-4">📋</div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{t('noReportAvailable') || 'No Report Available'}</h2>
          <p className="text-gray-600 dark:text-gray-400">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 page-transition">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <span className="text-4xl">📊</span>
            {t('weeklyReport') || 'Weekly Report'}
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            {t('aiGeneratedPlan') || 'AI-generated action plan for the week ahead'}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={copyToClipboard}
            className="bg-gray-600 hover:bg-gray-700 text-white font-semibold px-4 py-2 rounded-lg transition-all transform hover:scale-105 shadow-lg flex items-center gap-2"
            title="Copy as Markdown"
          >
            📋 {t('copy') || 'Copy'}
          </button>
          <button
            onClick={exportToPDF}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold px-4 py-2 rounded-lg transition-all transform hover:scale-105 shadow-lg flex items-center gap-2"
            title="Export as PDF"
          >
            📄 {t('exportPDF') || 'Export PDF'}
          </button>
        </div>
      </div>

      {report && (
        <>
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-lg">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span>🎯</span>
                {t('topPriorities') || 'Top 3 Priorities'}
              </h2>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {new Date(report.generated_at).toLocaleDateString()}
              </span>
            </div>

            <div className="space-y-4">
              {report.priorities.map((priority, idx) => (
                <div key={idx} className="bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-700/50 dark:to-blue-900/20 rounded-lg p-4 border border-gray-200 dark:border-gray-600 hover:shadow-md transition-all">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full flex items-center justify-center font-bold shadow-lg">
                      {idx + 1}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                        {priority.title}
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 text-sm mb-2">
                        {priority.description}
                      </p>
                      <div className="bg-blue-50 dark:bg-blue-900/20 rounded px-3 py-2 border border-blue-200 dark:border-blue-800">
                        <p className="text-sm text-blue-800 dark:text-blue-200">
                          <strong>{t('expectedImpact') || 'Expected Impact'}:</strong> {priority.impact}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-lg">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <span>⚠️</span>
              {t('risksAlerts') || 'Risks & Alerts'}
            </h2>
            <ul className="space-y-2">
              {report.risks.map((risk, idx) => (
                <li key={idx} className="flex items-start gap-3 p-3 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800">
                  <span className="text-amber-500 mt-1">⚠️</span>
                  <span className="text-gray-700 dark:text-gray-300">{risk}</span>
                </li>
              ))}
            </ul>
          </div>

          {report.quick_wins && report.quick_wins.length > 0 && (
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-xl p-6 border border-green-200 dark:border-green-700 shadow-lg">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <span>⚡</span>
                {t('quickWins') || 'Quick Wins'}
              </h2>
              <ul className="space-y-2">
                {report.quick_wins.map((win, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <span className="text-green-500 mt-1">✓</span>
                    <span className="text-gray-700 dark:text-gray-300">{win}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
            <p className="text-sm text-blue-800 dark:text-blue-200 flex items-center gap-2">
              <span className="text-lg">💡</span>
              {t('aiDisclaimer') || 'Automated insights. Review with your business knowledge.'}
            </p>
          </div>
        </>
      )}
    </div>
  );
}
