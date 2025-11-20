"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import styles from "./order.module.css";

// Tipos
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
type TabSummary = {
  id: number;
  status: string;
  number_of_people: number;
};

export default function OrdersPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [tabs, setTabs] = useState<TabSummary[]>([]);
  const [activeTab, setActiveTab] = useState<"orders" | "tabs">("orders");
  const [isLoading, setIsLoading] = useState(true);

  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const mockOrders: Order[] = [
    { 
      id: 101, 
      table_number: 5, 
      status: "PENDING", 
      items: [{ product: { name: "Hambúrguer Clássico" }, quantity: 2 }] 
    },
    { 
      id: 102, 
      table_number: 3, 
      status: "PENDING", 
      items: [{ product: { name: "Coca-Cola Zero" }, quantity: 1 }] 
    }
  ];

  const mockTabs: TabSummary[] = [
    { id: 1, status: "OCCUPIED", number_of_people: 2 },
    { id: 5, status: "OCCUPIED", number_of_people: 4 },
    { id: 8, status: "OCCUPIED", number_of_people: 1 },
  ];

  const fetchData = async () => {
    setIsLoading(true);
    
    // Se não tiver token ou Backend fora, usa Mock direto para teste visual
    if (!token) { 
        console.log("Sem token ou teste visual, carregando mocks...");
        setOrders(mockOrders);
        setTabs(mockTabs);
        setIsLoading(false);
        return;
    }

    try {
      const [resOrders, resTabs] = await Promise.all([
        fetch("http://localhost:5000/kitchen/orders/pending", { headers: { Authorization: `Bearer ${token}` } }),
        fetch("http://localhost:5000/tables", { headers: { Authorization: `Bearer ${token}` } }),
      ]);

      if (resOrders.ok && resTabs.ok) {
        const ordersDataRaw = await resOrders.json();
        const tabsData = await resTabs.json();
        
        const ordersData = (ordersDataRaw || []).map((o: any) => ({
            ...o,
            table_number: o.table_number ?? o.table_id,
            items: o.items || []
        }));

        setOrders(ordersData);
        setTabs(tabsData);
      } else {
        throw new Error("Backend com erro 500 ou 400");
      }
    } catch (err) {
      console.error("Erro na API, carregando MOCKS para visualização do design.");
      // FALLBACK: Carrega os dados de mentira para o design aparecer
      setOrders(mockOrders);
      setTabs(mockTabs);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleGoToPayment = (tableId: number) => {
    router.push(`/payment?table=${tableId}`);
  };

  const occupiedTabs = tabs.filter((t) => (t.status || "").toString().toUpperCase() === "OCCUPIED");

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
            Mesas Ocupadas ({occupiedTabs.length})
          </button>
        </div>
      </div>

      <div className={styles.contentArea}>
        {/* AREA DA COZINHA */}
        {activeTab === "orders" && (
          <div className={styles.grid}>
            {orders.length === 0 ? (
               <div className={styles.emptyState}>
                 <p>Tudo limpo na cozinha!</p>
               </div>
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
                         const pName = typeof item.product === 'string' ? item.product : item.product?.name || "Item";
                         return (
                            <li key={idx}>
                                <strong>{item.quantity}x</strong> {pName}
                            </li>
                         )
                      })}
                    </ul>
                  </div>
                  <div className={styles.cardFooter}>
                    <button className={styles.btnAction}>Iniciar Preparo</button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* AREA DAS MESAS / COMANDAS */}
        {activeTab === "tabs" && (
          <div className={styles.grid}>
            {occupiedTabs.length === 0 ? (
               <div className={styles.emptyState}>Nenhuma mesa aberta.</div>
            ) : (
              occupiedTabs.map((tab) => (
                <div key={tab.id} className={`${styles.card} ${styles.cardTable}`}>
                  <div className={styles.cardHeader}>
                    <span className={styles.tableBigTitle}>Mesa {tab.id}</span>
                    <span className={styles.peopleBadge}>
                      <Image
                        src="/icons/guess.png" 
                        alt="Pessoas"
                        width={16}
                        height={16}
                      />
                      {tab.number_of_people}
                     </span>
                  </div>
                  
                  <div className={styles.cardBody}>
                    <p className={styles.statusText}>Status: <strong>Ocupada</strong></p>
                    <p className={styles.instructionText}>Cliente aguardando ou consumindo.</p>
                  </div>

                  <div className={styles.cardFooter}>
                    <button 
                        onClick={() => handleGoToPayment(tab.id)}
                        className={styles.btnPay}
                    >
                        Fechar & Pagar
                    </button>
                    <button 
                        className={styles.btnAdd}
                        onClick={() => router.push(`/menu?table=${tab.id}&clients=${tab.number_of_people}`)}
                    >
                        + Pedido
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </main>
  );
}