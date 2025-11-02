"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import styles from "./order.module.css";

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
  status: "pending" | "in_progress" | "ready" | "delivered";
  created_at: string;
  items: OrderItem[];
  total_price: number;
};

//dados mock
const MOCK_ORDERS: Order[] = [
  {
    id: 101,
    table_number: 5,
    status: "pending",
    created_at: new Date().toISOString(),
    items: [
      { product: { id: 1, name: "Clássico da Casa", price: 24.9 }, quantity: 2, total_price: 49.8 },
      { product: { id: 19, name: "Refrigerante Lata", price: 6.0 }, quantity: 1, total_price: 6.0 },
    ],
    total_price: 55.8,
  },
  {
    id: 102,
    table_number: 2,
    status: "in_progress",
    created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    items: [
      { product: { id: 3, name: "Cheddar Melt", price: 27.9 }, quantity: 1, total_price: 27.9 },
    ],
    total_price: 27.9,
  },
  {
    id: 103,
    table_number: 10,
    status: "ready",
    created_at: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
    items: [
      { product: { id: 4, name: "Duplo Smash", price: 31.9 }, quantity: 1, total_price: 31.9 },
      { product: { id: 26, name: "Brownie com Sorvete", price: 16.9 }, quantity: 1, total_price: 16.9 },
    ],
    total_price: 48.8,
  },
];

export default function OrderPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const shouldUseMock = (): boolean => {
    if (typeof window === "undefined") return false;
    const params = new URLSearchParams(window.location.search);
    if (params.get("mock") === "1") return true;
    if (localStorage.getItem("useMockOrders") === "1") return true;
    if (process.env.NEXT_PUBLIC_USE_MOCK === "1") return true;
    return false;
  };

  useEffect(() => {
    const fetchOrders = async () => {
      setIsLoading(true);
      setError(null);

      const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
      const useMock = shouldUseMock();

      if (!token && !useMock) {
        router.push("/login");
        return;
      }

      try {
        if (useMock) {
          await new Promise((r) => setTimeout(r, 300));
          setOrders(MOCK_ORDERS);
          return;
        }

        const res = await fetch("http://localhost:5000/kitchen/orders/pending", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.status === 401) {
          router.push("/login");
          return;
        }

        if (!res.ok) throw new Error("Falha ao buscar pedidos");

        const data: Order[] = await res.json();
        setOrders(data);
      } catch (err) {
        console.error(err);
        setError("Falha ao buscar pedidos. Usando dados de exemplo.");
        setOrders(MOCK_ORDERS);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOrders();
  }, [router]);

  const handleStatusChange = (id: number, newStatus: Order["status"]) => {
    setOrders((prev) =>
      prev.map((order) =>
        order.id === id ? { ...order, status: newStatus } : order
      )
    );
  };

  const handleDelete = (id: number) => {
    setOrders((prev) => prev.filter((order) => order.id !== id));
  };

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
      <h1>Pedidos</h1>
      {error && <p style={{ color: "orange" }}>{error}</p>}

      <div className={styles.ordersGrid}>
        {orders.length === 0 ? (
          <p>Nenhum pedido no momento.</p>
        ) : (
          orders.map((order) => (
            <div key={order.id} className={styles.orderCard}>
              <div className={styles.orderCardHeader}>
                <h3>
                  Mesa {order.table_number} - Pedido #{order.id}
                </h3>
                <span
                  className={`${styles.statusTag} ${
                    order.status === "pending"
                      ? styles.statusPending
                      : order.status === "in_progress"
                      ? styles.statusInProgress
                      : order.status === "ready"
                      ? styles.statusReady
                      : styles.statusDelivered
                  }`}
                >
                  {order.status}
                </span>
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
                  Total: R$ {order.total_price.toFixed(2)}
                </div>
              </div>

              <div className={styles.orderCardActions}>
                {order.status === "pending" && (
                  <button
                    onClick={() => handleStatusChange(order.id, "in_progress")}
                    className={styles.btnPrimary}
                  >
                    Iniciar preparo
                  </button>
                )}
                {order.status === "in_progress" && (
                  <button
                    onClick={() => handleStatusChange(order.id, "ready")}
                    className={styles.btnSuccess}
                  >
                    Marcar como pronto
                  </button>
                )}
                {order.status === "ready" && (
                  <button
                    onClick={() => handleStatusChange(order.id, "delivered")}
                    className={styles.btnDelivered}
                  >
                    Entregue
                  </button>
                )}
                <button
                  onClick={() => handleDelete(order.id)}
                  className={styles.btnCancel}
                >
                  Excluir
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </main>
  );
}
