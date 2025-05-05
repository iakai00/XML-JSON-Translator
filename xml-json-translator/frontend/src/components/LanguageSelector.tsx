import { useEffect, useState } from 'react';
import Select from 'react-select';
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

  const options = languages.map(lang => ({
    value: lang.code,
    label: lang.name || (lang.model ? `${lang.code.toUpperCase()} (${lang.model})` : lang.code.toUpperCase())
  }));

  return (
    <div className="w-full">
      {error && <p className="text-red-500 text-sm mb-1">{error}</p>}
      <Select
        options={options}
        onChange={(option) => option && onChange(option.value)}
        placeholder={isLoading ? "Loading languages..." : "Select target language"}
        isDisabled={isLoading || languages.length === 0}
        className="w-full"
        classNames={{
          control: (state) => 
            `!rounded-md !shadow-sm !border ${state.isFocused ? '!border-blue-500 !shadow-outline-blue' : '!border-gray-300'}`
        }}
      />
      {isLoading && (
        <div className="flex items-center justify-center mt-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
          <span className="ml-2 text-sm text-gray-500">Loading available languages...</span>
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;