import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import fs from 'fs'
import path from 'path'

// Determine if HTTPS should be used (default to true)
const useHttps = process.env.DOCKER === 'true'

// Default config
const config = {
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    port: 5173,
    host: true, // Expose to network
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

// https://vite.dev/config/
export default defineConfig(config)