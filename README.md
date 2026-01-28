# Lyftr-AI-Backend-Assignment---KASHISH-THAREJA
Webhook Ingestion API (Lyftr AI Assignment)
Maine ye project ek robust aur scalable webhook receiver banane ke liye design kiya hai jo SMS data ko securely handle karta hai. Pura setup Dockerized hai taaki "it works on my machine" wali problem na aaye.

Design Decisions & Logic
Idempotency (Duplicate Handling): Database level par message_id ko Primary Key rakha hai. Isse agar same webhook dobara aata hai, toh server 200 OK return karega par data duplicate nahi hoga.

Security (HMAC): API har request ka X-Signature header check karti hai. Maine HMAC-SHA256 use kiya hai raw body aur WEBHOOK_SECRET ke saath taaki sirf authorized sources hi data bhej sakein.

Pagination & Filters: /messages endpoint par limit aur offset use kiya hai taaki bade datasets load karte waqt server crash na ho. Saath hi, deterministic ordering (ts aur message_id) rakhi hai.

Persistence: Docker volume (./data:/data) use kiya hai taaki container restart hone par bhi SQLite database ka data save rahe.

How to Run
Build and Start:

Bash
docker-compose up --build
Access API:

API running at: http://localhost:8000

Interactive Docs (Swagger): http://localhost:8000/docs

Endpoints
POST /webhook: Securely ingests SMS data.

GET /messages: Paginated list of all received messages.

GET /stats: Real-time analytics (Total messages, top senders, etc.).

GET /health/live: Liveness probe for monitoring.

GET /health/ready: Readiness probe (Checks DB & Secret).
