# 📖 Documentación del Proyecto

## 📋 Índice

1. [Casos de Uso](#casos-de-uso)
2. [Arquitectura](#arquitectura)
3. [Modelos de Datos](#modelos-de-datos)
4. [Flujos de Usuario](#flujos-de-usuario)
5. [Integraciones](#integraciones)
6. [Seguridad](#seguridad)

## 🎯 Casos de Uso

### Caso A: Usuario con e.firma y contraseña SAT ✅
**Estado**: Usuario completo con todas las credenciales

**Flujo**:
1. Usuario sube archivos .CER y .KEY
2. Ingresa contraseña de e.firma
3. Ingresa contraseña del SAT
4. Sistema valida credenciales
5. Sistema descarga automáticamente:
   - Constancia de situación fiscal
   - Opinión del cumplimiento
   - CFDI emitidos/recibidos
   - Declaraciones
6. Panel fiscal completo disponible

### Caso B: Usuario solo con RFC ⚡
**Estado**: Usuario con RFC pero sin credenciales completas

**Flujo**:
1. Usuario ingresa RFC
2. Sistema valida RFC con SAT
3. Sistema muestra perfil básico
4. Sistema guía para:
   - Crear contraseña SAT
   - Tramitar e.firma
   - Activar buzón tributario

### Caso C: Usuario sin contraseña SAT 📝
**Estado**: Usuario tiene RFC pero necesita contraseña

**Flujo**:
1. Usuario ingresa RFC y CURP
2. Sistema inicia proceso de recuperación/creación
3. OCR de INE para autocompletar datos
4. Webview guiada al portal SAT
5. Validación y guardado de contraseña

### Caso D: Usuario sin RFC 🆕
**Estado**: Usuario sin inscripción fiscal

**Flujo**:
1. Usuario ingresa CURP
2. Sistema verifica si existe RFC
3. Si no existe: guía de inscripción
4. OCR de documentos para prellenado
5. Asistente paso a paso
6. Descarga automática de cédula

## 🏗️ Arquitectura

### Backend API (FastAPI)
```
┌─────────────────────────────────────────┐
│           FastAPI Application            │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │   Auth   │  │  Fiscal  │  │  Docs  ││
│  │Endpoints │  │Endpoints │  │Endpoints││
│  └──────────┘  └──────────┘  └────────┘│
├─────────────────────────────────────────┤
│           Business Logic                 │
│  - Validation   - Encryption             │
│  - Processing   - Authentication         │
├─────────────────────────────────────────┤
│              Data Layer                  │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │PostgreSQL│  │  Redis   │  │ MinIO  ││
│  │   ORM    │  │  Cache   │  │Storage ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
```

### Workers (Celery)
```
┌─────────────────────────────────────────┐
│          Celery Workers                  │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │      SAT Automation Tasks          │ │
│  │  - Login SAT                       │ │
│  │  - Download CFDI                   │ │
│  │  - Update fiscal status            │ │
│  │  - Generate constancia             │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │      Document Tasks                │ │
│  │  - OCR processing                  │ │
│  │  - Encryption                      │ │
│  │  - Validation                      │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │      Notification Tasks            │ │
│  │  - Email                           │ │
│  │  - SMS                             │ │
│  │  - Push notifications              │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 💾 Modelos de Datos

### User
- id, email, phone, password
- first_name, last_name, curp
- status, tier, is_verified

### FiscalProfile
- rfc, curp, legal_name
- tax_regime, fiscal_status
- obligations, compliance_opinion
- tax_mailbox_active

### SATCredentials (cifrado)
- encrypted_password
- efirma files (.cer, .key)
- session tokens

### Document
- document_type, title, description
- file_path (cifrado)
- issue_date, expiry_date
- metadata, tags

## 🔒 Seguridad

### Cifrado
- **Passwords**: Bcrypt
- **JWT**: HS256
- **Documents**: Fernet (symmetric)
- **e.firma**: AES-256

### Almacenamiento
- Credenciales SAT: cifradas en DB
- Documentos: cifrados en storage
- Sesiones: JWT + Redis

### Rate Limiting
- Login: 5 intentos / 15 min
- API: 60 req / min
- Automation: 10 req / hora

## 🔗 Integraciones

### SAT (Web Scraping)
- Portal CFDI
- Constancia de situación
- Opinión del cumplimiento
- Buzón tributario

### PAC (opcional)
- Descarga masiva de CFDI
- Validación de facturas
- Timbrado

### Servicios externos
- Tesseract: OCR
- Twilio: SMS
- SendGrid: Email
- FCM/APNs: Push notifications

## 📱 MVP Roadmap

### Mes 1: Backend Core
- ✅ Setup de proyecto
- ✅ Modelos y migraciones
- ✅ Autenticación JWT
- ✅ Endpoints usuarios y fiscal
- 🔄 Integración SAT básica
- 🔄 Workers de Celery

### Mes 2: Automatización
- 🔄 Web scraping SAT completo
- 🔄 OCR de documentos
- 🔄 Descarga de CFDI
- 🔄 Validación RFC/CURP
- 🔄 Sistema de notificaciones

### Mes 3: Frontend
- 📅 App móvil (Flutter/RN)
- 📅 Dashboard web
- 📅 Onboarding guiado
- 📅 Gestión de documentos
- 📅 Testing y despliegue

---

**Leyenda**: ✅ Completado | 🔄 En progreso | 📅 Planeado
