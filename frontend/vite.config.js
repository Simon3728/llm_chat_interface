import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load env file based on mode
  const env = loadEnv(mode, process.cwd(), '')
  
  console.log(`Running in ${mode} mode`)
  
  // Base config
  const config = {
    plugins: [
      react(),
      tailwindcss(),
    ],
    server: {
      port: 5173,
      host: true, // Expose to network
    },
    define: {
      // Make environment variables available to the app
      'process.env.VITE_API_URL': JSON.stringify(env.VITE_API_URL),
      'process.env.APP_ENV': JSON.stringify(env.APP_ENV || 'development')
    }
  }
  
  return config
})