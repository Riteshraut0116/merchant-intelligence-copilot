import React from 'react';
import { useTheme, Theme } from '../hooks/useTheme';
import { useLanguage, Language } from '../hooks/useLanguage';

export function Settings() {
  const { theme, setTheme } = useTheme();
  const { language, setLanguage, t } = useLanguage();

  const themes: { value: Theme; label: string; icon: string; preview: string }[] = [
    { value: 'light', label: t('lightMode'), icon: '☀️', preview: 'bg-white border-gray-200' },
    { value: 'dark', label: t('darkMode'), icon: '🌙', preview: 'bg-gray-900 border-gray-700' },
    { value: 'gradient-dark', label: t('gradientDark'), icon: '🌈', preview: 'bg-gradient-to-br from-purple-900 to-indigo-900' },
    { value: 'glassmorphism', label: t('glassmorphism'), icon: '💎', preview: 'bg-gradient-to-br from-blue-100 to-purple-100' },
    { value: 'minimal', label: t('minimal'), icon: '⚪', preview: 'bg-white border-gray-100' },
  ];

  const languages: { value: Language; label: string; flag: string }[] = [
    { value: 'en', label: 'English', flag: '🇮🇳' },
    { value: 'hi', label: 'हिंदी', flag: '🇮🇳' },
    { value: 'mr', label: 'मराठी', flag: '🇮🇳' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8 page-transition">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{t('settingsTitle')}</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Customize your experience
        </p>
      </div>

      {/* Theme Settings */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-lg hover-lift">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <span className="text-2xl">🎨</span>
          {t('themeSettings')}
        </h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          {t('selectTheme')}
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {themes.map((themeOption) => (
            <button
              key={themeOption.value}
              onClick={() => setTheme(themeOption.value)}
              className={`relative p-4 rounded-lg border-2 transition-all hover:scale-105 ${
                theme === themeOption.value
                  ? 'border-indigo-500 ring-2 ring-indigo-200 dark:ring-indigo-800'
                  : 'border-gray-200 dark:border-gray-700 hover:border-indigo-300'
              }`}
            >
              <div className={`h-20 rounded-lg mb-3 ${themeOption.preview} border`} />
              <div className="flex items-center justify-between">
                <span className="font-medium text-gray-900 dark:text-white">
                  {themeOption.label}
                </span>
                <span className="text-2xl">{themeOption.icon}</span>
              </div>
              {theme === themeOption.value && (
                <div className="absolute top-2 right-2 bg-indigo-500 text-white rounded-full p-1">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Language Settings */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 shadow-lg hover-lift">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <span className="text-2xl">🌐</span>
          {t('languageSettings')}
        </h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          {t('interfaceLanguage')}
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {languages.map((lang) => (
            <button
              key={lang.value}
              onClick={() => setLanguage(lang.value)}
              className={`relative p-6 rounded-lg border-2 transition-all hover:scale-105 ${
                language === lang.value
                  ? 'border-indigo-500 ring-2 ring-indigo-200 dark:ring-indigo-800 bg-indigo-50 dark:bg-indigo-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-indigo-300'
              }`}
            >
              <div className="text-center">
                <div className="text-4xl mb-2">{lang.flag}</div>
                <div className="font-medium text-gray-900 dark:text-white">
                  {lang.label}
                </div>
              </div>
              {language === lang.value && (
                <div className="absolute top-2 right-2 bg-indigo-500 text-white rounded-full p-1">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Preview Section */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-xl p-6 border border-indigo-200 dark:border-indigo-800">
        <div className="flex items-start gap-3">
          <span className="text-2xl">💡</span>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
              {language === 'en' ? 'Tip' : language === 'hi' ? 'सुझाव' : 'टीप'}
            </h3>
            <p className="text-sm text-gray-700 dark:text-gray-300">
              {language === 'en' 
                ? 'Your theme and language preferences are saved automatically and will persist across sessions.'
                : language === 'hi'
                ? 'आपकी थीम और भाषा प्राथमिकताएं स्वचालित रूप से सहेजी जाती हैं और सत्रों में बनी रहेंगी।'
                : 'तुमची थीम आणि भाषा प्राधान्ये स्वयंचलितपणे जतन केली जातात आणि सत्रांमध्ये टिकून राहतील.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
