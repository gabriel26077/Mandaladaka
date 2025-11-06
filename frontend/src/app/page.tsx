"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import styles from './home.module.css'; 


type Table = {
  id: number;
  status: 'available' | 'occupied';
  number_of_people: number;
};

export default function HomePage() {
  const router = useRouter();

  const [tables, setTables] = useState<Table[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedTable, setSelectedTable] = useState<number | null>(null);
  const [personCount, setPersonCount] = useState(1);

  // LÓGICA PARA BUSCAR AS MESAS DA API
  useEffect(() => {
    const fetchTables = async () => {
      // 1.1. Pega o token salvo no login
      const token = localStorage.getItem('access_token');

      if (!token) {
        // Se não tem token, chuta o usuário para a tela de login
        router.push('/login');
        return;
      }

      try {
        // 1.2. Chama a API de mesas
        const response = await fetch('http://localhost:5000/tables', {
          method: 'GET',
          headers: {
            // 1.3. Envia o token para provar que estamos logados
            'Authorization': `Bearer ${token}`
          },
        });

        if (response.status === 401) {
          // Se o token for inválido/expirado
          setError("Sessão expirada. Por favor, faça login novamente.");
          localStorage.removeItem('access_token');
          router.push('/login');
          return;
        }

        if (!response.ok) {
          throw new Error('Falha ao buscar as mesas');
        }

        const data: Table[] = await response.json();
        setTables(data); // 1.4. Salva as mesas REAIS no estado

      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('Um erro inesperado ocorreu.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchTables();
  }, [router]);

  const handleContinue = async () => {
    if (!selectedTable || personCount <= 0) return;

    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }

    try {
      // 2.1. CHAMA A API PARA "ABRIR" A MESA
      const response = await fetch(`http://localhost:5000/tables/${selectedTable}/open`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          number_of_people: personCount // Envia o n de pessoas
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.description || 'Não foi possível abrir a mesa');
      }
      
      // 2.2. Se deu certo, navega para o menu
      router.push(`/menu?table=${selectedTable}&clients=${personCount}`);

    } catch (err) {
       if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Um erro inesperado ocorreu.');
      }
    }
  };
  
  const handleSelectTable = (tableId: number) => {
    setSelectedTable(tableId);
    setPersonCount(1); 
  };

  const handlePersonCountChange = (amount: number) => {
    setPersonCount(prevCount => Math.max(1, prevCount + amount));
  };
  
  if (isLoading) {
    return <main className={styles.mainContent}><p>Carregando mesas...</p></main>;
  }

  return (
    <main className={styles.mainContent}>
      <section className={styles.tablesSection}>
        <h2>LISTA DE MESAS</h2>
        
        {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
        
        <div className={styles.tablesGrid}>
          {tables.map((table) => (
            <div
              key={table.id}
              // Adiciona classe 'occupied' se a mesa estiver ocupada
              className={`
                ${styles.tableCard} 
                ${selectedTable === table.id ? styles.selected : ''}
                ${table.status === 'occupied' ? styles.occupied : ''}
              `}
              onClick={() => handleSelectTable(table.id)}
            >
              <div className={styles.tableCardContent}>
                <img className={styles.tableIcon} src="/icons/hover.png" alt="Mesa" />
                <span className={styles.tableName}>T{table.id}</span>
                {/* Mostra se a mesa está ocupada */}
                {table.status === 'occupied' && (
                  <span className={styles.occupiedText}>
                    ({table.number_of_people} pessoas)
                  </span>
                )}
              </div>
              {selectedTable === table.id && table.status === 'available' && (
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