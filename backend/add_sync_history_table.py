"""
Add sync_history table to database
Run this to add the sync tracking table
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.core.database import engine, Base
from app.models import SyncHistory

def add_sync_history_table():
    """Create sync_history table"""
    print("📊 Agregando tabla de historial de sincronizaciones...")
    
    try:
        # Create only the sync_history table
        Base.metadata.create_all(bind=engine, tables=[
            SyncHistory.__table__
        ])
        
        print("✅ Tabla sync_history creada exitosamente")
        print("\nEstructura:")
        print("  - id: Identificador único")
        print("  - user_id: Usuario que ejecutó la sync")
        print("  - sync_type: FULL o QUICK")
        print("  - status: RUNNING, COMPLETED, FAILED")
        print("  - started_at / completed_at: Timestamps")
        print("  - results: JSON con estadísticas detalladas")
        print("  - error_message: Detalles en caso de fallo")
        
    except Exception as e:
        print(f"❌ Error al crear tabla: {e}")
        raise

if __name__ == "__main__":
    add_sync_history_table()
