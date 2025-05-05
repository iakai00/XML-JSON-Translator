'use client';

import { ToastContainer } from 'react-toastify';
import TranslationForm from '@/components/TranslationForm';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100">
      <ToastContainer position="top-right" autoClose={5000} />
      
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-800 sm:text-5xl pb-2 relative">
            XML & JSON Translator
            <span className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-24 h-1 bg-primary"></span>
          </h1>
          <p className="mt-5 max-w-2xl mx-auto text-xl text-gray-600">
            Translate your XML and JSON files from English to multiple languages with advanced machine learning.
          </p>
        </div>

        <TranslationForm />

        <div className="mt-16 max-w-5xl mx-auto">
          <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200 bg-gray-50">
              <h3 className="text-xl leading-6 font-semibold text-gray-900">
                How It Works
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Learn how to use the translation service effectively.
              </p>
            </div>
            <div className="px-6 py-5 divide-y divide-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 py-4">
                <div className="col-span-1 flex flex-col items-center text-center px-4">
                  <div className="w-16 h-16 bg-primary-light bg-opacity-20 text-primary rounded-full flex items-center justify-center mb-3">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <h4 className="text-lg font-medium text-gray-900">1. Upload Files</h4>
                  <p className="mt-2 text-sm text-gray-500">Upload your XML or JSON files containing English text.</p>
                </div>
                <div className="col-span-1 flex flex-col items-center text-center px-4">
                  <div className="w-16 h-16 bg-secondary-light bg-opacity-20 text-secondary rounded-full flex items-center justify-center mb-3">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                    </svg>
                  </div>
                  <h4 className="text-lg font-medium text-gray-900">2. Choose Settings</h4>
                  <p className="mt-2 text-sm text-gray-500">Select your target language and preferred translation service.</p>
                </div>
                <div className="col-span-1 flex flex-col items-center text-center px-4">
                  <div className="w-16 h-16 bg-success-light bg-opacity-20 text-success rounded-full flex items-center justify-center mb-3">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </div>
                  <h4 className="text-lg font-medium text-gray-900">3. Download Results</h4>
                  <p className="mt-2 text-sm text-gray-500">Get your translated files with preserved structure and formatting.</p>
                </div>
              </div>

              <div className="py-5">
                <h4 className="text-lg font-medium text-gray-900 mb-2">Features</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="flex items-start">
                    <svg className="flex-shrink-0 h-5 w-5 text-success mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="ml-2 text-sm text-gray-600">Preserves XML/JSON structure and IDs</p>
                  </div>
                  <div className="flex items-start">
                    <svg className="flex-shrink-0 h-5 w-5 text-success mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="ml-2 text-sm text-gray-600">Bulk translation of multiple files</p>
                  </div>
                  <div className="flex items-start">
                    <svg className="flex-shrink-0 h-5 w-5 text-success mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="ml-2 text-sm text-gray-600">HTML tag and attribute preservation</p>
                  </div>
                  <div className="flex items-start">
                    <svg className="flex-shrink-0 h-5 w-5 text-success mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="ml-2 text-sm text-gray-600">Supports multiple translation engines</p>
                  </div>
                  <div className="flex items-start">
                    <svg className="flex-shrink-0 h-5 w-5 text-success mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="ml-2 text-sm text-gray-600">Placeholder preservation (e.g., __name__)</p>
                  </div>
                  <div className="flex items-start">
                    <svg className="flex-shrink-0 h-5 w-5 text-success mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="ml-2 text-sm text-gray-600">CDATA section handling</p>
                  </div>
                </div>
              </div>

              <div className="py-5">
                <h4 className="text-lg font-medium text-gray-900 mb-2">Supported Languages</h4>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-y-2 gap-x-4">
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-primary mr-2"></div>
                    <span className="text-sm text-gray-600">Finnish</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-primary mr-2"></div>
                    <span className="text-sm text-gray-600">Swedish</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-primary mr-2"></div>
                    <span className="text-sm text-gray-600">German</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-primary mr-2"></div>
                    <span className="text-sm text-gray-600">French</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-primary mr-2"></div>
                    <span className="text-sm text-gray-600">Spanish</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-primary mr-2"></div>
                    <span className="text-sm text-gray-600">Italian</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-secondary mr-2"></div>
                    <span className="text-sm text-gray-600">Japanese</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-secondary mr-2"></div>
                    <span className="text-sm text-gray-600">Chinese</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-secondary mr-2"></div>
                    <span className="text-sm text-gray-600">And more...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}