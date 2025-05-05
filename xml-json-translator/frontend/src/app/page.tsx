'use client';

import { ToastContainer } from 'react-toastify';
import TranslationForm from '@/components/TranslationForm';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <ToastContainer position="top-right" autoClose={5000} />
      
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            XML & JSON Translator
          </h1>
          <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
            Translate your XML and JSON files from English to multiple languages using advanced machine learning models.
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          <TranslationForm />
        </div>

        <div className="mt-16 max-w-3xl mx-auto">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                How It Works
              </h3>
              <p className="mt-1 max-w-2xl text-sm text-gray-500">
                Learn how to use the translation service effectively.
              </p>
            </div>
            <div className="border-t border-gray-200">
              <dl>
                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">
                    Supported File Types
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    XML and JSON files with text content in English
                  </dd>
                </div>
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">
                    Supported Languages
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    Finnish, Swedish, German, French, Spanish, and more (depending on selected service)
                  </dd>
                </div>
                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">
                    Translation Services
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <ul className="divide-y divide-gray-200">
                      <li className="py-2">
                        <strong>Hugging Face:</strong> Free machine translation using Helsinki-NLP models
                      </li>
                      <li className="py-2">
                        <strong>AWS Bedrock:</strong> Premium translation using Claude AI (requires AWS credentials)
                      </li>
                    </ul>
                  </dd>
                </div>
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">
                    Max File Size
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    5MB
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}