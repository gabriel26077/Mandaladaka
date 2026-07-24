"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import styles from "./order.module.css";

type OrderItem = {
  product?: { id?: number; name?: string; price?: number } | string;
  quantity: number;
  total_price?: number;
};
type Order = {
  id: number;
  table_number?: number;
  table_id?: number;
  status: string;
  created_at?: string;
  items: OrderItem[];
  total_price?: number;
};

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [activeTab, setActiveTab] = useState<"orders" | "tabs">("orders");
  const [isLoading, setIsLoading] = useState(true);

  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const mockOrders: Order[] = [
    {
      id: 101,
      table_number: 5,
      status: "PENDING",
      items: [{ product: { name: "Hambúrguer Clássico" }, quantity: 2 }],
    },
    {
      id: 102,
      table_number: 3,
      status: "PENDING",
      items: [{ product: { name: "Coca-Cola Zero" }, quantity: 1 }],
    },
  ];

  const fetchData = async () => {
    setIsLoading(true);

    if (!token) {
      setOrders(mockOrders);
      setIsLoading(false);
      return;
    }

    try {
      const resOrders = await fetch("http://localhost:5000/kitchen/orders/pending", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (resOrders.ok) {
        const ordersDataRaw = await resOrders.json();
        const ordersData = (ordersDataRaw || []).map((o: any) => ({
          ...o,
          table_number: o.table_number ?? o.table_id,
          items: o.items || [],
        }));
        setOrders(ordersData);
      } else {
        throw new Error("Erro ao buscar pedidos");
      }
    } catch (err) {
      console.error("Erro na API, carregando mocks para visualização.");
      setOrders(mockOrders);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleStartPreparation = async (orderId: number) => {
    setOrders((prevOrders) => prevOrders.filter((order) => order.id !== orderId));

    if (token) {
      try {
        await fetch(`http://localhost:5000/kitchen/orders/${orderId}/start`, {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
        });
      } catch (error) {
        console.error("Erro de conexão ao iniciar preparo.");
      }
    }
  };

  return (
    <main className={styles.mainContainer}>
      <div className={styles.header}>
        <h1>Gerenciamento de Pedidos</h1>
        <div className={styles.tabSwitcher}>
          <button
            className={`${styles.tabBtn} ${activeTab === "orders" ? styles.active : ""}`}
            onClick={() => setActiveTab("orders")}
          >
            <Image
              src="/icons/kitchen.png"
              alt="Ícone de Cozinha"
              width={20}
              height={20}
              className={styles.tabIcon}
            />
            Cozinha ({orders.length})
          </button>
          <button
            className={`${styles.tabBtn} ${activeTab === "tabs" ? styles.active : ""}`}
            onClick={() => setActiveTab("tabs")}
          >
            <Image
              src="/icons/table.png"
              alt="Ícone de Mesa"
              width={20}
              height={20}
              className={styles.tabIcon}
            />
            Mesas Ocupadas
          </button>
        </div>
      </div>

      <div className={styles.contentArea}>
        {/* AREA DA COZINHA */}
        {activeTab === "orders" && (
          <div className={styles.grid}>
            {isLoading ? (
              <div className={styles.emptyState}>Carregando pedidos...</div>
            ) : orders.length === 0 ? (
              <div className={styles.emptyState}>Tudo limpo na cozinha!</div>
            ) : (
              orders.map((order) => (
                <div key={order.id} className={styles.card}>
                  <div className={styles.cardHeader}>
                    <span className={styles.tableBadge}>Mesa {order.table_number}</span>
                    <span className={styles.timeBadge}># {order.id}</span>
                  </div>
                  <div className={styles.cardBody}>
                    <ul>
                      {order.items.map((item, idx) => {
                        const pName =
                          typeof item.product === "string"
                            ? item.product
                            : item.product?.name || "Item";
                        return (
                          <li key={idx}>
                            <strong>{item.quantity}x</strong> {pName}
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                  <div className={styles.cardFooter}>
                    <button
                      className={styles.btnAction}
                      onClick={() => handleStartPreparation(order.id)}
                    >
                      Iniciar Preparo
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* EM BREVE — MESAS OCUPADAS */}
        {activeTab === "tabs" && (
          <div className={styles.comingSoonWrapper}>
            <div className={styles.comingSoonCard}>
              <Image
                src="/icons/table.png"
                alt="Mesas Ocupadas"
                width={56}
                height={56}
                className={styles.comingSoonIcon}
              />
              <h2 className={styles.comingSoonTitle}>Mesas Ocupadas</h2>
              <p className={styles.comingSoonText}>
                Esta funcionalidade está em desenvolvimento e estará disponível em breve.
              </p>
              <span className={styles.comingSoonBadge}>Em breve</span>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}