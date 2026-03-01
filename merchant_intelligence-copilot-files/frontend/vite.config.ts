import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react'

export default defineConfig({ 
  plugins: [react()], 
  server: { port: 5173 },
  define: {
    // Fallback for production if env var not set
    'import.meta.env.VITE_API_BASE_URL': JSON.stringify(
      process.env.VITE_API_BASE_URL || 'https://merchant-intelligence-copilot.onrender.com'
    )
  }
})
