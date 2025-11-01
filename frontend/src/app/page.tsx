"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from './home.module.css'; 
import { mockTables } from './tables.mock';

type Table = {
  id: number;
  status: 'available' | 'occupied';
  number_of_people: number;
};

export default function HomePage() {
  const router = useRouter();
  const [tables, setTables] = useState<Table[]>(mockTables);
  

  const [selectedTable, setSelectedTable] = useState<number | null>(null);
  const [personCount, setPersonCount] = useState(1);

  const handleSelectTable = (tableId: number) => {
    setSelectedTable(tableId);
    setPersonCount(1); 
  };

  const handlePersonCountChange = (amount: number) => {
    setPersonCount(prevCount => Math.max(1, prevCount + amount));
  };

  const handleContinue = () => {
    if (selectedTable && personCount > 0) {
      router.push(`/menu?table=${selectedTable}&clients=${personCount}`);
    }
  };

  return (
    <main className={styles.mainContent}>
      <section className={styles.tablesSection}>
        <h2>LISTA DE MESAS</h2>
        <div className={styles.tablesGrid}>
          {tables.map((table) => (
            <div
              key={table.id}
              className={`${styles.tableCard} ${selectedTable === table.id ? styles.selected : ''}`}
              onClick={() => handleSelectTable(table.id)}
            >
              <div className={styles.tableCardContent}>
                <img className={styles.tableIcon} src="/icons/hover.png" alt="Mesa" />
                <span className={styles.tableName}>T{table.id}</span>
              </div>
              {selectedTable === table.id && (
                <div className={styles.personCounter}>
                  <button onClick={(e) => { e.stopPropagation(); handlePersonCountChange(-1); }} className={styles.counterBtn}>-</button>
                  <span className={styles.personCount}>{personCount}</span>
                  <button onClick={(e) => { e.stopPropagation(); handlePersonCountChange(1); }} className={styles.counterBtn}>+</button>
                </div>
              )}
            </div>
          ))}
        </div>
        <div className={styles.tablesFooter}>
          <div className={styles.selectionSummary}>
            <span>MESA: <strong>T{selectedTable}</strong></span>
            <span>CLIENTES: <strong>{personCount}</strong></span>
          </div>
          <button onClick={handleContinue} className={styles.btnConfirm} disabled={!selectedTable}>
            CONTINUAR
          </button>
        </div>
      </section>
    </main>
  );
}