"""
Verify database tables exist

This script checks if all required tables exist in the database.
"""
from sqlalchemy import inspect
from app.core.database import engine

def check_tables():
    """Check if all required tables exist"""
    print("🔍 Verificando tablas en la base de datos...")
    print("=" * 60)
    
    # Expected tables
    expected_tables = [
        'users',
        'fiscal_profiles',
        'sat_credentials',
        'documents',
        'notifications',
        'audit_logs',
        'cfdis',
        'prestaciones_anuales',
        'sync_history',
        'solicitudes_descarga_sat'
    ]
    
    # Get actual tables
    inspector = inspect(engine)
    actual_tables = inspector.get_table_names()
    
    print(f"📊 Tablas encontradas: {len(actual_tables)}")
    print(f"📋 Tablas esperadas: {len(expected_tables)}")
    print("=" * 60)
    
    # Check each expected table
    missing_tables = []
    for table in expected_tables:
        if table in actual_tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} (FALTA)")
            missing_tables.append(table)
    
    print("=" * 60)
    
    if missing_tables:
        print(f"\n⚠️  Faltan {len(missing_tables)} tabla(s):")
        for table in missing_tables:
            print(f"   - {table}")
        print("\n💡 Ejecuta: python create_tables.py")
        return False
    else:
        print("\n✅ Todas las tablas existen!")
        
        # Show extra tables
        extra_tables = [t for t in actual_tables if t not in expected_tables]
        if extra_tables:
            print(f"\n📝 Tablas adicionales ({len(extra_tables)}):")
            for table in extra_tables:
                print(f"   - {table}")
        
        return True

if __name__ == "__main__":
    success = check_tables()
    exit(0 if success else 1)
