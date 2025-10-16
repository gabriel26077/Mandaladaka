import styles from '../app/home.module.css';

export default function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <h1 className={styles.logo}>MDK</h1>
      <nav className={styles.sidebarNav}>
        <ul>
          <li className={`${styles.navItem} ${styles.active}`}>
            <a href="#"><img src="/icons/home.png" alt="Ícone Home" /><span>HOME</span></a>
          </li>
          <li className={styles.navItem}>
            <a href="#"><img src="/icons/menu.png" alt="Ícone Cardápio" /><span>CARDÁPIO</span></a>
          </li>
          <li className={styles.navItem}>
            <a href="#"><img src="/icons/payment.png" alt="Ícone Pagamento" /><span>PAGAMENTO</span></a>
          </li>
          <li className={styles.navItem}>
            <a href="#"><img src="/icons/order.png" alt="Ícone Pedidos" /><span>PEDIDOS</span></a>
          </li>
          <li className={styles.navItem}>
            <a href="#"><img src="/icons/settings.png" alt="Ícone Configurações" /><span>CONFIGURAÇÕES</span></a>
          </li>
        </ul>
      </nav>
    </aside>
  );
}