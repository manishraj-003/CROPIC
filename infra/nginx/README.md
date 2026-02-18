# Nginx TLS Proxy (Dev)

This proxy terminates TLS 1.3 and forwards traffic to local backend at `http://host.docker.internal:8000`.

## Generate Cert (OpenSSL)
From `infra/nginx/certs`:

```powershell
openssl req -x509 -nodes -newkey rsa:2048 -days 365 `
  -keyout dev.key -out dev.crt -subj "/CN=localhost"
```

## Run
From `infra`:

```powershell
docker compose up -d nginx
```

Then access API via `https://localhost:8443`.
