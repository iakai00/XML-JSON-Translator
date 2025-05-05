import axios from 'axios';
import { SupportedLanguagesResponse, TranslationService } from '@/types';

// Configure base axios instance
const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

console.log('API Service initialized with baseURL:', baseURL);

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Add timeout for better user experience
  timeout: 60000, // 60 seconds
});

/**
 * Fetch supported languages from the backend
 */
export const getSupportedLanguages = async (serviceType?: TranslationService): Promise<SupportedLanguagesResponse> => {
  const params = serviceType ? { service_type: serviceType } : {};
  console.log('Fetching languages with params:', params);
  try {
    const response = await api.get('/translate/languages', { params });
    console.log('Languages response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching languages:', error);
    throw error;
  }
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

  try {
    const response = await api.post('/translate/xml', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    });

    // Create a blob URL for the downloaded file
    return URL.createObjectURL(response.data);
  } catch (error) {
    console.error('Error translating XML file:', error);
    throw error;
  }
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

  try {
    const response = await api.post('/translate/json', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    });

    // Create a blob URL for the downloaded file
    return URL.createObjectURL(response.data);
  } catch (error) {
    console.error('Error translating JSON file:', error);
    throw error;
  }
};

/**
 * Helper function to handle API errors
 */
export const handleApiError = (error: any): string => {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    if (error.response.data && error.response.data.detail) {
      return error.response.data.detail;
    }
    return `Server error: ${error.response.status}`;
  } else if (error.request) {
    // The request was made but no response was received
    return 'No response from server. Please check your connection.';
  } else {
    // Something happened in setting up the request that triggered an Error
    return `Error: ${error.message}`;
  }
};

// Add a function to detect file type properly
export const getFileType = (file: File): 'xml' | 'json' | 'unknown' => {
  const fileName = file.name.toLowerCase();
  if (fileName.endsWith('.xml')) {
    return 'xml';
  } else if (fileName.endsWith('.json') || fileName.endsWith('.jsonl')) {
    return 'json';
  }
  
  // If we can't determine by extension, try to check content
  // This is a simplified check and might need improvement
  return 'unknown';
};

const apiService = {
  getSupportedLanguages,
  translateXmlFile,
  translateJsonFile,
  handleApiError,
  getFileType
};

export default apiService;