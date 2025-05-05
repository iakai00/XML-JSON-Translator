import React from 'react';
import { TranslatedFile } from '@/types';

interface FileCardProps {
  file: TranslatedFile;
}

const FileCard = ({ file }: FileCardProps) => {
  const fileExtension = file.originalName.split('.').pop()?.toLowerCase();
  const isXml = fileExtension === 'xml';
  const isJson = fileExtension === 'json';
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-200">
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-start">
          <div className={`
            flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center mr-3
            ${isXml ? 'bg-primary-light bg-opacity-20 text-primary' : ''}
            ${isJson ? 'bg-secondary-light bg-opacity-20 text-secondary' : ''}
          `}>
            {isXml && (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9l-3 3m0 0l3 3m-3-3h8" />
              </svg>
            )}
            {isJson && (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            )}
          </div>
          <div className="overflow-hidden">
            <h3 className="text-sm font-semibold text-gray-900 truncate">{file.translatedName}</h3>
            <p className="text-xs text-gray-500 mt-1">From: {file.originalName}</p>
            <div className="flex items-center mt-1">
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-light bg-opacity-20 text-primary-dark">
                {file.targetLanguage.toUpperCase()}
              </span>
              <span className="text-xs text-gray-500 ml-2">
                {formatDate(file.timestamp)}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div className="px-4 py-3 bg-gray-50 flex justify-between items-center">
        <a
          href={file.downloadUrl}
          download={file.translatedName}
          className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          <svg className="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Download
        </a>
        
        <button
          type="button"
          onClick={() => {
            const element = document.createElement("a");
            element.href = file.downloadUrl;
            element.download = file.translatedName;
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
          }}
          className="text-xs text-gray-500 hover:text-primary"
        >
          Quick Download
        </button>
      </div>
    </div>
  );
};

export default FileCard;