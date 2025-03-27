import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import fs from 'fs'
import path from 'path'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load env file based on mode
  const env = loadEnv(mode, process.cwd(), '')
  
  // Determine if HTTPS should be used
  const useHttps = env.USE_HTTPS === 'true'
  
  console.log(`Running in ${mode} mode with HTTPS: ${useHttps}`)
  
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

  // Add HTTPS if enabled and certificates exist
  if (useHttps) {
    const certPath = path.resolve(__dirname, '../certs/dev')
    const keyFile = path.join(certPath, 'key.pem')
    const certFile = path.join(certPath, 'cert.pem')
    
    if (fs.existsSync(keyFile) && fs.existsSync(certFile)) {
      config.server.https = {
        key: fs.readFileSync(keyFile),
        cert: fs.readFileSync(certFile),
      }
      console.log('HTTPS enabled for development server')
    } else {
      console.warn('HTTPS requested but certificates not found at', certPath)
      console.warn('Run scripts/generate-certificates.sh to create certificates')
    }
  }
  
  return config
})