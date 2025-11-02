"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import styles from "./order.module.css";

/* Tipagens */
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
/* Dados Mock */
const MOCK_ORDERS: Order[] = [
  {
    id: 101,
    table_number: 5,
    status: "pending",
    created_at: new Date().toISOString(),
    items: [
      {
        product: { id: 1, name: "Clássico da Casa", price: 24.9 },
        quantity: 2,
        total_price: 49.8,
      },
      {
        product: { id: 19, name: "Refrigerante Lata", price: 6.0 },
        quantity: 1,
        total_price: 6.0,
      },
    ],
    total_price: 55.8,
  },
  {
    id: 102,
    table_number: 2,
    status: "in_progress",
    created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    items: [
      {
        product: { id: 3, name: "Cheddar Melt", price: 27.9 },
        quantity: 1,
        total_price: 27.9,
      },
    ],
    total_price: 27.9,
  },
  {
    id: 103,
    table_number: 10,
    status: "pending",
    created_at: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
    items: [
      {
        product: { id: 4, name: "Duplo Smash", price: 31.9 },
        quantity: 1,
        total_price: 31.9,
      },
      {
        product: { id: 26, name: "Brownie com Sorvete", price: 16.9 },
        quantity: 1,
        total_price: 16.9,
      },
    ],
    total_price: 48.8,
  },
];

export default function OrderPage() {
  const router = useRouter();
  const [pendingOrders, setPendingOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /* Detecta se o mock foi pedido (query string ?mock=1, localStorage, ou env) */
  const shouldUseMock = (): boolean => {
    if (typeof window === "undefined") return false;
    try {
      const params = new URLSearchParams(window.location.search);
      if (params.get("mock") === "1") return true;
    } catch (_) {}
    if (typeof process !== "undefined" && process.env.NEXT_PUBLIC_USE_MOCK === "1")
      return true;
    if (localStorage.getItem("useMockOrders") === "1") return true;
    return false;
  };

  useEffect(() => {
    const fetchPendingOrders = async () => {
      setIsLoading(true);
      setError(null);

      const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
      const useMock = shouldUseMock();

      if (!token && !useMock) {
        // Se não houver token e não estivermos em mock, redireciona pra login
        router.push("/login");
        return;
      }

      try {
        if (useMock) {
          await new Promise((r) => setTimeout(r, 300));
          setPendingOrders(MOCK_ORDERS);
          return;
        }

        const response = await fetch("http://localhost:5000/kitchen/orders/pending", {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.status === 401) {
          router.push("/login");
          return;
        }
        if (!response.ok) {
          // tenta parsear mensagem de erro do back
          const txt = await response.text();
          throw new Error(txt || "Falha ao buscar pedidos pendentes");
        }

        const data: Order[] = await response.json();
        setPendingOrders(data);
      } catch (err) {
        // Se falhar ao acessar o back, CADEIA: tenta usar mock como fallback
        if (err instanceof Error) {
          console.error("Erro buscando pedidos:", err.message);
          // se o back deu erro, ainda assim podemos mostrar mock
          setError("Falha ao buscar pedidos do backend. Usando dados de exemplo.");
          setPendingOrders(MOCK_ORDERS);
        } else {
          setError("Erro desconhecido ao buscar pedidos.");
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchPendingOrders();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router]);

  if (isLoading) {
    return (
      <main className={styles.mainContainer}>
        <h1>Pedidos Pendentes</h1>
        <p>Carregando...</p>
      </main>
    );
  }

  return (
    <main className={styles.mainContainer}>
      <h1>Pedidos Pendentes</h1>

      {error && <p style={{ color: "orange" }}>Aviso: {error}</p>}

      <div className={styles.ordersGrid}>
        {pendingOrders.length === 0 && <p>Nenhum pedido pendente no momento.</p>}

        {pendingOrders.map((order) => (
          <div key={order.id} className={styles.orderCard}>
            <div className={styles.orderCardHeader}>
              <h3>
                Mesa {order.table_number} - Pedido #{order.id}
              </h3>
              <span className={styles.statusPending}>{order.status}</span>
            </div>
            <div className={styles.orderCardBody}>
              <ul>
                {order.items.map((item) => (
                  <li key={item.product.id}>
                    <span>
                      {item.quantity}x {item.product.name}
                    </span>
                    <span>R$ {item.total_price.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
              <div style={{ marginTop: "1rem", fontWeight: 600 }}>
                Total: R$ {Number(order.total_price).toFixed(2)}
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
