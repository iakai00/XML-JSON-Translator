// Language option type for dropdown selection
export interface Language {
    code: string;
    name?: string;
    model?: string;
  }
  
  // Translation service options
  export type TranslationService = 'huggingface' | 'bedrock';
  
  // Form data for translation request
  export interface TranslationFormData {
    files: File[];
    targetLanguage: string;
    serviceType: TranslationService;
  }
  
  // Record for a translated file
  export interface TranslatedFile {
    originalName: string;
    translatedName: string;
    downloadUrl: string;
    targetLanguage: string;
    timestamp: string;
  }
  
  // API response types
  export interface ApiError {
    detail: string;
  }
  
  export interface SupportedLanguagesResponse {
    languages: Language[];
  }
  
  export interface TranslationResponse {
    success: boolean;
    message: string;
    filename?: string;
    download_url?: string;
  }
  
  // Upload states
  export enum UploadState {
    IDLE = 'idle',
    UPLOADING = 'uploading',
    SUCCESS = 'success',
    ERROR = 'error'
  }