"use client";

import './globals.css';
import styles from './home.module.css';
import Sidebar from '../components/sidebar';
import Header from '../components/header';
import { usePathname } from 'next/navigation';


export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isLoginPage = pathname === '/login';

  if (isLoginPage) {
    return (
      <html lang="pt-br">
        <body>
          {children}
        </body>
      </html>
    );
  }
  
  return (
    <html lang="pt-br">
      <body>
        <div className={styles.appContainer}>
          <Sidebar />
          <Header />
          <main className={styles.mainContent}> 
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}