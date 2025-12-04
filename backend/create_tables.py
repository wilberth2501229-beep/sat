"""
Create all database tables

This script creates all tables defined in the models:
- users
- fiscal_profiles
- sat_credentials
- documents
- notifications
- audit_logs
- cfdis
- prestaciones_anuales
- sync_history
- solicitudes_descarga_sat
"""
from app.core.database import engine, Base
from app.models import (
    User, FiscalProfile, SATCredentials, Document, 
    Notification, AuditLog, CFDI, PrestacionAnual,
    SyncHistory, SolicitudDescargaSAT
)

def create_all_tables():
    """Create all database tables"""
    print("🔨 Creating database tables...")
    print("=" * 60)
    
    # List all models being created
    models = [
        User, FiscalProfile, SATCredentials, Document,
        Notification, AuditLog, CFDI, PrestacionAnual,
        SyncHistory, SolicitudDescargaSAT
    ]
    
    print(f"📋 Creating {len(models)} tables:")
    for model in models:
        print(f"   - {model.__tablename__}")
    
    print("=" * 60)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ All tables created successfully!")
    print("\n📊 Tables created:")
    print("   ✓ users")
    print("   ✓ fiscal_profiles")
    print("   ✓ sat_credentials")
    print("   ✓ documents")
    print("   ✓ notifications")
    print("   ✓ audit_logs")
    print("   ✓ cfdis")
    print("   ✓ prestaciones_anuales")
    print("   ✓ sync_history")
    print("   ✓ solicitudes_descarga_sat")

if __name__ == "__main__":
    create_all_tables()

