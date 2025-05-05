import { useEffect, useState } from 'react';
import { Language, TranslationService } from '@/types';
import { getSupportedLanguages } from '@/services/apiService';

interface LanguageSelectorProps {
  onChange: (value: string) => void;
  serviceType: TranslationService;
}

const LanguageSelector = ({ onChange, serviceType }: LanguageSelectorProps) => {
  const [languages, setLanguages] = useState<Language[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('');

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await getSupportedLanguages(serviceType);
        setLanguages(response.languages || []);
      } catch (err) {
        console.error('Failed to fetch languages:', err);
        setError('Failed to load supported languages. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchLanguages();
  }, [serviceType]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedLanguage(value);
    onChange(value);
  };

  return (
    <div className="w-full">
      {error && <p className="text-error text-sm mb-1">{error}</p>}
      <select
        onChange={handleChange}
        value={selectedLanguage}
        className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-primary focus:outline-none focus:ring-primary sm:text-sm bg-white text-gray-800 font-medium"
        disabled={isLoading || languages.length === 0}
      >
        <option value="" className="text-gray-500">Select a target language</option>
        {languages.map((language) => (
          <option 
            key={language.code} 
            value={language.code}
            className="text-gray-800 font-medium"
          >
            {language.name || (language.model ? `${language.code.toUpperCase()} (${language.model})` : language.code.toUpperCase())}
          </option>
        ))}
      </select>
      
      {isLoading && (
        <div className="flex items-center justify-center mt-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
          <span className="ml-2 text-sm text-gray-500">Loading available languages...</span>
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;