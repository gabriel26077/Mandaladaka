import styles from './home.module.css';

function TableCard({ name, isSelected = false }: { name: string, isSelected?: boolean }) {
  const cardClasses = isSelected
    ? `${styles.tableCard} ${styles.selected}`
    : styles.tableCard;

  return (
    <div className={cardClasses}>
      <div className={styles.tableCardContent}>
        <img className={styles.tableIcon} src="/icons/hover.png" alt="Mesa" />
        <span className={styles.tableName}>{name}</span>
      </div>
      {isSelected && (
        <div className={styles.personCounter}>
          <button className={styles.counterBtn}>-</button>
          <span className={styles.personCount}>2</span>
          <button className={styles.counterBtn}>+</button>
        </div>
      )}
    </div>
  );
}

export default function HomePage() {
  return (
    <main className={styles.mainContent}>
      <section className={styles.tablesSection}>
        <h2>LISTA DE MESAS</h2>
        <div className={styles.tablesGrid}>
          <TableCard name="T1" isSelected={true} />
          <TableCard name="T2" />
          <TableCard name="T3" />
          <TableCard name="T4" />
          <TableCard name="T5" />
          <TableCard name="T6" />
          <TableCard name="T7" />
          <TableCard name="T8" />
          <TableCard name="T9" />
          <TableCard name="T10" />
        </div>
        <div className={styles.tablesFooter}>
          <div className={styles.selectionSummary}>
            <span>MESA: <strong>1</strong></span>
            <span>CLIENTES: <strong>2</strong></span>
          </div>
          <button className={styles.btnConfirm}>CONTINUAR</button>
        </div>
      </section>

      <section className={styles.orderSection}>
        <div className={styles.orderHeader}>
          <h2>PEDIDO #</h2>
          <div className={styles.orderInfo}>
            <span><img src="/icons/guess.png" alt="Ícone Cliente" />CLIENTE</span>
            <span><img src="/icons/table.png" alt="Ícone Mesa" />MESA</span>
          </div>
        </div>
        <div className={styles.orderBodyEmpty}>
          <img src="/icons/empty-order-icon.png" alt="Pedido Vazio" />
          <p>PEDIDO VAZIO</p>
        </div>
      </section>
    </main>
  );
}