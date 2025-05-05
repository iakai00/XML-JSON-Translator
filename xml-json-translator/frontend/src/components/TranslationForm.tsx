// src/components/TranslationForm.tsx
import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import FileUploader from './FileUploader';
import LanguageSelector from './LanguageSelector';
import ServiceSelector from './ServiceSelector';
import LoadingSpinner from './LoadingSpinner';
import FileCard from './FileCard';
import { TranslationFormData, TranslationService, UploadState, TranslatedFile } from '@/types';
import { translateXmlFile, translateJsonFile } from '@/services/apiService';

const handleApiError = (error: any): string => {
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (error.message) {
    return error.message;
  }
  return 'An unknown error occurred';
};

const TranslationForm = () => {
  const [formData, setFormData] = useState<TranslationFormData>({
    files: [],
    targetLanguage: '',
    serviceType: 'huggingface',
  });
  
  const [isTranslating, setIsTranslating] = useState(false);
  const [translatedFiles, setTranslatedFiles] = useState<TranslatedFile[]>([]);
  const [currentFileIndex, setCurrentFileIndex] = useState(0);
  const [progress, setProgress] = useState(0);
  const [translationComplete, setTranslationComplete] = useState(false);

  const handleFilesSelect = (files: File[]) => {
    setFormData({ ...formData, files });
    // Reset translated files when new files are selected
    setTranslatedFiles([]);
  };

  const handleLanguageChange = (languageCode: string) => {
    setFormData({ ...formData, targetLanguage: languageCode });
  };

  const handleServiceChange = (serviceType: TranslationService) => {
    setFormData({ ...formData, serviceType });
  };

  // Updated part of TranslationForm.tsx handleSubmit function
  const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (formData.files.length === 0) {
        toast.error('Please select at least one file to translate');
        return;
        }
        
        if (!formData.targetLanguage) {
        toast.error('Please select a target language');
        return;
        }
        
        try {
        setIsTranslating(true);
        setTranslationComplete(false);
        setCurrentFileIndex(0);
        setProgress(0);
        setTranslatedFiles([]);
        
        const results: TranslatedFile[] = [];
        
        // Process files one by one
        for (let i = 0; i < formData.files.length; i++) {
            const file = formData.files[i];
            setCurrentFileIndex(i);
            
            // Calculate and update progress
            const currentProgress = Math.round(((i) / formData.files.length) * 100);
            setProgress(currentProgress);
            
            // Properly detect file type
            const fileExtension = file.name.split('.').pop()?.toLowerCase();
            if (!fileExtension || !['xml', 'json'].includes(fileExtension)) {
            toast.warning(`Skipping ${file.name}: Only XML and JSON files are supported`);
            continue;
            }
            
            let url: string;
            
            try {
            // Check file content type more carefully
            if (fileExtension === 'xml') {
                url = await translateXmlFile(
                file, 
                formData.targetLanguage, 
                formData.serviceType
                );
            } else if (fileExtension === 'json') {
                url = await translateJsonFile(
                file, 
                formData.targetLanguage, 
                formData.serviceType
                );
            } else {
                throw new Error(`Unsupported file type: ${fileExtension}`);
            }
            
            // Generate download filename
            const originalName = file.name.split('.')[0];
            const newFilename = `${originalName}_${formData.targetLanguage}.${fileExtension}`;
            
            // Add to translated files
            results.push({
                originalName: file.name,
                translatedName: newFilename,
                downloadUrl: url,
                targetLanguage: formData.targetLanguage,
                timestamp: new Date().toISOString()
            });
            } catch (error) {
            console.error(`Error translating file ${file.name}:`, error);
            toast.error(`Failed to translate ${file.name}: ${handleApiError(error)}`);
            }
        }
        
        // Update progress to 100% when all files are done, even if there were some errors
        setProgress(100);
        
        // Only show completion modal if at least one file was translated
        if (results.length > 0) {
            setTranslatedFiles(results);
            setTranslationComplete(true);
            
            // Close modal after a short delay to show 100% completion
            setTimeout(() => {
            setIsTranslating(false);
            setTranslationComplete(false);
            toast.success(`Successfully translated ${results.length} file(s)!`);
            }, 1500);
        } else {
            setIsTranslating(false);
            toast.error('No files were translated successfully');
        }
        } catch (error) {
        console.error('Translation error:', error);
        toast.error('Failed to translate files. Please try again.');
        setIsTranslating(false);
        setTranslationComplete(false);
        }
  };

  const acceptedFiles = {
    'application/xml': ['.xml'],
    'application/json': ['.json'],
    'text/xml': ['.xml'],
    'text/plain': ['.xml', '.json'],
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <div className="bg-primary px-6 py-4">
            <h3 className="text-lg font-medium text-white">Upload Files</h3>
            <p className="text-white text-sm opacity-80">Drag and drop or select files to translate</p>
          </div>
          <div className="p-6">
            <FileUploader
              onFilesSelect={handleFilesSelect}
              accept={acceptedFiles}
              maxSize={5 * 1024 * 1024} // 5MB
              multiple={true}
            />
            {formData.files.length > 0 && (
              <div className="mt-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Selected Files ({formData.files.length})</h4>
                <ul className="text-sm text-gray-600 space-y-1 max-h-40 overflow-y-auto bg-gray-50 rounded p-2">
                  {formData.files.map((file, index) => (
                    <li key={index} className="flex items-center">
                      <svg className="h-4 w-4 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      {file.name} ({(file.size / 1024).toFixed(1)} KB)
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <div className="bg-secondary px-6 py-4">
              <h3 className="text-lg font-medium text-white">Target Language</h3>
              <p className="text-white text-sm opacity-80">Select the language to translate to</p>
            </div>
            <div className="p-6">
              <LanguageSelector
                onChange={handleLanguageChange}
                serviceType={formData.serviceType}
              />
            </div>
          </div>
          
          <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <div className="bg-secondary-light px-6 py-4">
              <h3 className="text-lg font-medium text-gray-800">Translation Service</h3>
              <p className="text-gray-600 text-sm">Choose your preferred translation engine</p>
            </div>
            <div className="p-6">
              <ServiceSelector
                value={formData.serviceType}
                onChange={handleServiceChange}
              />
            </div>
          </div>
        </div>

        <div className="flex justify-center mt-8">
          <button
            type="submit"
            disabled={isTranslating || formData.files.length === 0 || !formData.targetLanguage}
            className={`
              px-6 py-3 rounded-md font-medium text-white shadow-md transition duration-200 ease-in-out
              ${isTranslating || formData.files.length === 0 || !formData.targetLanguage 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50'
              }
            `}
          >
            {isTranslating ? (
              <div className="flex items-center">
                <span className="mr-2">Translating</span>
                <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              </div>
            ) : (
              <>
                <span>Translate {formData.files.length > 1 ? `${formData.files.length} Files` : 'File'}</span>
              </>
            )}
          </button>
        </div>
      </form>

      {isTranslating && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-xl shadow-2xl text-center max-w-md w-full">
            {!translationComplete ? (
              <>
                <LoadingSpinner size="large" />
                <h3 className="mt-4 text-xl font-medium text-gray-800">Translating Files</h3>
                <p className="mt-2 text-gray-600">
                  File {currentFileIndex + 1} of {formData.files.length}: {formData.files[currentFileIndex]?.name ?? ''}
                </p>
              </>
            ) : (
              <>
                <div className="w-16 h-16 mx-auto bg-success-light rounded-full flex items-center justify-center">
                  <svg className="w-10 h-10 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h3 className="mt-4 text-xl font-medium text-gray-800">Translation Complete!</h3>
                <p className="mt-2 text-gray-600">
                  Successfully translated {translatedFiles.length} file(s)
                </p>
              </>
            )}
            <div className="mt-6 w-full bg-gray-200 rounded-full h-2.5">
              <div className="bg-primary h-2.5 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
            </div>
            <p className="mt-2 text-sm text-gray-500">{progress}% Complete</p>
            
            {translationComplete && (
              <button
                type="button"
                className="mt-6 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none"
                onClick={() => setIsTranslating(false)}
              >
                View Results
              </button>
            )}
          </div>
        </div>
      )}

      {translatedFiles.length > 0 && (
        <div className="mt-8 bg-white shadow-md rounded-lg overflow-hidden">
          <div className="bg-success px-6 py-4">
            <h3 className="text-lg font-medium text-white">Translated Files</h3>
            <p className="text-white text-sm opacity-80">Download your translated files</p>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {translatedFiles.map((file, index) => (
                <FileCard key={index} file={file} />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TranslationForm;