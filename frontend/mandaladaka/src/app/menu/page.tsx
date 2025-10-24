"use client";

import { useState } from 'react';
import { mockProducts } from './mock-data';
import { useSearchParams } from 'next/navigation';

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
    <main style={{ display: 'flex' }}>
      <div className="product-list" style={{ flex: 2, padding: '1rem' }}>
        <h1>Cardápio</h1>
        {products.map((product) => (
          <div key={product.id} style={{ border: '1px solid #ccc', margin: '0.5rem', padding: '0.5rem' }}>
            <img 
              src={product.imageUrl} 
              alt={product.name} 
              style={{ width: '100px', height: '100px', objectFit: 'cover' }} 
            />
            <h3>{product.name}</h3>
            <p>R$ {product.price.toFixed(2)}</p>
            <p>Categoria: {product.category}</p>
            <button>Adicionar</button>
          </div>
        ))}
      </div>

      <div className="order-summary" style={{ flex: 1, padding: '1rem', borderLeft: '1px solid #ddd' }}>
        <h2>Seu Pedido</h2>
        <div style={{ padding: '10px 0' }}>
          <span>MESA: <strong>{table || 'N/A'}</strong></span>
          <span style={{ marginLeft: '1rem' }}>CLIENTES: <strong>{clients || 'N/A'}</strong></span>
        </div>
        <hr />
        <p>(Itens do pedido aqui...)</p>
      </div>

    </main>
  );
}