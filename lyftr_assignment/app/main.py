import os
from fastapi import FastAPI, Request, HTTPException, Depends, Header, Response, status

from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func 

from . import models, database, security, schemas

# creating DB tables
models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

# Dependency: DB Session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/webhook")
async def webhook_receiver(
    request: Request, 
    db: Session = Depends(get_db),
    x_signature: str = Header(None)
):
    
    
    body_bytes = await request.body()
    
    
    if not x_signature or not security.verify_signature(body_bytes, x_signature):
        # Log error event here if needed
        raise HTTPException(status_code=401, detail="invalid signature")

    # Payload parse
    try:
        data = await request.json()
        payload = schemas.WebhookPayload(**data)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid payload") [cite: 49]

    # Idempotency Check (Check if message exists)
    existing_msg = db.query(models.Message).filter(models.Message.message_id == payload.message_id).first()
    
    if existing_msg:
        return {"status": "ok"} [cite: 58, 64]

    # inserting db  
    new_msg = models.Message(
        message_id=payload.message_id,
        from_msisdn=payload.from_msisdn,
        to_msisdn=payload.to_msisdn,
        ts=payload.ts,
        text=payload.text,
        created_at=datetime.utcnow().isoformat() + "Z"
    )
    db.add(new_msg)
    db.commit()

    return {"status": "ok"}

# Health Checks 
@app.get("/health/live")
def health_live():
    return {"status": "live"} 

@app.get("/health/ready")
def health_ready(db: Session = Depends(get_db)):
    if not os.getenv("WEBHOOK_SECRET"):
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    try:
        db.execute("SELECT 1")
    except Exception:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return {"status": "ready"}

# 1. GET /messages (List with Pagination & Filters)
@app.get("/messages")
def list_messages(
    limit: int = 50, offset: int = 0, 
    from_msisdn: str = None, since: str = None, q: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Message)
    
    # Filters lagao [cite: 74, 77, 80]
    if from_msisdn:
        query = query.filter(models.Message.from_msisdn == from_msisdn)
    if since:
        query = query.filter(models.Message.ts >= since)
    if q:
        query = query.filter(models.Message.text.ilike(f"%{q}%")) # Case-insensitive search [cite: 81]

    total = query.count() # Total count filters ke baad [cite: 103]
    
    # Pagination aur Ordering
    data = query.order_by(models.Message.ts.asc(), models.Message.message_id.asc())\
                .offset(offset).limit(limit).all()

    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset
    }

# 2. GET /stats (Simple Analytics)
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total_messages = db.query(models.Message).count() 
    senders_count = db.query(func.count(func.distinct(models.Message.from_msisdn))).scalar()
    
    # Top 10 senders by count
    messages_per_sender = db.query(
        models.Message.from_msisdn.label("from"), 
        func.count(models.Message.message_id).label("count")
    ).group_by(models.Message.from_msisdn).order_by(func.count().desc()).limit(10).all()

    # First aur Last message timestamp 
    first_msg = db.query(func.min(models.Message.ts)).scalar()
    last_msg = db.query(func.max(models.Message.ts)).scalar()

    return {
        "total_messages": total_messages,
        "senders_count": senders_count,
        "messages_per_sender": [dict(row._mapping) for row in messages_per_sender],
        "first_message_ts": first_msg,
        "last_message_ts": last_msg
    }
    
