import Head from 'next/head'; // Import from next/head
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>SPEC GEN</title>
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;