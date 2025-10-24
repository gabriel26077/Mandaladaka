// Em: app/menu/page.tsx
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

const allCategories = [...new Set(mockProducts.map((product) => product.category))];

export default function MenuPage() {
  const [products, setProducts] = useState<Product[]>(mockProducts);
  const searchParams = useSearchParams();
  const table = searchParams.get('table');
  const clients = searchParams.get('clients');

  const [activeCategory, setActiveCategory] = useState(allCategories[0]);

  const filteredProducts = products.filter(
    (product) => product.category === activeCategory
  );
  

  return (
    <main className={styles.mainContainer}>
      <section className={styles.productsSection}>
        <h2>Cardápio</h2>
        
        <div className={styles.filterBar}>
          {allCategories.map((category) => (
            <button
              key={category}
            
              className={`${styles.filterButton} ${
                activeCategory === category ? styles.active : ''
              }`}
            
              onClick={() => setActiveCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>

        <div className={styles.productsGrid}>
         
          {filteredProducts.map((product) => (
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