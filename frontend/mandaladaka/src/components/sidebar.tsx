"use client";

import styles from '../app/home.module.css';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className={styles.sidebar}>
      <img
        src="/icons/mdk_com.png"
        alt="MDK Logo"
        className={styles.logo}
      />

      <nav className={styles.sidebarNav}>
        <ul>
          <li className={`${styles.navItem} ${pathname === '/' ? styles.active : ''}`}>
            <Link href="/" className={styles.sidebarLink}>
              <img src="/icons/home.png" alt="Ícone Home" />
              <span>HOME</span>
            </Link>
          </li>
          <li className={`${styles.navItem} ${pathname === '/menu' ? styles.active : ''}`}>
            <Link href="/menu" className={styles.sidebarLink}>
              <img src="/icons/menu.png" alt="Ícone Cardápio" />
              <span>CARDÁPIO</span>
            </Link>
          </li>
          <li className={`${styles.navItem} ${pathname === '/payment' ? styles.active : ''}`}>
            <Link href="/payment" className={styles.sidebarLink}>
              <img src="/icons/payment.png" alt="Ícone Pagamento" />
              <span>PAGAMENTO</span>
            </Link>
          </li>
          <li className={`${styles.navItem} ${pathname === '/order' ? styles.active : ''}`}>
            <Link href="/order" className={styles.sidebarLink}>
              <img src="/icons/order.png" alt="Ícone Pedidos" />
              <span>PEDIDOS</span>
            </Link>
          </li>
          <li className={`${styles.navItem} ${pathname === '/settings' ? styles.active : ''}`}>
            <Link href="/settings" className={styles.sidebarLink}>
              <img src="/icons/settings.png" alt="Ícone Configurações" />
              <span>CONFIGURAÇÕES</span>
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}