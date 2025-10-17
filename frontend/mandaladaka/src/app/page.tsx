"use client";

import { useState } from 'react';
import styles from './home.module.css';

const tablesData = [
  { name: 'T1' }, { name: 'T2' }, { name: 'T3' }, { name: 'T4' }, { name: 'T5' },
  { name: 'T6' }, { name: 'T7' }, { name: 'T8' }, { name: 'T9' }, { name: 'T10' }
];

export default function HomePage() {
  const [selectedTable, setSelectedTable] = useState('T1');
  const [personCount, setPersonCount] = useState(2);

  const handleSelectTable = (tableName: string) => {
    setSelectedTable(tableName);
    setPersonCount(1); 
  };

  const handlePersonCountChange = (amount: number) => {
    setPersonCount(prevCount => Math.max(1, prevCount + amount));
  };

  return (
    <main className={styles.mainContent}>
      <section className={styles.tablesSection}>
        <h2>LISTA DE MESAS</h2>
        <div className={styles.tablesGrid}>
          {tablesData.map((table) => (
            <div
              key={table.name}
              className={`${styles.tableCard} ${selectedTable === table.name ? styles.selected : ''}`}
              onClick={() => handleSelectTable(table.name)}
            >
              <div className={styles.tableCardContent}>
                <img className={styles.tableIcon} src="/icons/hover.png" alt="Mesa" />
                <span className={styles.tableName}>{table.name}</span>
              </div>
              {selectedTable === table.name && (
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
            <span>MESA: <strong>{selectedTable}</strong></span>
            <span>CLIENTES: <strong>{personCount}</strong></span>
          </div>
          <button className={styles.btnConfirm}>CONTINUAR</button>
        </div>
      </section>
    </main>
  );
}