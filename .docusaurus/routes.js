import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/physical-ai-textbook/__docusaurus/debug',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug', '1b0'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/config',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/config', '4ef'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/content',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/content', '02c'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/globalData',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/globalData', '58f'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/metadata',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/metadata', '647'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/registry',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/registry', '125'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/__docusaurus/debug/routes',
    component: ComponentCreator('/physical-ai-textbook/__docusaurus/debug/routes', 'aa1'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/search',
    component: ComponentCreator('/physical-ai-textbook/search', '400'),
    exact: true
  },
  {
    path: '/physical-ai-textbook/docs',
    component: ComponentCreator('/physical-ai-textbook/docs', '0c1'),
    routes: [
      {
        path: '/physical-ai-textbook/docs',
        component: ComponentCreator('/physical-ai-textbook/docs', '7c9'),
        routes: [
          {
            path: '/physical-ai-textbook/docs',
            component: ComponentCreator('/physical-ai-textbook/docs', 'd60'),
            routes: [
              {
                path: '/physical-ai-textbook/docs/additional-resources',
                component: ComponentCreator('/physical-ai-textbook/docs/additional-resources', 'b62'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/glossary',
                component: ComponentCreator('/physical-ai-textbook/docs/glossary', 'b3c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/hardware-requirements',
                component: ComponentCreator('/physical-ai-textbook/docs/hardware-requirements', '265'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/introduction/why-physical-ai-matters',
                component: ComponentCreator('/physical-ai-textbook/docs/introduction/why-physical-ai-matters', '857'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-1/week-1',
                component: ComponentCreator('/physical-ai-textbook/docs/module-1/week-1', 'e85'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-1/week-2',
                component: ComponentCreator('/physical-ai-textbook/docs/module-1/week-2', '0e4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-2/week-3',
                component: ComponentCreator('/physical-ai-textbook/docs/module-2/week-3', '8af'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-2/week-4',
                component: ComponentCreator('/physical-ai-textbook/docs/module-2/week-4', 'ef1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-2/week-5',
                component: ComponentCreator('/physical-ai-textbook/docs/module-2/week-5', 'd7a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-3/week-6',
                component: ComponentCreator('/physical-ai-textbook/docs/module-3/week-6', '5de'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-3/week-7',
                component: ComponentCreator('/physical-ai-textbook/docs/module-3/week-7', 'b2b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-4/week-10',
                component: ComponentCreator('/physical-ai-textbook/docs/module-4/week-10', '889'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-4/week-8',
                component: ComponentCreator('/physical-ai-textbook/docs/module-4/week-8', '969'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-4/week-9',
                component: ComponentCreator('/physical-ai-textbook/docs/module-4/week-9', 'faa'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-5/week-11',
                component: ComponentCreator('/physical-ai-textbook/docs/module-5/week-11', '382'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-5/week-12',
                component: ComponentCreator('/physical-ai-textbook/docs/module-5/week-12', 'be3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-6/capstone-project',
                component: ComponentCreator('/physical-ai-textbook/docs/module-6/capstone-project', '2e5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/module-6/week-13',
                component: ComponentCreator('/physical-ai-textbook/docs/module-6/week-13', 'f42'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/physical-ai-textbook/docs/prerequisites-setup',
                component: ComponentCreator('/physical-ai-textbook/docs/prerequisites-setup', 'c0b'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/physical-ai-textbook/',
    component: ComponentCreator('/physical-ai-textbook/', '014'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
