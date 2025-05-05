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
      small: 'h-4 w-4 border-2',
      medium: 'h-8 w-8 border-3',
      large: 'h-12 w-12 border-4',
    };
    
    return (
      <div className={`flex flex-col items-center justify-center ${className}`}>
        <div 
          className={`animate-spin rounded-full border-solid border-blue-500 border-t-transparent ${sizeClasses[size]}`} 
        />
        {message && (
          <p className="mt-2 text-sm text-gray-600">{message}</p>
        )}
      </div>
    );
  };
  
  export default LoadingSpinner;