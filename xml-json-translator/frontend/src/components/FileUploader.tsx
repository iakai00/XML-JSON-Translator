import { useCallback, useState } from 'react';
import { useDropzone, FileRejection, DropEvent } from 'react-dropzone';
import { UploadState } from '@/types';

interface FileUploaderProps {
  onFilesSelect: (files: File[]) => void;
  accept: Record<string, string[]>;
  maxSize?: number;
  multiple?: boolean;
}

const FileUploader = ({ 
  onFilesSelect, 
  accept, 
  maxSize = 5 * 1024 * 1024,
  multiple = false
}: FileUploaderProps) => {
  const [uploadState, setUploadState] = useState<UploadState>(UploadState.IDLE);
  const [fileNames, setFileNames] = useState<string[]>([]);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const names = acceptedFiles.map(file => file.name);
      setFileNames(names);
      setUploadState(UploadState.SUCCESS);
      setErrorMessage('');
      onFilesSelect(acceptedFiles);
    }
  }, [onFilesSelect]);

  const onDropRejected = useCallback((fileRejections: FileRejection[], event: DropEvent) => {
    if (fileRejections.length > 0) {
      const rejection = fileRejections[0];
      let message = 'File upload failed';
      
      if (rejection?.errors?.length > 0) {
        const error = rejection.errors[0];
        if (error.code === 'file-too-large') {
          message = `File is too large. Max size is ${maxSize / (1024 * 1024)}MB`;
        } else if (error.code === 'file-invalid-type') {
          message = 'Invalid file type. Please select XML or JSON files';
        } else {
          message = error.message;
        }
      }
      
      setErrorMessage(message);
      setUploadState(UploadState.ERROR);
    }
  }, [maxSize]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    onDropRejected,
    accept,
    maxSize,
    multiple
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 cursor-pointer transition-all duration-300 text-center
          ${isDragActive ? 'border-primary bg-primary-light bg-opacity-10' : 'border-gray-300 hover:border-primary hover:bg-gray-50'}
          ${uploadState === UploadState.ERROR ? 'border-error bg-error-light bg-opacity-10' : ''}
          ${uploadState === UploadState.SUCCESS ? 'border-success bg-success-light bg-opacity-10' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {uploadState === UploadState.SUCCESS ? (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 bg-success-light bg-opacity-30 rounded-full flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <p className="font-medium text-success">Files uploaded successfully</p>
            <div className="mt-2 text-sm text-gray-600 max-w-xs overflow-hidden">
              {fileNames.length === 1 ? (
                <p className="truncate">{fileNames[0]}</p>
              ) : (
                <p>{fileNames.length} files selected</p>
              )}
            </div>
            <p className="mt-2 text-xs text-gray-500">
              Drop more files or click to select additional files
            </p>
          </div>
        ) : uploadState === UploadState.ERROR ? (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 bg-error-light bg-opacity-30 rounded-full flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-error" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <p className="font-medium text-error">Upload Failed</p>
            <p className="text-sm text-error mt-1">{errorMessage}</p>
            <p className="mt-2 text-xs text-gray-500">
              Please try again with valid files
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 bg-primary-light bg-opacity-20 rounded-full flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p className="font-medium text-gray-800">{isDragActive ? 'Drop the files here' : 'Drag & drop files here, or click to select'}</p>
            <p className="text-sm text-gray-500 mt-2">
              {multiple ? 'Upload multiple files at once' : 'Only one file at a time'}
            </p>
            <p className="text-sm text-gray-500 mt-1">Only XML and JSON files supported (Max 5MB per file)</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUploader;