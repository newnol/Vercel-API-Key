import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: '⚖️ Smart Load Balancing',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Tự động phân phối requests đến các Vercel API keys dựa trên credit balance.
        Weighted random selection đảm bảo sử dụng tối ưu tài nguyên.
      </>
    ),
  },
  {
    title: '🔐 API Key Management',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Hệ thống xác thực với rate limiting, expiry dates, và usage tracking.
        Quản lý keys dễ dàng qua CLI hoặc Admin API.
      </>
    ),
  },
  {
    title: '🚀 100% OpenAI Compatible',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Hỗ trợ đầy đủ OpenAI API endpoints với streaming. Drop-in replacement
        cho OpenAI SDK - chỉ cần đổi base URL!
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
