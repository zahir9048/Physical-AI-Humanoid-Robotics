import { themes as prismThemes } from 'prism-react-renderer';

const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'From Foundations to Embodied Intelligence',
  favicon: 'img/favicon.ico',

  url: 'https://zahir9048.github.io',
  baseUrl: '/Physical-AI-Humanoid-Robotics/',

  organizationName: 'zahir9048', // Usually your GitHub org/user name.
  projectName: 'physical-ai-textbook', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/zahir9048/Physical-AI-Humanoid-Robotics/tree/001-build-comprehensive-textbook/',
          remarkPlugins: [require('remark-mermaid')],
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themes: [
    // ... Your other themes.
    [
      '@easyops-cn/docusaurus-search-local',
      {
        // ... your options
        hashed: true,
        language: ['en'],
        removeDefaultStopWordFilter: false,
        highlightSearchTermsOnTargetPage: true,
      },
    ],
  ],


  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics Textbook',
        logo: {
          alt: 'Physical AI Textbook Logo',
          src: 'img/pic.jpg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Tutorial',
          },
          {
            type: 'search',
            position: 'right',
          },
          {
            href: 'https://github.com/zahir9048/Physical-AI-Humanoid-Robotics',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Tutorial',
                to: '/docs/introduction/why-physical-ai-matters',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/zahir9048/Physical-AI-Humanoid-Robotics',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
