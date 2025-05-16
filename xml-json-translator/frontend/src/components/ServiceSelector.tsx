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
    id: 'claude',
    name: 'Claude AI',
    description: 'Premium translation using Claude AI (requires API key)',
    icon: (
      <svg className="h-6 w-6 text-gray-600" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z" />
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