"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import styles from "./order.module.css";

// Tipos de Dados (Adaptados para o consumo da API real)
type OrderItem = {
  product: { id: number; name: string; price: number; };
  quantity: number;
  total_price: number;
};
type OrderStatus = "pending" | "in_progress" | "ready" | "delivered";
type Order = {
  id: number;
  table_number: number;
  status: OrderStatus;
  created_at: string;
  items: OrderItem[];
  total_price: number;
};
type TabStatus = "OCCUPIED" | "FREE"; // Tipos de status da API /tables
type TabSummary = { // Corresponde ao retorno do GET /tables
  id: number;
  status: TabStatus;
  number_of_people: number;
};
// Tipo detalhado da Comanda (retorno do GET /tables/<table_id>)
type TabDetails = TabSummary & {
  orders: { id: number; items: { product: string; quantity: number }[] }[];
};


// ======================================================================
// COMPONENTE PRINCIPAL
// ======================================================================

export default function OrdersPage() {
  const router = useRouter();

  const [orders, setOrders] = useState<Order[]>([]);
  const [tabs, setTabs] = useState<TabSummary[]>([]); // Mesas
  
  const [selectedTab, setSelectedTab] = useState<TabDetails | null>(null); 
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);


  /* ======= FUNÇÃO DE BUSCA DE DADOS (REAL) - COM LOG DE DEPURACAO ======= */
  const fetchData = async () => {
    setIsLoading(true);
    setError(null);
    const token = localStorage.getItem("access_token");

    if (!token) {
      router.push("/login");
      return;
    }

    try {
      // 1. Busca Pedidos Pendentes (Kitchen API)
      const resOrders = await fetch("http://localhost:5000/kitchen/orders/pending", { 
        headers: { Authorization: `Bearer ${token}` },
      });

      // 2. Busca Comandas/Mesas (Waiter API)
      const resTabs = await fetch("http://localhost:5000/tables", { 
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!resOrders.ok || !resTabs.ok) {
         if (resOrders.status === 401 || resTabs.status === 401) {
            router.push("/login");
            return;
         }
         throw new Error("Erro ao buscar dados do servidor.");
      }
      
      const ordersData: Order[] = await resOrders.json();
      setOrders(ordersData);
      
      const tabsData: TabSummary[] = await resTabs.json(); //
      setTabs(tabsData);
      
      // LOG CRÍTICO: Verifique o console do navegador
      console.log("Resposta GET /tables:", tabsData); 

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
  }, [router]);

  /* ======= LÓGICAS DE AÇÃO (Simplificadas) ======= */

  const handleStatusChange = async (id: number) => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    try {
      // POST /kitchen/orders/<order_id>/start
      const res = await fetch(`http://localhost:5000/kitchen/orders/${id}/start`, { 
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) throw new Error("Falha ao iniciar preparo no servidor.");

      alert(`Pedido #${id} iniciado. Removido da lista de pendentes.`);
      fetchData(); 

    } catch (err) {
      console.error(err);
      alert("Erro ao comunicar com o servidor para iniciar preparo.");
    }
  };

  const handleDelete = (id: number) => {
    alert(`Excluir Pedido #${id} (Ação não mapeada na API).`);
  };

  const handleCloseTab = async (tableId: number) => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }

    try {
      // POST /tables/<table_id>/close
      const res = await fetch(`http://localhost:5000/tables/${tableId}/close`, { 
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) throw new Error(`Erro ao fechar comanda: ${res.status}.`);

      alert(`Mesa ${tableId} foi fechada (liberada) com sucesso!`);
      fetchData(); 

    } catch (err) {
      console.error(err);
      alert("Falha ao fechar a mesa. Verifique o servidor.");
    }
  };

  const handleOpenTabDetails = async (tab: TabSummary) => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }

    try {
        // GET /tables/<table_id>
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


  /* ======= RENDERIZAÇÃO ======= */

  // Mesas que estão ocupadas. (Filtro reforçado para maiúsculas)
  const occupiedTabs = tabs.filter(t => t.status.toUpperCase() === 'OCCUPIED');

  if (isLoading)
    return (
      <main className={styles.mainContainer}>
        <h1>Carregando Pedidos e Mesas...</h1>
      </main>
    );

  return (
    <main className={styles.mainContainer}>
      <div className={styles.headerRow} style={{ marginBottom: '2rem' }}>
        <h1>Painel de Pedidos e Mesas Abertas</h1>
      </div>

      {error && <p style={{ color: "red", fontWeight: 600 }}>{error}</p>}

      {/* ========================================= */}
      {/* SEÇÃO 1: PEDIDOS PENDENTES (COZINHA) */}
      {/* ========================================= */}
      <h2>🍲 Pedidos Pendentes ({orders.length})</h2>
      <div className={styles.ordersGrid}>
        {orders.length === 0 ? (
          <p>Nenhum pedido pendente na cozinha.</p>
        ) : (
          orders.map((order) => (
            <div key={order.id} className={styles.orderCard}>
              <div className={styles.orderCardHeader}>
                <h3>Mesa {order.table_number} - Pedido #{order.id}</h3>
                <span className={`${styles.statusTag} ${styles.statusPending}`}>Pendente</span>
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
              <div className={styles.orderCardActions}>
                <button
                  onClick={() => handleStatusChange(order.id)}
                  className={styles.btnPrimary}
                >
                  Iniciar preparo
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* ========================================= */}
      {/* SEÇÃO 2: MESAS ABERTAS (GARÇOM MVP) */}
      {/* ========================================= */}
      <h2 style={{ marginTop: '3rem' }}>🛎️ Mesas Ocupadas ({occupiedTabs.length})</h2>
      <div className={styles.ordersGrid}>
        {occupiedTabs.length === 0 ? (
          <p>Nenhuma mesa ocupada no momento.</p>
        ) : (
          occupiedTabs.map((tab) => (
            <div key={tab.id} className={styles.orderCard} style={{ cursor: 'pointer' }} onClick={() => handleOpenTabDetails(tab)}>
              <div className={styles.orderCardHeader}>
                <h3>Mesa {tab.id}</h3>
                <span className={`${styles.statusTag} ${styles.statusInProgress}`}>
                  Ocupada ({tab.number_of_people} pessoas)
                </span>
              </div>

              <div className={styles.orderCardBody}>
                <p>Status: **Ocupada** desde a abertura da comanda.</p>
                <p style={{marginTop: '0.5rem', fontWeight: 500}}>
                    Capacidade: {tab.number_of_people} pessoas.
                </p>
              </div>

              <div className={styles.orderCardActions}>
                {/* Botão de Fechar Comanda */}
                <button
                  onClick={(e) => { 
                    e.stopPropagation(); // Evita abrir o modal
                    handleCloseTab(tab.id);
                  }}
                  className={styles.btnCancel}
                >
                  Fechar Mesa/Comanda
                </button>
                {/* Botão para ir ao Cardápio e adicionar pedido */}
                <button
                    onClick={(e) => {
                        e.stopPropagation(); // Evita abrir o modal
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
      
      {/* MODAL DE DETALHES (Mantido, mas precisa do GET /tables/<id> funcionar) */}
      {/* ... (O código do Modal permanece o mesmo do bloco anterior) ... */}
      {selectedTab && (
        <div 
          style={{
            position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
            backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', justifyContent: 'center',
            alignItems: 'center', zIndex: 1000 
          }}
          onClick={() => setSelectedTab(null)}
        >
          <div 
            style={{
              backgroundColor: 'white', padding: '30px', borderRadius: '12px',
              width: '90%', maxWidth: '500px', maxHeight: '80vh', overflowY: 'auto',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h2>Comanda da Mesa {selectedTab.id}</h2>
              <button onClick={() => setSelectedTab(null)} style={{ border: 'none', background: 'none', fontSize: '1.5rem', cursor: 'pointer' }}>
                &times;
              </button>
            </div>

            <h3 style={{ marginBottom: '1rem', borderBottom: '1px solid #eee', paddingBottom: '0.5rem' }}>Pedidos Atuais:</h3>
            
            {selectedTab.orders.length === 0 ? (
                <p>Nenhum pedido nesta comanda.</p>
            ) : (
                selectedTab.orders.map((order) => (
                    <div key={order.id} style={{ marginBottom: '1rem', padding: '10px', border: '1px solid #ddd', borderRadius: '8px' }}>
                        <strong>Pedido #{order.id}</strong>
                        <ul style={{ listStyle: 'none', paddingLeft: '10px', marginTop: '5px' }}>
                            {order.items.map((item, index) => (
                                <li key={index} style={{ display: 'flex', justifyContent: 'space-between' }}>
                                    <span>{item.quantity}x {item.product}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))
            )}
            
            <p style={{ marginTop: '1.5rem', fontStyle: 'italic', color: '#555' }}>
              Total: Seria necessário calcular ou buscar em outro endpoint.
            </p>

            <div className={styles.orderCardActions} style={{ marginTop: '2rem' }}>
              {selectedTab.status === "OCCUPIED" ? (
                  <>
                      <button 
                        onClick={() => handleNewOrder(selectedTab.id, selectedTab.number_of_people)}
                        className={styles.btnSuccess}
                      >
                        + Criar Novo Pedido
                      </button>
                      <button
                        onClick={() => {
                          handleCloseTab(selectedTab.id);
                          setSelectedTab(null);
                        }}
                        className={styles.btnCancel}
                      >
                        Fechar Comanda
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