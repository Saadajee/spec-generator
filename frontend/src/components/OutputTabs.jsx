// src/components/OutputTabs.jsx
import { Tab } from '@headlessui/react';
import { cn } from '@/utils/classnames'; // Optional helper, see below
import SectionDisplay from './SectionDisplay';

const sections = [
  { key: 'modules', title: 'Modules & Features', dataKey: ['modules', 'features_by_module'] },
  { key: 'stories', title: 'User Stories', dataKey: 'user_stories' },
  { key: 'api', title: 'API Endpoints', dataKey: 'api_endpoints' },
  { key: 'db', title: 'Database Schema', dataKey: 'db_schema' },
  { key: 'questions', title: 'Open Questions', dataKey: 'open_questions' },
];

export default function OutputTabs({ spec }) {
  return (
    <Tab.Group as="div" className="w-full">
      <Tab.List className="flex flex-wrap sm:flex-nowrap gap-2 sm:gap-0 sm:space-x-1 border-b-2 border-industrial-700 mb-8 sm:mb-10">
        {sections.map((section) => (
          <Tab
            key={section.key}
            className={({ selected }) =>
              cn(
                'px-4 sm:px-6 py-3 font-mono text-xs sm:text-sm font-bold tracking-wider transition-colors duration-200',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-industrial-accent focus-visible:ring-offset-2 focus-visible:ring-offset-industrial-900',
                selected
                  ? 'text-industrial-900 bg-industrial-accent shadow-md'
                  : 'text-industrial-500 hover:text-industrial-accent hover:bg-industrial-800'
              )
            }
          >
            {section.title}
          </Tab>
        ))}
      </Tab.List>

      <Tab.Panels className="mt-4">
        {sections.map((section) => (
          <Tab.Panel
            key={section.key}
            className="focus-visible:outline-none"
          >
            {Array.isArray(section.dataKey) ? (
              <>
                <SectionDisplay title="Modules" data={spec?.modules} />
                <div className="mt-12">
                  <SectionDisplay title="Features by Module" data={spec?.features_by_module} />
                </div>
              </>
            ) : (
              <SectionDisplay title={section.title} data={spec?.[section.dataKey]} />
            )}
          </Tab.Panel>
        ))}
      </Tab.Panels>
    </Tab.Group>
  );
}