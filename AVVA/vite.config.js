import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            '/api/': {
                target: 'https://avva.itatmisis.ru/',
                changeOrigin: true, 
            },
        },
        port: 3000,
    },
})
