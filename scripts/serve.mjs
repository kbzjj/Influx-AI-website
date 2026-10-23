import { createServer } from 'node:http'
import { createReadStream, existsSync, statSync } from 'node:fs'
import { extname, join, normalize, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(fileURLToPath(new URL('..', import.meta.url)))
const port = Number(process.env.PORT) || 3000
const defaultEntry = '/versions/%E6%96%B9%E6%A1%88%E4%B8%89/'

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.ico': 'image/x-icon',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.mp3': 'audio/mpeg',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.txt': 'text/plain; charset=utf-8',
}

createServer((req, res) => {
  const url = new URL(req.url ?? '/', 'http://localhost')

  if (url.pathname === '/') {
    res.writeHead(302, { Location: defaultEntry + url.search })
    res.end()
    return
  }

  let pathname
  try {
    pathname = decodeURIComponent(url.pathname)
  } catch {
    res.writeHead(400)
    res.end('Bad request')
    return
  }

  let filePath = normalize(join(root, pathname))
  if (!filePath.startsWith(root)) {
    res.writeHead(403)
    res.end('Forbidden')
    return
  }

  if (existsSync(filePath) && statSync(filePath).isDirectory()) {
    if (!pathname.endsWith('/')) {
      res.writeHead(301, { Location: url.pathname + '/' + url.search })
      res.end()
      return
    }
    filePath = join(filePath, 'index.html')
  }

  if (!existsSync(filePath) || !statSync(filePath).isFile()) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' })
    res.end('Not found')
    return
  }

  res.writeHead(200, {
    'Content-Type': mimeTypes[extname(filePath).toLowerCase()] ?? 'application/octet-stream',
    'Cache-Control': 'no-cache',
  })
  createReadStream(filePath).pipe(res)
}).listen(port, '0.0.0.0', () => {
  console.log(`Influx AI preview running on http://localhost:${port}`)
})
