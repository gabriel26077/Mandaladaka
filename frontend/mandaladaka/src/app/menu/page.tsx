"use client";

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { mockProducts } from './mock-data';
import styles from './menu.module.css';

type Product = {
  id: number;
  name: string;
  price: number;
  category: string;
  imageUrl: string;
  availability: number | boolean;
};

export default function MenuPage() {
  const [products, setProducts] = useState<Product[]>(mockProducts);
  const searchParams = useSearchParams();
  const table = searchParams.get('table');
  const clients = searchParams.get('clients');

  return (
    <main className={styles.mainContainer}>
      
      <section className={styles.productsSection}>
        <h2>Cardápio</h2>

        <div className={styles.productsGrid}>
  {products.map((product) => (
    // No futuro, colocaremos o onClick aqui
    <div key={product.id} className={styles.productCard}> 
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

      <section className={styles.orderSection}>
        <div className={styles.orderHeader}>
          <h2>Seu Pedido</h2>
          <div className={styles.orderInfo}>
            <span>MESA: <strong>{table || 'N/A'}</strong></span>
            <span>CLIENTES: <strong>{clients || 'N/A'}</strong></span>
          </div>
        </div>

        <div className={styles.orderBodyEmpty}>
          <p>(Pedido Vazio)</p>
        </div>
      </section>
    </main>
  );
}