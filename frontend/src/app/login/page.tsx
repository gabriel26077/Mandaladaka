"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from './login.module.css';
import Image from 'next/image';

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

    try {
      const response = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.description || 'Falha no login');

      localStorage.setItem('access_token', data.access_token);
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
        
        <Image 
          src="/icons/mdk_com.png"
          alt="MDK Logo"
          width={150}
          height={150}
          className={styles.logo}
        />
        
        <h1>Bem Vindo!</h1>
        <div className={styles.inputGroup}>
          <label htmlFor="username">Usuário</label>
          <input 
            type="text" 
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={isLoading}
            placeholder="Digite seu nome de usuário"
          />
        </div>

        <div className={styles.inputGroup}>
          <div className={styles.labelRow}>
            <label htmlFor="password">Senha</label>
            <a href="#" className={styles.forgotPassword}>Esqueceu a senha?</a>
          </div>
          <input 
            type="password" 
            id="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={isLoading}
            placeholder="Digite sua senha"
          />
        </div>

        {error && <p className={styles.errorText}>{error}</p>}

        <button type="submit" className={styles.btnSubmit} disabled={isLoading}>
          {isLoading ? 'Entrando...' : 'LOGIN'}
        </button>
      </form>
    </div>
  );
}