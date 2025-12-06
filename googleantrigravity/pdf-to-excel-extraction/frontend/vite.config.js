import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        proxy: {
            '/upload': 'http://localhost:8000',
            '/extract': 'http://localhost:8000',
            '/export': 'http://localhost:8000',
        }
    }
})
