/**
 * Creating a sidebar enables you to:
 - Create an ordered group of docs
 - Render a sidebar in the docs site
 - List the contents of the sidebar in the docs category
 - `createSidebarItems` as a function or object
 */

module.exports = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      link: {
        type: 'doc',
        id: 'introduction/why-physical-ai-matters',
      },
      items: [
        'introduction/why-physical-ai-matters',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: Foundations',
      items: [
        'module-1/week-1',
        'module-1/week-2',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: ROS 2 Fundamentals',
      items: [
        'module-2/week-3',
        'module-2/week-4',
        'module-2/week-5',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Robot Simulation with Gazebo',
      items: [
        'module-3/week-6',
        'module-3/week-7',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: NVIDIA Isaac Platform',
      items: [
        'module-4/week-8',
        'module-4/week-9',
        'module-4/week-10',
      ],
    },
    {
      type: 'category',
      label: 'Module 5: Humanoid Robot Development',
      items: [
        'module-5/week-11',
        'module-5/week-12',
      ],
    },
    {
      type: 'category',
      label: 'Module 6: Conversational Robotics and Capstone Project',
      items: [
        'module-6/week-13',
        'module-6/capstone-project',
      ],
    },
    {
      type: 'category',
      label: 'Hardware & Setup',
      items: [
        'hardware-requirements',
        'prerequisites-setup',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
        'glossary',
        'additional-resources',
      ],
    },
  ],
};
