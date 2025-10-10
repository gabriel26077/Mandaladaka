import styles from '../app/home.module.css';

export default function Header() {
  return (
    <header className={styles.appHeader}>
      <div className={styles.searchBar}>
        <input type="text" placeholder="Procure por produto ou pedido" />
      </div>
      <div className={styles.headerActions}>
        <span className={styles.dateTime}>18 de Outubro 2025, 10:00AM</span>
        <button className={styles.btnAddTable}>+ ADD MESA</button>
      </div>
    </header>
  );
}