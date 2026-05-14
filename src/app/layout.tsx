import { PolicyEngineShell } from "@policyengine/ui-kit/layout";
import "@policyengine/ui-kit/styles.css";

import type { Metadata, Viewport } from 'next';
import './globals.css';

const SITE_URL = 'https://uk-2024-manifestos-comparison.vercel.app';
const TITLE = 'UK 2024 manifestos comparison | PolicyEngine';
const DESCRIPTION =
  'Compare the societal and household-level impacts of the Conservative, Labour and Liberal Democrat 2024 UK election manifestos.';

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: TITLE,
  description: DESCRIPTION,
  keywords: [
    'UK manifestos',
    '2024 UK election',
    'Conservative',
    'Labour',
    'Liberal Democrat',
    'PolicyEngine',
    'tax and benefits',
  ],
  authors: [{ name: 'PolicyEngine' }],
  alternates: { canonical: SITE_URL },
  openGraph: {
    type: 'website',
    title: TITLE,
    description: DESCRIPTION,
    url: SITE_URL,
    siteName: 'PolicyEngine',
  },
  twitter: {
    card: 'summary_large_image',
    title: TITLE,
    description: DESCRIPTION,
    site: '@ThePolicyEngine',
  },
};

export const viewport: Viewport = {
  themeColor: '#2C6496',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <PolicyEngineShell country="uk">{children}        </PolicyEngineShell>
      </body>
    </html>
  );
}
