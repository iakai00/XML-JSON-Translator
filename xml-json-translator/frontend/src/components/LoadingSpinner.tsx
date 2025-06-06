import React from 'react';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  className?: string;
  message?: string;
}

const LoadingSpinner = ({ 
  size = 'medium', 
  className = '', 
  message = 'Processing...' 
}: LoadingSpinnerProps) => {
  
  const sizeClasses = {
    small: 'h-5 w-5',
    medium: 'h-10 w-10',
    large: 'h-16 w-16',
  };
  
  return (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      <div className={`${sizeClasses[size]}`}>
        <svg
          className="animate-spin text-primary"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          width="100%"
          height="100%"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      </div>
      {message && (
        <p className="mt-3 text-center text-sm font-medium text-gray-600">{message}</p>
      )}
    </div>
  );
};

export default LoadingSpinner;