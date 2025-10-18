"use client";

import { useState, useEffect } from 'react';
import styles from '../app/home.module.css';

export default function Header() {
  const [currentDateTime, setCurrentDateTime] = useState<Date | null>(null);

  useEffect(() => {
    setCurrentDateTime(new Date());

    const timer = setInterval(() => {
      setCurrentDateTime(new Date());
    }, 60000);

    return () => clearInterval(timer);
  }, []);

  const formattedDateTime = currentDateTime?.toLocaleString('pt-BR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <header className={styles.appHeader}>
      <div className={styles.searchBar}>
        <input type="text" placeholder="Procure por produto ou pedido" />
        <img src="/icons/search.png" alt="Pesquisar" />
      </div>

      <div className={styles.headerActions}>
        <span className={styles.dateTime}>
          {formattedDateTime || 'Carregando...'}
        </span>
      </div>
    </header>
  );
}