Lyftr-AI Backend-Assignment KASHISH-THAREJA
Webhook Ingestion API (Lyftr AI Assignment)
I developed this project to create a robust and scalable webhook receiver that securely handles SMS data. The entire system is Dockerized to ensure environment consistency and ease of deployment.


Design Decisions & Logic
+ Idempotency (Duplicate Handling): I used the message_id as the Primary Key in the SQLite database. This ensures that if the same webhook is triggered multiple times, the server returns a 200 OK but doesn't create duplicate entries in the database.

+ Security (HMAC): Every request to the /webhook endpoint is validated using an X-Signature header. I implemented HMAC-SHA256 verification using a WEBHOOK_SECRET and the raw request body to ensure only authorized sources can ingest data.
  
+ Pagination & Filters: To keep the API performant, the /messages endpoint supports limit and offset. I also added deterministic ordering (by ts and message_id) and support for filtering by sender or text search.
  
+ Persistence: I configured a Docker volume (./data:/data) to ensure that the SQLite database remains intact even if the container is restarted or rebuilt.
  
+ Observability: I included both /health/live and /health/ready probes. The readiness probe specifically checks for the existence of the WEBHOOK_SECRET and a successful database connection before marking the service as ready.

How to Run
Build and Start:

+ Bash
  docker-compose up --build

+ Access API:

+ Base URL: http://localhost:8000

+ Interactive Swagger Docs: http://localhost:8000/docs

Endpoints
+ POST /webhook: Securely ingests SMS data with signature validation.

+ GET /messages: Paginated retrieval of messages with search filters.

+ GET /stats: Real-time analytics, including total counts and top 10 senders.

+ GET /health/live: Basic liveness check.

+ GET /health/ready: Readiness check ensuring DB and Environment are properly configured.
