import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        {/* Remove <title> and the broken <link> */}
        {/* Favicon is auto-handled if favicon.ico is in /public */}
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}