import React, { useState } from 'react';
import { toast } from 'react-toastify';
import FileUploader from './FileUploader';
import LanguageSelector from './LanguageSelector';
import ServiceSelector from './ServiceSelector';
import LoadingSpinner from './LoadingSpinner';
import { TranslationFormData, TranslationService } from '@/types';
import { translateXmlFile, translateJsonFile } from '@/services/apiService';

const TranslationForm = () => {
  const [formData, setFormData] = useState<TranslationFormData>({
    file: null,
    targetLanguage: '',
    serviceType: 'huggingface',
  });

  const [isTranslating, setIsTranslating] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [downloadFilename, setDownloadFilename] = useState<string | null>(null);

  const handleFileSelect = (file: File) => {
    setFormData({ ...formData, file });
    // Reset download data when a new file is selected
    setDownloadUrl(null);
    setDownloadFilename(null);
  };

  const handleLanguageChange = (languageCode: string) => {
    setFormData({ ...formData, targetLanguage: languageCode });
  };

  const handleServiceChange = (serviceType: TranslationService) => {
    setFormData({ ...formData, serviceType });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.file) {
      toast.error('Please select a file to translate');
      return;
    }
    
    if (!formData.targetLanguage) {
      toast.error('Please select a target language');
      return;
    }
    
    const fileExtension = formData.file.name.split('.').pop()?.toLowerCase();
    if (!fileExtension || !['xml', 'json'].includes(fileExtension)) {
      toast.error('Only XML and JSON files are supported');
      return;
    }

    try {
      setIsTranslating(true);
      
      let url: string;
      
      if (fileExtension === 'xml') {
        url = await translateXmlFile(
          formData.file, 
          formData.targetLanguage, 
          formData.serviceType
        );
      } else {
        url = await translateJsonFile(
          formData.file, 
          formData.targetLanguage, 
          formData.serviceType
        );
      }
      
      // Generate download filename
      const originalName = formData.file.name.split('.')[0];
      const newFilename = `${originalName}_${formData.targetLanguage}.${fileExtension}`;
      
      setDownloadUrl(url);
      setDownloadFilename(newFilename);
      
      toast.success('Translation completed successfully!');
    } catch (error) {
      console.error('Translation error:', error);
      toast.error('Failed to translate file. Please try again.');
    } finally {
      setIsTranslating(false);
    }
  };

  const acceptedFiles = {
    'application/xml': ['.xml'],
    'application/json': ['.json'],
    'text/xml': ['.xml'],
    'text/plain': ['.xml', '.json'],
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Upload File</h3>
        <FileUploader
          onFileSelect={handleFileSelect}
          accept={acceptedFiles}
          maxSize={5 * 1024 * 1024} // 5MB
        />
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Translation Settings</h3>
        
        <div className="space-y-4">
          <div>
            <label htmlFor="targetLanguage" className="block text-sm font-medium text-gray-700 mb-1">
              Target Language
            </label>
            <LanguageSelector
              onChange={handleLanguageChange}
              serviceType={formData.serviceType}
            />
          </div>
          
          <div>
            <ServiceSelector
              value={formData.serviceType}
              onChange={handleServiceChange}
            />
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center">
        <button
          type="submit"
          disabled={isTranslating || !formData.file || !formData.targetLanguage}
          className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
            ${isTranslating || !formData.file || !formData.targetLanguage 
              ? 'opacity-50 cursor-not-allowed' 
              : 'hover:bg-blue-700'}`}
        >
          {isTranslating ? (
            <>
              <span className="mr-2">Translating</span>
              <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            </>
          ) : (
            'Translate File'
          )}
        </button>

        {downloadUrl && downloadFilename && (
          <a
            href={downloadUrl}
            download={downloadFilename}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            <svg className="mr-1.5 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download Translated File
          </a>
        )}
      </div>

      {isTranslating && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <LoadingSpinner size="large" message="Translating your file... This may take a moment." />
          </div>
        </div>
      )}
    </form>
  );
};

export default TranslationForm;