"use client";

import { useRouter } from "next/navigation";
import styles from "./payment.module.css";

export default function PaymentPage() {
  const router = useRouter();

  return (
    <main className={styles.container}>
      <div className={styles.comingSoonCard}>
        <span className={styles.icon}>💳</span>
        <h1 className={styles.title}>Pagamentos</h1>
        <p className={styles.text}>
          Esta funcionalidade está em desenvolvimento e estará disponível em breve.
        </p>
        <span className={styles.badge}>Em breve</span>
        <button className={styles.backBtn} onClick={() => router.back()}>
          Voltar
        </button>
      </div>
    </main>
  );
}