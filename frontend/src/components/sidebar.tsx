"use client";

import { useState } from 'react';
import styles from '../app/home.module.css';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    // Adiciona a classe .collapsed condicionalmente
    <aside className={`${styles.sidebar} ${isCollapsed ? styles.collapsed : ''}`}>
      
     <img
      src="/icons/mdk_com.png" 
      alt="MDK Logo"
      className={styles.logo}
      />

      <nav className={styles.sidebarNav}>
        <ul>
          <li className={`${styles.navItem} ${pathname === '/' ? styles.active : ''}`}>
            <Link href="/" className={styles.sidebarLink} title="Mesas">
              <img src="/icons/home.png" alt="Ícone Home" />
              <span>MESAS</span>
            </Link>
          </li>
          <li className={`${styles.navItem} ${pathname === '/menu' ? styles.active : ''}`}>
            <Link href="/menu" className={styles.sidebarLink} title="Cardápio">
              <img src="/icons/menu.png" alt="Ícone Cardápio" />
              <span>CARDÁPIO</span>
            </Link>
          </li>
          <li className={`${styles.navItem} ${pathname === '/order' ? styles.active : ''}`}>
            <Link href="/order" className={styles.sidebarLink} title="Pedidos">
              <img src="/icons/order.png" alt="Ícone Pedidos" />
              <span>PEDIDOS</span>
            </Link>
          </li>
          <li className={`${styles.navItem} ${pathname === '/payment' ? styles.active : ''}`}>
            <Link href="/payment" className={styles.sidebarLink} title="Pagamento">
              <img src="/icons/payment.png" alt="Ícone Pagamento" />
              <span>PAGAMENTO</span>
            </Link>
          </li>
        </ul>
      </nav>

      {/* Botão para fechar/abrir */}
      <button onClick={toggleSidebar} className={styles.toggleBtn}>
        {isCollapsed ? '➤' : '◀'} 
      </button>
    </aside>
  );
}