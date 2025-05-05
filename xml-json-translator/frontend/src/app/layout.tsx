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
          <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center">
              <h1 className="text-lg font-semibold text-blue-600">XML Translator</h1>
              <nav>
                <ul className="flex space-x-4">
                  <li>
                    <a 
                      href="https://github.com/yourusername/xml-translator" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-gray-500 hover:text-gray-900"
                    >
                      GitHub
                    </a>
                  </li>
                  <li>
                    <a 
                      href="/api/docs" 
                      target="_blank" 
                      className="text-gray-500 hover:text-gray-900"
                    >
                      API Docs
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </header>
        {children}
        <footer className="bg-white">
          <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            <p className="text-center text-gray-500 text-sm">
              &copy; {new Date().getFullYear()} XML & JSON Translator. All rights reserved.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}