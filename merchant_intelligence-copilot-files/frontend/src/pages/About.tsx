import React from 'react';

export function About() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">About</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          AI-powered decision assistant for Indian MSMEs
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">The Problem</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Indian Micro, Small, and Medium Enterprises (MSMEs) represent 30% of India's GDP and employ over 110 million people. 
          However, 80% of these businesses operate with minimal digital infrastructure, leading to:
        </p>
        <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
          <li>30-40% inventory wastage due to overstocking or stockouts</li>
          <li>15-20% revenue loss from suboptimal pricing decisions</li>
          <li>Limited market intelligence leading to missed demand opportunities</li>
          <li>High operational friction in understanding sales patterns and trends</li>
        </ul>
        <p className="text-gray-700 dark:text-gray-300 mt-4">
          Traditional business intelligence tools are too expensive (₹10,000-50,000/month), require technical expertise, 
          and lack vernacular language support—making them inaccessible to most MSMEs.
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Our Solution</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Merchant Intelligence Copilot is an AI-powered decision assistant that transforms simple CSV/POS sales data 
          into actionable business intelligence. Merchants upload their sales history, and the system generates:
        </p>
        <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
          <li>Demand forecasts with confidence intervals</li>
          <li>Inventory recommendations with urgency indicators</li>
          <li>Anomaly alerts for demand spikes and drops</li>
          <li>Multilingual action plans (English, Hindi, Marathi)</li>
          <li>Conversational chat interface for natural language queries</li>
        </ul>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">AI Usage</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Forecasting</h3>
            <p className="text-gray-700 dark:text-gray-300">
              We use Prophet (Meta) time-series models to predict future demand with confidence intervals. 
              Machine learning is essential because it captures non-linear patterns, seasonality, and trends 
              that traditional spreadsheets cannot.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Amazon Bedrock Reasoning</h3>
            <p className="text-gray-700 dark:text-gray-300">
              Large Language Models (LLMs) transform raw forecasts into actionable intelligence. We use Amazon Bedrock 
              to generate natural language explanations, multilingual support, and conversational AI capabilities. 
              This makes complex data accessible to non-technical merchants.
            </p>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Responsible AI</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Confidence Scoring</h3>
            <p className="text-gray-700 dark:text-gray-300">
              Every AI recommendation includes a confidence score (0-100%) based on data quality and forecast accuracy. 
              Color-coded badges help merchants quickly identify which insights to trust.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Transparency & Explainability</h3>
            <p className="text-gray-700 dark:text-gray-300">
              Every recommendation includes a "Why?" explanation showing the reasoning behind forecasts, reorder quantities, 
              and confidence scores. Merchants understand not just what to do, but why.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Disclaimers</h3>
            <p className="text-gray-700 dark:text-gray-300">
              All AI-generated content includes clear disclaimers reminding merchants that these are probabilistic 
              suggestions that should be verified with business judgment.
            </p>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Hackathon Context</h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          This project was built for the AWS AI for Bharat Hackathon, focusing on AI solutions that help 
          Indian businesses work smarter and become more productive.
        </p>
        <div className="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-4 border border-indigo-200 dark:border-indigo-800">
          <p className="text-sm text-indigo-800 dark:text-indigo-200">
            <strong>Team:</strong> Bharat Brain Wave<br />
            <strong>Theme:</strong> AI for Retail, Commerce & Market Intelligence<br />
            <strong>Cost:</strong> ₹37/merchant/month (100x cheaper than traditional tools)
          </p>
        </div>
      </div>

      <div className="bg-gradient-to-r from-indigo-50 to-blue-50 dark:from-indigo-900/20 dark:to-blue-900/20 rounded-xl p-6 border border-indigo-200 dark:border-indigo-800">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Built with ❤️ for Bharat MSMEs</h2>
        <p className="text-gray-700 dark:text-gray-300">
          Empowering small businesses with enterprise-grade AI at affordable prices
        </p>
      </div>
    </div>
  );
}
