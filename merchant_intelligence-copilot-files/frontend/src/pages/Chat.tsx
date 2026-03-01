import React, { useState, useRef, useEffect } from 'react';
import { api } from '../lib/api';
import { ChatMessage } from '../types';
import { useLanguage } from '../hooks/useLanguage';

export function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiAvailable, setApiAvailable] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { language, t } = useLanguage();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const suggestions = {
    en: [
      'Which products should I order this week?',
      'What are my top selling products?',
      'Are there any demand spikes or alerts?'
    ],
    hi: [
      'मुझे इस सप्ताह कौन से उत्पाद ऑर्डर करने चाहिए?',
      'मेरे सबसे ज़्यादा बिकने वाले उत्पाद कौन से हैं?',
      'क्या कोई मांग में अचानक वृद्धि या अलर्ट है?'
    ],
    mr: [
      'या आठवड्यात मला कोणती उत्पादने मागवावी?',
      'माझी सर्वाधिक विक्री होणारी उत्पादने कोणती आहेत?',
      'मागणीत काही अचानक वाढ किंवा अलर्ट आहे का?'
    ]
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    // Auto-send the suggestion
    setTimeout(() => {
      handleSend();
    }, 100);
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Get insights from localStorage for context
      const storedInsights = localStorage.getItem('lastInsights');
      const insights = storedInsights ? JSON.parse(storedInsights) : null;
      
      const response = await api.post('/chat', {
        message: input,
        language,
        insights: insights
      });

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.data.response || response.data.message,
        confidence: response.data.confidence,
        timestamp: Date.now()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setApiAvailable(true);
    } catch (err: any) {
      console.error('Chat error:', err);
      
      if (err?.response?.status === 404) {
        setApiAvailable(false);
        const fallbackMessage: ChatMessage = {
          role: 'assistant',
          content: language === 'en' 
            ? '🚧 Chat backend is not connected yet. This feature will be available soon.\n\nIn the meantime, you can:\n• Upload CSV data to view insights\n• Check the Dashboard for forecasts\n• View the Weekly Report for recommendations'
            : language === 'hi'
            ? '🚧 चैट बैकएंड अभी कनेक्ट नहीं है। यह सुविधा जल्द ही उपलब्ध होगी।\n\nइस बीच, आप कर सकते हैं:\n• अंतर्दृष्टि देखने के लिए CSV डेटा अपलोड करें\n• पूर्वानुमान के लिए डैशबोर्ड देखें\n• सिफारिशों के लिए साप्ताहिक रिपोर्ट देखें'
            : '🚧 चॅट बॅकएंड अद्याप कनेक्ट केलेले नाही. ही सुविधा लवकरच उपलब्ध होईल.\n\nदरम्यान, तुम्ही करू शकता:\n• अंतर्दृष्टी पाहण्यासाठी CSV डेटा अपलोड करा\n• अंदाजांसाठी डॅशबोर्ड पहा\n• शिफारशींसाठी साप्ताहिक अहवाल पहा',
          timestamp: Date.now()
        };
        setMessages(prev => [...prev, fallbackMessage]);
      } else if (err?.code === 'ERR_NETWORK' || err?.message?.includes('Network Error')) {
        const errorMessage: ChatMessage = {
          role: 'assistant',
          content: language === 'en'
            ? '❌ Cannot connect to backend. Please ensure:\n• Backend is running (sam local start-api)\n• API URL is correct in .env file\n• Port 3000 is not blocked'
            : language === 'hi'
            ? '❌ बैकएंड से कनेक्ट नहीं हो सकता। कृपया सुनिश्चित करें:\n• बैकएंड चल रहा है (sam local start-api)\n• .env फ़ाइल में API URL सही है\n• पोर्ट 3000 ब्लॉक नहीं है'
            : '❌ बॅकएंडशी कनेक्ट होऊ शकत नाही. कृपया खात्री करा:\n• बॅकएंड चालू आहे (sam local start-api)\n• .env फाइलमध्ये API URL बरोबर आहे\n• पोर्ट 3000 ब्लॉक केलेला नाही',
          timestamp: Date.now()
        };
        setMessages(prev => [...prev, errorMessage]);
      } else {
        const errorMessage: ChatMessage = {
          role: 'assistant',
          content: `⚠️ ${language === 'en' ? 'Sorry, I encountered an error' : language === 'hi' ? 'क्षमा करें, मुझे एक त्रुटि का सामना करना पड़ा' : 'माफ करा, मला त्रुटी आली'}: ${err?.response?.data?.message || err?.message || 'Unknown error'}`,
          timestamp: Date.now()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-12rem)] flex flex-col page-transition">
      <div className="mb-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{t('chatTitle')}</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          {t('chatSubtitle')}
        </p>
      </div>

      {!apiAvailable && (
        <div className="mb-4 bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4 border border-amber-200 dark:border-amber-800 animate-slide-up">
          <div className="flex items-start gap-3">
            <span className="text-2xl">🚧</span>
            <div>
              <h3 className="font-semibold text-amber-800 dark:text-amber-200 mb-1">
                {language === 'en' ? 'Chat Feature Coming Soon' : language === 'hi' ? 'चैट सुविधा जल्द आ रही है' : 'चॅट वैशिष्ट्य लवकरच येत आहे'}
              </h3>
              <p className="text-sm text-amber-700 dark:text-amber-300">
                {language === 'en' 
                  ? 'The chat endpoint is not yet implemented in the backend. You can still use other features like Dashboard, Upload Data, and Weekly Report.'
                  : language === 'hi'
                  ? 'चैट एंडपॉइंट अभी बैकएंड में लागू नहीं किया गया है। आप अभी भी डैशबोर्ड, डेटा अपलोड और साप्ताहिक रिपोर्ट जैसी अन्य सुविधाओं का उपयोग कर सकते हैं।'
                  : 'चॅट एंडपॉइंट अद्याप बॅकएंडमध्ये लागू केलेला नाही. तुम्ही अजूनही डॅशबोर्ड, डेटा अपलोड आणि साप्ताहिक अहवाल यासारखी इतर वैशिष्ट्ये वापरू शकता.'}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="flex-1 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-y-auto p-4 space-y-4 mb-4 shadow-lg">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8 animate-fade-in">
            <div className="text-6xl mb-4 animate-float">💬</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              {t('startConversation')}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {t('askAnything')}
            </p>
            <div className="grid grid-cols-1 gap-3 w-full max-w-md">
              {suggestions[language].map((suggestion, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="px-4 py-3 bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/30 dark:to-purple-900/30 hover:from-indigo-100 hover:to-purple-100 dark:hover:from-indigo-900/50 dark:hover:to-purple-900/50 rounded-lg text-gray-700 dark:text-gray-300 transition-all hover:scale-105 text-left border border-indigo-200 dark:border-indigo-800"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                  {msg.confidence !== undefined && (
                    <div className="mt-2 pt-2 border-t border-gray-300 dark:border-gray-600">
                      <p className="text-xs opacity-75">{language === 'en' ? 'Confidence' : language === 'hi' ? 'विश्वास' : 'आत्मविश्वास'}: {msg.confidence}%</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start animate-slide-up">
                <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 mb-4 border border-blue-200 dark:border-blue-800">
        <p className="text-sm text-blue-800 dark:text-blue-200 flex items-center gap-2">
          <span className="text-lg">💡</span>
          {t('aiDisclaimer')}
        </p>
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={t('askMeAnything')}
          disabled={loading}
          className="flex-1 px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 disabled:opacity-50 focus:ring-2 focus:ring-indigo-500 transition-all"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-semibold px-6 py-3 rounded-lg transition-all transform hover:scale-105 disabled:hover:scale-100"
        >
          {t('send')}
        </button>
      </div>
    </div>
  );
}
