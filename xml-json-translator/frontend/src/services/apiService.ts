import axios from 'axios';
import { SupportedLanguagesResponse, TranslationService } from '@/types';

// Configure base axios instance
const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch supported languages from the backend
 */
export const getSupportedLanguages = async (serviceType?: TranslationService): Promise<SupportedLanguagesResponse> => {
  const params = serviceType ? { service_type: serviceType } : {};
  const response = await api.get('/translate/languages', { params });
  return response.data;
};

/**
 * Translate an XML file
 */
export const translateXmlFile = async (
  file: File,
  targetLanguage: string,
  serviceType?: TranslationService
): Promise<string> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('target_language', targetLanguage);
  
  if (serviceType) {
    formData.append('service_type', serviceType);
  }

  const response = await api.post('/translate/xml', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    responseType: 'blob',
  });

  // Create a blob URL for the downloaded file
  return URL.createObjectURL(response.data);
};

/**
 * Translate a JSON file
 */
export const translateJsonFile = async (
  file: File,
  targetLanguage: string,
  serviceType?: TranslationService
): Promise<string> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('target_language', targetLanguage);
  
  if (serviceType) {
    formData.append('service_type', serviceType);
  }

  const response = await api.post('/translate/json', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    responseType: 'blob',
  });

  // Create a blob URL for the downloaded file
  return URL.createObjectURL(response.data);
};

const apiService = {
    getSupportedLanguages,
    translateXmlFile,
    translateJsonFile,
  };
  
export default apiService;