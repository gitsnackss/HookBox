"""Replay logic with SSRF protection."""
import json
import httpx
from datetime import datetime
from app.utils.security import validate_replay_target
from app.models.replay import Replay
from app.models.webhook import Webhook
from sqlalchemy.orm import Session
from app.utils.id_generator import generate_id

def replay_webhook(
    db: Session,
    webhook: Webhook,
    target_url: str,
    include_original_headers: bool = True,
    timeout: int = 10,
) -> Replay:
    # Validate target URL (SSRF protection)
    allowed_domains = json.loads(webhook.project.allowed_replay_domains or "[]")
    ok, reason = validate_replay_target(target_url, allowed_domains)
    if not ok:
        replay = Replay(
            id=generate_id("rpl"),
            webhook_id=webhook.id,
            target_url=target_url,
            error=reason,
            replayed_at=datetime.utcnow(),
        )
        db.add(replay)
        db.commit()
        db.refresh(replay)
        return replay

    # Prepare request
    # NOTE: In a real async app we'd await this, but for this sync function wrapper we'll use sync blocking or just httpx (which is sync by default if not AsyncClient)
    # However, to be proper async we should use AsyncClient. For MVP simplicity in this potentially synchronous route context, we might use requests or httpx sync.
    # The architecture doc specified separate logic. Let's stick to a simple sync approach for the replay wrapper or ensure callers are async.
    # Given the route definitions are often async, let's use httpx.post synchronously or wrap in async.
    # Let's assume this is called from an async path but the service function itself is blocking (simpler for MVP) or we make it async.
    # The implementation plan had it as `def replay_webhook`, implying sync?
    # Let's make it sync for now as per reference implementation, using `httpx.request` directly.
    
    headers = json.loads(webhook.headers) if include_original_headers else {}
    # Remove hop‑by‑hop headers
    for h in ["host", "content-length", "connection", "keep-alive"]:
        headers.pop(h, None)

    # Add replay‑specific headers
    headers["X-HookBox-Replay"] = "true"
    headers["X-HookBox-Original-Timestamp"] = webhook.received_at.isoformat()
    headers["X-HookBox-Replay-ID"] = generate_id("rpl")

    # Send request
    try:
        response = httpx.request(
            method=webhook.method,
            url=target_url,
            headers=headers,
            content=webhook.body,
            timeout=timeout,
            follow_redirects=False,
        )
        response_body = response.text[:10_000]  # truncate
        replay = Replay(
            id=generate_id("rpl"),
            webhook_id=webhook.id,
            target_url=target_url,
            request_headers=json.dumps(headers),
            request_body=webhook.body.decode(errors="replace") if webhook.body else None,
            response_status_code=response.status_code,
            response_headers=json.dumps(dict(response.headers)),
            response_body=response_body,
            response_time_ms=int(response.elapsed.total_seconds() * 1000),
            replayed_at=datetime.utcnow(),
        )
    except Exception as exc:
        replay = Replay(
            id=generate_id("rpl"),
            webhook_id=webhook.id,
            target_url=target_url,
            request_headers=json.dumps(headers),
            request_body=webhook.body.decode(errors="replace") if webhook.body else None,
            error=str(exc),
            replayed_at=datetime.utcnow(),
        )
    db.add(replay)
    db.commit()
    db.refresh(replay)
    return replay
