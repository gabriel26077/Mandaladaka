"use client";

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import styles from './payment.module.css';

interface Item {
    product: string | { name: string; price: number; category?: string };
    quantity: number;
    price_at_order?: number;
}

interface Order {
    id: number;
    items: Item[];
    status: string;
}

interface TableDetails {
    id: number;
    status: string;
    number_of_people: number;
    orders: Order[];
}

function PaymentContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const tableId = searchParams.get('table');

    const [tableData, setTableData] = useState<TableDetails | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [paymentMethod, setPaymentMethod] = useState<'money' | 'card' | 'pix'>('money');
    const [cashReceived, setCashReceived] = useState<string>("");

    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

    useEffect(() => {
        if (!tableId || !token) return;

        const fetchTable = async () => {
            setIsLoading(true);
            try {
                const res = await fetch(`http://localhost:5000/tables/${tableId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    setTableData(data);
                }
            } catch (error) {
                console.error("Erro ao buscar mesa", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchTable();
    }, [tableId, token]);

    const calculateTotal = () => {
        if (!tableData) return { subtotal: 0, service: 0, total: 0 };

        let subtotal = 0;

        tableData.orders.forEach(order => {
            if (order.status === 'CANCELLED') return;

            order.items.forEach(item => {
                let price = 0;
                if (item.price_at_order) {
                    price = item.price_at_order;
                } else if (typeof item.product !== 'string' && item.product.price) {
                    price = item.product.price;
                } else {
                    price = 0; 
                }
                subtotal += price * item.quantity;
            });
        });

        const service = subtotal * 0.10;
        return {
            subtotal,
            service,
            total: subtotal + service
        };
    };

    const { subtotal, service, total } = calculateTotal();
    const change = parseFloat(cashReceived) - total;

    const handleFinalizePayment = async () => {
        if (!confirm("Confirmar pagamento e fechar mesa?")) return;

        try {
            const res = await fetch(`http://localhost:5000/tables/${tableId}/close`, {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` }
            });

            if (res.ok) {
                alert("Pagamento realizado com sucesso!");
                router.push('/');
            } else {
                alert("Erro ao fechar mesa.");
            }
        } catch (err) {
            alert("Erro de conexão.");
        }
    };

    if (!tableId) return <div className={styles.container}>Selecione uma mesa na tela de Pedidos.</div>;
    if (isLoading) return <div className={styles.container}>Carregando dados da mesa...</div>;

    return (
        <main className={styles.container}>
            <div className={styles.header}>
                <h1>PEDIDO / MESA #: {tableId}</h1>
            </div>

            <div className={styles.contentGrid}>
                <div className={styles.itemsList}>
                    <div className={styles.tableHeader}>
                        <span>Item</span>
                        <span style={{textAlign: 'center'}}>Preço</span>
                        <span style={{textAlign: 'center'}}>Qtd</span>
                        <span style={{textAlign: 'right'}}>Subtotal</span>
                    </div>

                    {tableData?.orders.map(order => (
                        order.items.map((item, idx) => {
                             const pName = typeof item.product === 'string' ? item.product : item.product.name;
                             const pPrice = (typeof item.product !== 'string' ? item.product.price : item.price_at_order) || 0;
                             const pCat = typeof item.product !== 'string' ? item.product.category : 'Geral';
                             
                             return (
                                <div key={`${order.id}-${idx}`} className={styles.itemRow}>
                                    <div className={styles.itemName}>
                                        <strong>{pName}</strong>
                                        <span className={styles.itemCategory}>{pCat}</span>
                                    </div>
                                    <div style={{textAlign: 'center'}}>R$ {pPrice.toFixed(2)}</div>
                                    <div style={{textAlign: 'center'}}>{item.quantity}</div>
                                    <div style={{textAlign: 'right', fontWeight: 600}}>
                                        R$ {(pPrice * item.quantity).toFixed(2)}
                                    </div>
                                </div>
                             );
                        })
                    ))}
                    
                    {tableData?.orders.length === 0 && <p>Nenhum pedido encontrado.</p>}
                </div>

                <div className={styles.paymentPanel}>
                    <div className={styles.totalDisplay}>
                        <h2>TOTAL A PAGAR</h2>
                        <div className={styles.bigPrice}>R$ {total.toFixed(2)}</div>
                    </div>

                    <div className={styles.paymentMethods}>
                        <button 
                            className={`${styles.methodBtn} ${paymentMethod === 'money' ? styles.active : ''}`}
                            onClick={() => setPaymentMethod('money')}
                        >
                            <span>💵</span> Dinheiro
                        </button>
                        <button 
                            className={`${styles.methodBtn} ${paymentMethod === 'card' ? styles.active : ''}`}
                            onClick={() => setPaymentMethod('card')}
                        >
                            <span>💳</span> Cartão
                        </button>
                        <button 
                            className={`${styles.methodBtn} ${paymentMethod === 'pix' ? styles.active : ''}`}
                            onClick={() => setPaymentMethod('pix')}
                        >
                            <span>💠</span> Pix
                        </button>
                    </div>

                    {paymentMethod === 'money' && (
                        <div className={styles.inputGroup}>
                            <label>RECEBIDO</label>
                            <div style={{display: 'flex', alignItems: 'center'}}>
                                <span>R$</span>
                                <input 
                                    type="number" 
                                    className={styles.moneyInput}
                                    placeholder="0.00"
                                    value={cashReceived}
                                    onChange={(e) => setCashReceived(e.target.value)}
                                />
                            </div>
                        </div>
                    )}

                    <div className={styles.summary}>
                        <div className={styles.summaryRow}>
                            <span>Subtotal</span>
                            <span>R$ {subtotal.toFixed(2)}</span>
                        </div>
                        <div className={styles.summaryRow}>
                            <span>Taxa de Serviço (10%)</span>
                            <span>R$ {service.toFixed(2)}</span>
                        </div>
                        {paymentMethod === 'money' && change > 0 && (
                            <div className={styles.summaryRow} style={{color: 'green'}}>
                                <span>Troco</span>
                                <span>R$ {change.toFixed(2)}</span>
                            </div>
                        )}
                        <div className={styles.summaryRow + ' ' + styles.total}>
                            <span>TOTAL</span>
                            <span>R$ {total.toFixed(2)}</span>
                        </div>
                    </div>

                    <button 
                        className={styles.payButton} 
                        onClick={handleFinalizePayment}
                        disabled={paymentMethod === 'money' && parseFloat(cashReceived || '0') < total}
                    >
                        Pagar Agora
                    </button>

                    <button className={styles.cancelButton} onClick={() => router.back()}>
                        Voltar
                    </button>
                </div>
            </div>
        </main>
    );
}

export default function PaymentPage() {
    return (
        <Suspense fallback={<div>Carregando...</div>}>
            <PaymentContent />
        </Suspense>
    );
}