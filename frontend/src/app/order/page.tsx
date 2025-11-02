"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import styles from './order.module.css';

type OrderItem = {
  product: {
    id: number;
    name: string;
    price: number;
  };
  quantity: number;
  total_price: number;
};

type Order = {
  id: number;
  table_number: number;
  status: string;
  created_at: string;
  items: OrderItem[];
  total_price: number;
};

export default function OrderPage() {
  const router = useRouter();
  const [pendingOrders, setPendingOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Lógica para buscar os pedidos pendentes
  useEffect(() => {
    const fetchPendingOrders = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      try {
        // 1. Chama a API da Cozinha
        const response = await fetch('http://localhost:5000/kitchen/orders/pending', {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${token}` },
        });

        if (response.status === 401) {
          router.push('/login');
          return;
        }
        if (!response.ok) {
          throw new Error('Falha ao buscar pedidos pendentes');
        }

        const data: Order[] = await response.json();
        setPendingOrders(data); // 2. Salva os pedidos no estado

      } catch (err) {
        if (err instanceof Error) setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPendingOrders();
  }, [router]);

  if (isLoading) {
    return <main className={styles.mainContainer}><h1>Pedidos Pendentes</h1><p>Carregando...</p></main>;
  }

  if (error) {
    return <main className={styles.mainContainer}><h1>Pedidos Pendentes</h1><p style={{ color: 'red' }}>Erro: {error}</p></main>;
  }

  return (
    <main className={styles.mainContainer}>
      <h1>Pedidos Pendentes</h1>

      <div className={styles.ordersGrid}>
        {pendingOrders.length === 0 && (
          <p>Nenhum pedido pendente no momento.</p>
        )}

        {/* Mapeia e exibe cada pedido em um card */}
        {pendingOrders.map((order) => (
          <div key={order.id} className={styles.orderCard}>
            <div className={styles.orderCardHeader}>
              <h3>Mesa {order.table_number} - Pedido #{order.id}</h3>
              <span className={styles.statusPending}>{order.status}</span>
            </div>
            <div className={styles.orderCardBody}>
              <ul>
                {order.items.map((item) => (
                  <li key={item.product.id}>
                    <span>{item.quantity}x {item.product.name}</span>
                    <span>R$ {item.total_price.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}