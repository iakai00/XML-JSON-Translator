import { TranslationService } from '@/types';
import { RadioGroup } from '@headlessui/react';

interface ServiceSelectorProps {
  value: TranslationService;
  onChange: (value: TranslationService) => void;
}

const services = [
  {
    id: 'huggingface',
    name: 'Hugging Face',
    description: 'Free machine translation using Helsinki-NLP models',
    icon: (
      <svg className="h-6 w-6 text-gray-600" viewBox="0 0 24 24" fill="currentColor">
        <path d="M10.682 16.942H8.855v-4.705h1.827v4.705zm0-5.35H8.855V9.402h1.827v2.19zm4.464 5.35h-1.827v-4.705h1.827v4.705zm0-5.35h-1.827V9.402h1.827v2.19z" />
        <path d="M22 4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V4zm-4 12.942c0 .584-.474 1.058-1.058 1.058H7.058A1.058 1.058 0 0 1 6 16.942V7.058C6 6.474 6.474 6 7.058 6h9.884C17.526 6 18 6.474 18 7.058v9.884z" />
      </svg>
    ),
  },
  {
    id: 'bedrock',
    name: 'AWS Bedrock',
    description: 'Premium translation using Claude AI (requires AWS credentials)',
    icon: (
      <svg className="h-6 w-6 text-gray-600" viewBox="0 0 24 24" fill="currentColor">
        <path d="M7.64 5.92v9.48c0 1.1.9 2 2 2h4.71c1.1 0 2-.9 2-2V5.92c0-.98-.71-1.8-1.67-1.95C14.11 3.87 12.53 4 12 4s-2.11-.13-2.67-.03c-.97.15-1.69.98-1.69 1.95z" />
        <path d="M21.65 10.97a.979.979 0 0 0-1.05.23l-2.84 2.84-1.41-1.41a.996.996 0 0 0-1.41 0c-.39.39-.39 1.02 0 1.41l2.12 2.12c.39.39 1.02.39 1.41 0l3.54-3.54c.39-.39.39-1.03-.01-1.41-.17-.19-.43-.28-.7-.24zM14.92 21.96c-1 .05-2.07.04-3.08-.04h-.01c-1.07-.09-1.98-.81-2.23-1.84-.19-.79-.31-1.62-.35-2.5h9.53c.02-.17.03-.35.03-.52V7.16c0-.17-.01-.35-.03-.52h-9.53c.04-.88.16-1.71.35-2.5.25-1.03 1.16-1.75 2.23-1.84h.01c1.07-.09 2.21-.09 3.37 0 1.07.09 1.98.81 2.23 1.84.19.79.31 1.62.35 2.5h2.04c-.16-4.19-2.5-6.27-6.7-6.27h-.08c-4.23 0-6.65 2.09-6.65 6.68v9.88c0 4.59 2.43 6.68 6.65 6.68h.08c4.2 0 6.53-2.08 6.7-6.27H17.5c-.04.88-.16 1.71-.35 2.5-.25 1.03-1.16 1.75-2.23 1.84z" />
      </svg>
    ),
  },
];

const ServiceSelector = ({ value, onChange }: ServiceSelectorProps) => {
  return (
    <div className="w-full">
      <RadioGroup value={value} onChange={onChange}>
        <RadioGroup.Label className="text-sm font-medium text-gray-700 mb-2">
          Select Translation Service
        </RadioGroup.Label>
        <div className="space-y-2">
          {services.map((service) => (
            <RadioGroup.Option
              key={service.id}
              value={service.id}
              className={({ checked }) =>
                `relative flex cursor-pointer rounded-lg px-5 py-4 focus:outline-none
                ${checked ? 'bg-primary-light bg-opacity-15 border border-primary' : 'bg-white border border-gray-200 hover:bg-gray-50'}`
              }
            >
              {({ checked }) => (
                <div className="flex w-full items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">{service.icon}</div>
                    <div className="ml-3">
                      <RadioGroup.Label
                        as="p"
                        className={`font-medium ${checked ? 'text-primary-dark' : 'text-gray-900'}`}
                      >
                        {service.name}
                      </RadioGroup.Label>
                      <RadioGroup.Description
                        as="span"
                        className={`inline text-sm ${checked ? 'text-primary' : 'text-gray-500'}`}
                      >
                        {service.description}
                      </RadioGroup.Description>
                    </div>
                  </div>
                  <div
                    className={`flex-shrink-0 ${checked ? 'text-primary' : 'text-gray-400'}`}
                  >
                    <div className={`h-6 w-6 rounded-full border-2 ${checked ? 'border-primary bg-primary' : 'border-gray-300'} flex items-center justify-center`}>
                      {checked && (
                        <div className="h-2 w-2 rounded-full bg-white"></div>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </RadioGroup.Option>
          ))}
        </div>
      </RadioGroup>
    </div>
  );
};

export default ServiceSelector;