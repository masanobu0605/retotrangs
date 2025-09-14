from __future__ import annotations

from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import get_settings
from .db import Base, engine, session_scope
from .models import Tenant, User
from . import models_cf  # noqa: F401  モデルを読み込み、create_all 対象に含めるため
from .security import hash_password
from .routers import auth as auth_router
from .routers import users as admin_users_router
from .routers import me as me_router
from .routers import public as public_router
from .routers import accounts as accounts_router
from .routers import deals as deals_router
from .routers import contacts as contacts_router
from .routers import notes as notes_router
from .routers import tasks as tasks_router
from .routers import custom_fields as custom_fields_router
from .routers import attachments as attachments_router


settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"]
    ,allow_headers=["*"]
)


@app.get("/health")
def health():
    return {"ok": True, "service": settings.app_name}


def _bootstrap():
    # reset test DB on pytest runs (SQLite) to avoid state leakage
    try:
        if str(engine.url).startswith("sqlite") and settings.testing:
            db_file = getattr(engine.url, "database", None)
            if db_file and os.path.exists(db_file):
                os.remove(db_file)
    except Exception as e:
        print(f"[BOOTSTRAP] test db cleanup skipped: {e}")
    # create tables
    Base.metadata.create_all(bind=engine)
    # apply RLS if PostgreSQL
    if str(engine.url).startswith("postgresql"):
        try:
            with engine.begin() as conn:
                # tenants: match by id; others by tenant_id
                try:
                    conn.exec_driver_sql("ALTER TABLE IF EXISTS tenants ENABLE ROW LEVEL SECURITY;")
                    conn.exec_driver_sql("DROP POLICY IF EXISTS p_tenants ON tenants;")
                    conn.exec_driver_sql("CREATE POLICY p_tenants ON tenants USING (id::text = current_setting('app.current_tenant', true))")
                except Exception as e:
                    print(f"[BOOTSTRAP] tenants policy skipped: {e}")

                tables = ['users','accounts','contacts','deals','notes','tasks']
                for t in tables:
                    try:
                        conn.exec_driver_sql(f"ALTER TABLE IF EXISTS {t} ENABLE ROW LEVEL SECURITY;")
                        conn.exec_driver_sql(f"DROP POLICY IF EXISTS p_{t} ON {t};")
                        conn.exec_driver_sql("CREATE POLICY p_%s ON %s USING (tenant_id::text = current_setting('app.current_tenant', true))" % (t, t))
                    except Exception as e:
                        print(f"[BOOTSTRAP] policy for {t} skipped: {e}")
        except Exception as e:
            print(f"[BOOTSTRAP] RLS apply skipped/error: {e}")
    # seed default tenant and admin
    with session_scope() as session:
        tenant = session.query(Tenant).filter(Tenant.slug == "default").first()
        if not tenant:
            tenant = Tenant(name="Default", slug="default")
            session.add(tenant)
            session.flush()

        admin = (
            session.query(User)
            .filter(User.tenant_id == tenant.id, User.email == settings.admin_email)
            .first()
        )
        if not admin:
            session.add(
                User(
                    tenant_id=tenant.id,
                    name="Admin",
                    email=settings.admin_email,
                    password_hash=hash_password(settings.admin_password),
                    role="admin",
                )
            )


_bootstrap()

# include routers
app.include_router(auth_router.router)
app.include_router(me_router.router)
app.include_router(admin_users_router.router)
app.include_router(public_router.router)
app.include_router(accounts_router.router)
app.include_router(deals_router.router)
app.include_router(contacts_router.router)
app.include_router(notes_router.router)
app.include_router(tasks_router.router)
app.include_router(custom_fields_router.router)
app.include_router(attachments_router.router)


@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name} from {settings.app_name}!"}
