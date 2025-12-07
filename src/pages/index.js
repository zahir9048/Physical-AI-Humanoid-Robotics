import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/introduction/why-physical-ai-matters">
            Read the Book
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome`}
      description="Physical AI & Humanoid Robotics Textbook: From Foundations to Embodied Intelligence">
      <HomepageHeader />
      <main>
        <section className={styles.description}>
          <div className="container padding-horiz--md">
            <div className="row">
              <div className="col col--8 col--offset-2">
                <h2>About This Book</h2>
                <p>
                  This comprehensive textbook on Physical AI & Humanoid Robotics provides a structured approach
                  to understanding the intersection of artificial intelligence and embodied systems. The book covers
                  everything from fundamental concepts to advanced implementations in humanoid robotics.
                </p>
                <p>
                  The content is organized in a semester-long curriculum with weekly modules that build upon
                  each other, providing both theoretical foundations and practical applications. Each module
                  includes hands-on exercises, code examples, and real-world case studies.
                </p>
                <p>
                  Topics include kinematics, dynamics, control systems, machine learning for robotics,
                  sensor fusion, computer vision, and embodied AI principles. The book emphasizes practical
                  implementation using modern tools and frameworks while maintaining rigorous theoretical foundations.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}