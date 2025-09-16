import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from "path"
import tailwindcss from "@tailwindcss/vite"

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,  // Frontend will run on port 3000
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8080',  // Backend runs on Binder port
        changeOrigin: true,
        secure: false,
        ws: true
      },
      '/ws': {
        target: (process.env.VITE_API_URL || 'http://localhost:8080').replace('http', 'ws'),
        ws: true
      }
    }
  },
  define: {
    'process.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'http://localhost:8080')
  },
  build: {
    outDir: 'dist'
  }
})
