import './globals.css';
import styles from './home.module.css';
import Sidebar from '../components/sidebar';
import Header from '../components/header';

export const metadata = {
  title: 'MDK - Sistema de Pedidos',
  description: 'Sistema de gestão de pedidos e mesas para restaurantes.',
  icons: {
    icon: '/favicon.ico', 
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-br">
      <body>
        <div className={styles.appContainer}>
          <Sidebar />
          <Header />
          {children}
        </div>
      </body>
    </html>
  );
}