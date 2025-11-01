"use client";

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { mockProducts, Product } from './mock-data';
import styles from './menu.module.css';

type OrderItem = Product & {
  quantity: number;
};

const allCategories = [...new Set(mockProducts.map((product) => product.category))];

const TAX_RATE = 0.10; // 10%

export default function MenuPage() {
  const [products, setProducts] = useState<Product[]>(mockProducts);
  const searchParams = useSearchParams();
  const table = searchParams.get('table');
  const clients = searchParams.get('clients');
  const [activeCategory, setActiveCategory] = useState(allCategories[0]);
  const [orderItems, setOrderItems] = useState<OrderItem[]>([]);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [modalQuantity, setModalQuantity] = useState(1);

  const filteredProducts = products.filter(
    (product) => product.category === activeCategory
  );

  const openQuantityModal = (product: Product) => {
    setSelectedProduct(product);
    setModalQuantity(1);
    setIsModalOpen(true);
  };

  const handleConfirmAdd = () => {
    if (!selectedProduct) return;
    const existingItem = orderItems.find((item) => item.id === selectedProduct.id);
    if (existingItem) {
      setOrderItems(
        orderItems.map((item) =>
          item.id === selectedProduct.id
            ? { ...item, quantity: item.quantity + modalQuantity }
            : item
        )
      );
    } else {
      setOrderItems([
        ...orderItems,
        { ...selectedProduct, quantity: modalQuantity },
      ]);
    }
    setIsModalOpen(false);
    setSelectedProduct(null);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedProduct(null);
  };
  
  const handleQuantityChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const quantity = parseInt(e.target.value, 10);
    if (quantity > 0) {
      setModalQuantity(quantity);
    }
  };

  const handleRemoveItem = (productId: number) => {
    setOrderItems(orderItems.filter((item) => item.id !== productId));
  };

  const handleCancelOrder = () => {
    setOrderItems([]);
  };
  
  const subtotal = orderItems.reduce(
    (sum, item) => sum + item.price * item.quantity, 0
  );
  const tax = subtotal * TAX_RATE;
  const total = subtotal + tax;

  return (
    <main className={styles.mainContainer}>
      
      {/* Coluna da Esquerda: Produtos */}
      <section className={styles.productsSection}>
        <h2>Cardápio</h2>
        <div className={styles.filterBar}>
          {allCategories.map((category) => (
            <button key={category} className={`${styles.filterButton} ${activeCategory === category ? styles.active : ''}`} onClick={() => setActiveCategory(category)}>
              {category}
            </button>
          ))}
        </div>
        <div className={styles.productsGrid}>
          {filteredProducts.map((product) => (
            <div key={product.id} className={styles.productCard} onClick={() => openQuantityModal(product)} > 
              <img src={product.imageUrl} alt={product.name} />
              <div className={styles.productInfo}>
                <h3>{product.name}</h3>
                <p>Categoria: {product.category}</p>
                <span className={styles.productPrice}>R$ {product.price.toFixed(2)}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Coluna da Direita: Pedido */}
      <section className={styles.orderSection}>
        <div className={styles.orderHeader}>
          <h2>Seu Pedido</h2>
          <div className={styles.orderInfo}>
            <span>
              <img src="/icons/table.png" alt="Ícone Mesa" />
              MESA: <strong>{table || 'N/A'}</strong>
            </span>
            <span>
              <img src="/icons/guess.png" alt="Ícone Clientes" />
              CLIENTES: <strong>{clients || 'N/A'}</strong>
            </span>
          </div>
        </div>

        <div className={styles.orderBody}>
          {orderItems.length === 0 ? (
            <div className={styles.orderBodyEmpty}>
              <img src="/icons/empty-order-icon.png" alt="Pedido Vazio" />
              <p>(Pedido Vazio)</p>
            </div>
          ) : (
            <ul className={styles.orderList}>
              {orderItems.map((item) => (
                <li key={item.id} className={styles.orderItem}>
                  <div className={styles.itemInfo}>
                    <span className={styles.itemQuantity}>{item.quantity}x</span>
                    <span className={styles.itemName}>{item.name}</span>
                  </div>
                  <div className={styles.itemActions}>
                    <span className={styles.itemPrice}>R$ {(item.price * item.quantity).toFixed(2)}</span>
                    <button 
                      className={styles.btnRemoveIcon}
                      onClick={() => handleRemoveItem(item.id)}
                    >
                     <img src="/icons/trash.png" alt="Remover" />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className={styles.orderFooter}>
          <div className={styles.orderTotal}>
            <div className={styles.totalRow}>
              <span>SUBTOTAL</span>
              <span>R$ {subtotal.toFixed(2)}</span>
            </div>
            <div className={styles.totalRow}>
              <span>TAXA DE SERVIÇO (10%)</span>
              <span>R$ {tax.toFixed(2)}</span>
            </div>
            <div className={`${styles.totalRow} ${styles.grandTotal}`}>
              <span>TOTAL</span>
              <span>R$ {total.toFixed(2)}</span>
            </div>
          </div>
          <div className={styles.footerActions}>
            <button className={styles.btnCancelOrder} onClick={handleCancelOrder}>
              Cancelar Pedido
            </button>
            <button className={styles.btnSendOrder} disabled={orderItems.length === 0}>
              Enviar Pedido
            </button>
          </div>
        </div>
      </section>

      {/* Modal */}
      {isModalOpen && selectedProduct && (
        <div className={styles.modalBackdrop} onClick={handleCloseModal}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <h3>Adicionar Produto</h3>
            <p>Produto: <strong>{selectedProduct.name}</strong></p>
            <div className={styles.quantityInput}>
              <label htmlFor="quantity">Quantidade:</label>
              <input type="number" id="quantity" value={modalQuantity} onChange={handleQuantityChange} min="1" />
            </div>
            <div className={styles.modalActions}>
              <button className={styles.btnCancel} onClick={handleCloseModal}>Cancelar</button>
              <button className={styles.btnConfirm} onClick={handleConfirmAdd}>Confirmar</button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}