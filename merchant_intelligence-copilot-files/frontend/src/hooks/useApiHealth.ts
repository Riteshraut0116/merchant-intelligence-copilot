import { useEffect, useState } from 'react';
import { api } from '../lib/api';

export function useApiHealth() {
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [lastCheck, setLastCheck] = useState<number>(0);

  const checkHealth = async () => {
    try {
      await api.get('/health', { timeout: 5000 });
      setIsConnected(true);
      setLastCheck(Date.now());
    } catch {
      setIsConnected(false);
      setLastCheck(Date.now());
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(() => {
      if (Date.now() - lastCheck > 30000) {
        checkHealth();
      }
    }, 30000);
    return () => clearInterval(interval);
  }, [lastCheck]);

  return { isConnected, checkHealth };
}
