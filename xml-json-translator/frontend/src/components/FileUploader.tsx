import { useCallback, useState } from 'react';
import { useDropzone, FileRejection, DropEvent } from 'react-dropzone';
import { UploadState } from '@/types';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
  accept: Record<string, string[]>;
  maxSize?: number;
}

const FileUploader = ({ onFileSelect, accept, maxSize = 5 * 1024 * 1024 }: FileUploaderProps) => {
  const [uploadState, setUploadState] = useState<UploadState>(UploadState.IDLE);
  const [fileName, setFileName] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setFileName(file.name);
      setUploadState(UploadState.SUCCESS);
      setErrorMessage('');
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const onDropRejected = useCallback((fileRejections: FileRejection[], event: DropEvent) => {
    const rejection = fileRejections[0];
    let message = 'File upload failed';
    
    if (rejection?.errors?.length > 0) {
      const error = rejection.errors[0];
      if (error.code === 'file-too-large') {
        message = `File is too large. Max size is ${maxSize / (1024 * 1024)}MB`;
      } else if (error.code === 'file-invalid-type') {
        message = 'Invalid file type. Please select an XML or JSON file';
      } else {
        message = error.message;
      }
    }
    
    setErrorMessage(message);
    setUploadState(UploadState.ERROR);
  }, [maxSize]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    onDropRejected,
    accept,
    maxSize,
    multiple: false
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-6 cursor-pointer transition-all duration-200 text-center
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'}
          ${uploadState === UploadState.ERROR ? 'border-red-500 bg-red-50' : ''}
          ${uploadState === UploadState.SUCCESS ? 'border-green-500 bg-green-50' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {uploadState === UploadState.SUCCESS ? (
          <div className="flex flex-col items-center">
            <svg className="w-12 h-12 text-green-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <p className="font-medium">File uploaded successfully</p>
            <p className="text-sm text-gray-600 mt-1">{fileName}</p>
          </div>
        ) : uploadState === UploadState.ERROR ? (
          <div className="flex flex-col items-center">
            <svg className="w-12 h-12 text-red-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
            <p className="font-medium text-red-600">Upload Failed</p>
            <p className="text-sm text-red-600 mt-1">{errorMessage}</p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <svg className="w-12 h-12 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="font-medium">{isDragActive ? 'Drop the file here' : 'Drag & drop file here, or click to select'}</p>
            <p className="text-sm text-gray-500 mt-1">Only XML and JSON files supported (Max 5MB)</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUploader;