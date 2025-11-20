"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import styles from "./order.module.css";

// Tipos (flexíveis para combinar com o que a API pode retornar)
type OrderItem = {
  product?: { id?: number; name?: string; price?: number } | string;
  quantity: number;
  total_price?: number;
};
type OrderStatus = "PENDING" | "IN_PROGRESS" | "READY_FOR_DELIVERY" | "DELIVERED" | string;
type Order = {
  id: number;
  table_number?: number;
  table_id?: number;
  status: OrderStatus;
  created_at?: string;
  items: OrderItem[];
  total_price?: number;
};
type TabStatus = "OCCUPIED" | "FREE" | string;
type TabSummary = {
  id: number;
  status: TabStatus;
  number_of_people: number;
};
type TabDetails = TabSummary & {
  orders: { id: number; items: { product: string; quantity: number }[] }[];
};

export default function OrdersPage() {
  const router = useRouter();

  const [orders, setOrders] = useState<Order[]>([]);
  const [tabs, setTabs] = useState<TabSummary[]>([]);
  const [selectedTab, setSelectedTab] = useState<TabDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // nova: controla qual aba está ativa
  const [activeTab, setActiveTab] = useState<"orders" | "tabs">("orders");

  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const fetchData = async () => {
    setIsLoading(true);
    setError(null);

    if (!token) {
      router.push("/login");
      return;
    }

    try {
      // buscar pedidos pendentes (cozinha) e mesas (garçom) em paralelo
      const [resOrders, resTabs] = await Promise.all([
        fetch("http://localhost:5000/kitchen/orders/pending", {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch("http://localhost:5000/tables", {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      if (resOrders.status === 401 || resTabs.status === 401) {
        router.push("/login");
        return;
      }

      if (!resOrders.ok || !resTabs.ok) {
        throw new Error("Erro ao buscar dados do servidor.");
      }

      const ordersDataRaw = await resOrders.json();
      //_map para adaptar a estrutura esperada (opcional)
      const ordersData: Order[] = (ordersDataRaw || []).map((o: any) => ({
        id: o.id,
        table_number: o.table_number ?? o.table_id ?? o.tableId ?? null,
        status: (o.status || "PENDING").toUpperCase(),
        created_at: o.created_at,
        items: (o.items || []).map((it: any) => ({
          product: it.product ?? it.product_name ?? it.product?.name,
          quantity: it.quantity,
          total_price: it.total_price ?? (it.quantity && it.product?.price ? it.quantity * it.product.price : undefined),
        })),
        total_price: o.total_price,
      }));

      const tabsData: TabSummary[] = await resTabs.json();

      setOrders(ordersData);
      setTabs(tabsData);

      console.log("GET /tables ->", tabsData);
    } catch (err) {
      console.error(err);
      setError("Falha ao buscar dados do servidor. Verifique o backend e o token.");
      setOrders([]);
      setTabs([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router]);

  // Ações
  const handleStatusChange = async (id: number) => {
    if (!token) return;
    try {
      const res = await fetch(`http://localhost:5000/kitchen/orders/${id}/start`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Falha ao iniciar preparo.");
      alert(`Pedido #${id} iniciado.`);
      fetchData();
    } catch (err) {
      console.error(err);
      alert("Erro ao iniciar preparo.");
    }
  };

  const handleGoToPayment = (tableId: number) => {
    if (!token) {
      router.push("/login");
      return;
    }

    router.push(`/payment?table=${tableId}`);
  };

  const handleOpenTabDetails = async (tab: TabSummary) => {
    if (!token) {
      router.push("/login");
      return;
    }

    try {
      const res = await fetch(`http://localhost:5000/tables/${tab.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        alert(`Erro ao buscar detalhes da comanda. Status: ${res.status}`);
        throw new Error(`Erro ao buscar detalhes: ${res.status}`);
      }

      const details: TabDetails = await res.json();
      setSelectedTab(details);
    } catch (err) {
      console.error(err);
      alert("Falha ao buscar pedidos da comanda.");
    }
  };

  const handleNewOrder = (tableId: number, clients: number) => {
    router.push(`/menu?table=${tableId}&clients=${clients}`);
  };

  // filtros helpers
  const occupiedTabs = tabs.filter((t) => (t.status || "").toString().toUpperCase() === "OCCUPIED");

  if (isLoading)
    return (
      <main className={styles.mainContainer}>
        <h1>Carregando Pedidos e Mesas...</h1>
      </main>
    );

  return (
    <main className={styles.mainContainer}>
      <div className={styles.headerRow} style={{ marginBottom: "1rem", alignItems: "center" }}>
        <h1>Painel — Pedidos & Comandas</h1>

        {/* ABAS */}
        <div style={{ display: "flex", gap: 8 }}>
          <button
            className={`${styles.filterBtn} ${activeTab === "orders" ? styles.filterBtnActive : ""}`}
            onClick={() => setActiveTab("orders")}
          >
            Pedidos em aberto ({orders.length})
          </button>
          <button
            className={`${styles.filterBtn} ${activeTab === "tabs" ? styles.filterBtnActive : ""}`}
            onClick={() => setActiveTab("tabs")}
          >
            Comandas ({occupiedTabs.length})
          </button>
        </div>
      </div>

      {error && <p style={{ color: "red", fontWeight: 600 }}>{error}</p>}

      {/* ABAS: ORDERS */}
      {activeTab === "orders" && (
        <>
          <h2>🍲 Pedidos Pendentes ({orders.length})</h2>
          <div className={styles.ordersGrid}>
            {orders.length === 0 ? (
              <p>Nenhum pedido pendente na cozinha.</p>
            ) : (
              orders.map((order) => (
                <div key={order.id} className={styles.orderCard}>
                  <div className={styles.orderCardHeader}>
                    <h3>Mesa {order.table_number ?? order.table_id ?? "—"} - Pedido #{order.id}</h3>
                    <span className={`${styles.statusTag} ${styles.statusPending}`}>Pendente</span>
                  </div>
                  <div className={styles.orderCardBody}>
                    <ul>
                      {order.items.map((item, idx) => {
                        const productName = typeof item.product === "string" ? item.product : item.product?.name ?? "Produto";
                        const price = item.total_price ?? 0;
                        return (
                          <li key={idx}>
                            <span>{item.quantity}x {productName}</span>
                            <span>R$ {price.toFixed ? price.toFixed(2) : price}</span>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                  <div className={styles.orderCardActions}>
                    <button onClick={() => handleStatusChange(order.id)} className={styles.btnPrimary}>
                      Iniciar preparo
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}

      {/* ABAS: COMANDAS / MESAS */}
      {activeTab === "tabs" && (
        <>
          <h2 style={{ marginTop: "1.5rem" }}>🛎️ Mesas Ocupadas ({occupiedTabs.length})</h2>
          <div className={styles.ordersGrid}>
            {occupiedTabs.length === 0 ? (
              <p>Nenhuma mesa ocupada no momento.</p>
            ) : (
              occupiedTabs.map((tab) => (
                <div
                  key={tab.id}
                  className={styles.orderCard}
                  style={{ cursor: "pointer" }}
                  onClick={() => handleOpenTabDetails(tab)}
                >
                  <div className={styles.orderCardHeader}>
                    <h3>Mesa {tab.id}</h3>
                    <span className={`${styles.statusTag} ${styles.statusInProgress}`}>
                      Ocupada ({tab.number_of_people} pessoas)
                    </span>
                  </div>

                  <div className={styles.orderCardBody}>
                    <p>Status: <strong>Ocupada</strong></p>
                    <p style={{ marginTop: "0.5rem", fontWeight: 500 }}>
                      Capacidade: {tab.number_of_people} pessoas.
                    </p>
                  </div>

                  <div className={styles.orderCardActions}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleGoToPayment(tab.id);
                      }}
                      className={styles.btnCancel}
                    >
                      Ir para Pagamento
                    </button>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleNewOrder(tab.id, tab.number_of_people);
                      }}
                      className={styles.btnSuccess}
                    >
                      + Adicionar Pedido
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}

      {/* MODAL DE DETALHES DA COMANDA */}
      {selectedTab && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0,0,0,0.6)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
          onClick={() => setSelectedTab(null)}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: "30px",
              borderRadius: "12px",
              width: "90%",
              maxWidth: "500px",
              maxHeight: "80vh",
              overflowY: "auto",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
              <h2>Comanda da Mesa {selectedTab.id}</h2>
              <button onClick={() => setSelectedTab(null)} style={{ border: "none", background: "none", fontSize: "1.5rem", cursor: "pointer" }}>
                &times;
              </button>
            </div>

            <h3 style={{ marginBottom: "1rem", borderBottom: "1px solid #eee", paddingBottom: "0.5rem" }}>Pedidos Atuais:</h3>

            {selectedTab.orders.length === 0 ? (
              <p>Nenhum pedido nesta comanda.</p>
            ) : (
              selectedTab.orders.map((order) => (
                <div key={order.id} style={{ marginBottom: "1rem", padding: "10px", border: "1px solid #ddd", borderRadius: "8px" }}>
                  <strong>Pedido #{order.id}</strong>
                  <ul style={{ listStyle: "none", paddingLeft: "10px", marginTop: "5px" }}>
                    {order.items.map((item, index) => (
                      <li key={index} style={{ display: "flex", justifyContent: "space-between" }}>
                        <span>{item.quantity}x {item.product}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))
            )}

            <p style={{ marginTop: "1.5rem", fontStyle: "italic", color: "#555" }}>
              Total: se quiser, posso adicionar um cálculo somando preços (preciso do endpoint de produtos ou preço nos itens).
            </p>

            <div className={styles.orderCardActions} style={{ marginTop: "2rem" }}>
              {selectedTab.status === "OCCUPIED" ? (
                <>
                  <button
                    onClick={() => {
                      handleNewOrder(selectedTab.id, selectedTab.number_of_people);
                    }}
                    className={styles.btnSuccess}
                  >
                    + Criar Novo Pedido
                  </button>
                  <button
                    onClick={() => {
                      handleGoToPayment(selectedTab.id);
                      setSelectedTab(null);
                    }}
                    className={styles.btnCancel}
                  >
                    Ir para pagamento
                  </button>
                </>
              ) : (
                <span style={{ color: "#777" }}>Mesa Livre.</span>
              )}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
