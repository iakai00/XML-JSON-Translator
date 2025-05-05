import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import 'react-toastify/dist/ReactToastify.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'XML & JSON Translator',
  description: 'Translate XML and JSON files from English to multiple languages',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center py-4 px-4 sm:px-6 lg:px-8">
              <div className="flex items-center">
                <svg className="h-8 w-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                </svg>
                <h1 className="ml-2 text-xl font-bold text-primary">
                  XML Translator
                </h1>
              </div>
            </div>
          </div>
        </header>
        
        {children}
        
        <footer className="bg-white border-t border-gray-200">
          <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            <p className="text-center text-base text-gray-400">
              &copy; {new Date().getFullYear()} XML & JSON Translator. All rights reserved.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}