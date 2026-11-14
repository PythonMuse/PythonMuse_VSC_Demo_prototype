import { defineConfig } from 'cf/config'

// A static site: Cloudflare serves the files in ./public as they are.
// There is no server code, database, or secret. The folder to upload is
// named in the deploy command (see package.json), not here.
export default defineConfig({
  worker: {
    name: 'code-demo',
    compatibilityDate: '2026-10-01',
  },
})
