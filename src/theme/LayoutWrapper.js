import React from 'react';
import Layout from '@theme/Layout';
import { useLocation, useHistory } from '@docusaurus/router';
import { useLocaleContext } from '@docusaurus/theme-common';
import ChatWidget from '../components/Chatbot/ChatWidget';

// Custom layout wrapper to handle RTL direction for Urdu
export default function LayoutWrapper(props) {
  const location = useLocation();
  const history = useHistory();
  const { locale } = useLocaleContext();

  // Set direction attribute based on locale
  React.useEffect(() => {
    const isUrdu = locale === 'ur';
    document.documentElement.dir = isUrdu ? 'rtl' : 'ltr';

    // Add class to body for CSS targeting if needed
    if (isUrdu) {
      document.body.classList.add('locale-urdu');
    } else {
      document.body.classList.remove('locale-urdu');
    }

    return () => {
      document.body.classList.remove('locale-urdu');
    };
  }, [locale]);

  return (
    <>
      <Layout {...props} />
      <ChatWidget />
    </>
  );
}