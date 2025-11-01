"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from './login.module.css';

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    if (!username || !password) {
      setError("Usuário e senha são obrigatórios.");
      setIsLoading(false);
      return;
    }

    try {
      // 1. Chamar a API de back-end (Flask) que está rodando na porta 5000
      const response = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // O body envia o JSON no formato que o 'LoginSchema' espera
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.description || 'Falha no login');
      }

      // 2. Se o login for bem-sucedido (status 200)
      const token = data.access_token; // Pega o token da resposta

      // 3. Salva o token no localStorage do navegador
      localStorage.setItem('access_token', token);

      // 4. Redireciona o usuário para a página Home (/)
      router.push('/');

    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Um erro inesperado ocorreu.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.loginContainer}>
      <form className={styles.loginForm} onSubmit={handleLogin}>
        <h1>Login</h1>
        
        <div className={styles.inputGroup}>
          <label htmlFor="username">Usuário</label>
          <input 
            type="text" 
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={isLoading}
          />
        </div>

        <div className={styles.inputGroup}>
          <label htmlFor="password">Senha</label>
          <input 
            type="password" 
            id="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={isLoading}
          />
        </div>

        {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

        <button type="submit" className={styles.btnSubmit} disabled={isLoading}>
          {isLoading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
    </div>
  );
}