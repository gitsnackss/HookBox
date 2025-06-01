"""Tests for webhooks API."""
def test_list_webhooks(client, db):
    # Setup
    from app.models.project import Project
    from app.models.webhook import Webhook
    from app.utils.id_generator import generate_id
    from app.services.auth_service import AuthService
    import bcrypt
    
    # Create project with known API key
    raw_key = "test_api_key"
    key_hash = bcrypt.hashpw(raw_key.encode(), bcrypt.gensalt()).decode()
    
    proj = Project(
        id=generate_id("proj"),
        name="Test",
        inbox_key="listkey",
        api_key_hash=key_hash,
    )
    db.add(proj)
    db.commit()
    
    # Create webhook
    wh = Webhook(
        id=generate_id("wh"),
        project_id=proj.id,
        method="POST",
        path="/i/listkey",
        headers='{"content-type":"application/json"}',
        body=b'{"msg":"hi"}',
    )
    db.add(wh)
    db.commit()

    # Request
    response = client.get(
        f"/api/v1/projects/{proj.id}/webhooks",
        headers={"Authorization": f"Bearer {raw_key}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == wh.id
