"""
Streamlit Frontend - Gestor Fiscal Personal
"""
import streamlit as st
import requests
import os
from datetime import datetime
from typing import Optional

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# Session state initialization
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None


def api_request(endpoint: str, method: str = "GET", data: dict = None, files: dict = None):
    """Make API request with authentication"""
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            if files:
                response = requests.post(url, headers=headers, data=data, files=files)
            else:
                response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        return response
    except requests.exceptions.ConnectionError:
        st.error("⚠️ No se puede conectar al servidor. Asegúrate de que el backend esté ejecutándose.")
        return None


def login_page():
    """Login/Register page"""
    st.title("🏛️ Gestor Fiscal Personal SAT")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        st.subheader("Iniciar Sesión")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Iniciar Sesión")
            
            if submit:
                response = api_request("/auth/login", "POST", {
                    "username": email,
                    "password": password
                })
                
                if response and response.status_code == 200:
                    data = response.json()
                    st.session_state.token = data["access_token"]
                    
                    # Get user info
                    user_response = api_request("/auth/me")
                    if user_response and user_response.status_code == 200:
                        st.session_state.user = user_response.json()
                        st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
    
    with tab2:
        st.subheader("Crear Cuenta")
        with st.form("register_form"):
            email = st.text_input("Email")
            phone = st.text_input("Teléfono (opcional)")
            password = st.text_input("Contraseña", type="password")
            password2 = st.text_input("Confirmar Contraseña", type="password")
            first_name = st.text_input("Nombre")
            last_name = st.text_input("Apellidos")
            submit = st.form_submit_button("Registrarse")
            
            if submit:
                if password != password2:
                    st.error("❌ Las contraseñas no coinciden")
                else:
                    response = api_request("/auth/register", "POST", {
                        "email": email,
                        "phone": phone if phone else None,
                        "password": password,
                        "first_name": first_name,
                        "last_name": last_name
                    })
                    
                    if response and response.status_code == 200:
                        st.success("✅ Cuenta creada exitosamente. Por favor inicia sesión.")
                    else:
                        error_msg = response.json().get("detail", "Error al crear cuenta") if response else "Error de conexión"
                        st.error(f"❌ {error_msg}")


def dashboard_page():
    """Main dashboard"""
    st.title("🏛️ Gestor Fiscal Personal")
    
    # Sidebar
    with st.sidebar:
        st.write(f"👤 {st.session_state.user['first_name']} {st.session_state.user['last_name']}")
        st.write(f"📧 {st.session_state.user['email']}")
        
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Dashboard", 
        "👤 Perfil Fiscal", 
        "📄 Documentos",
        "🔐 Credenciales SAT"
    ])
    
    with tab1:
        show_dashboard()
    
    with tab2:
        show_fiscal_profile()
    
    with tab3:
        show_documents()
    
    with tab4:
        show_sat_credentials()


def show_dashboard():
    """Dashboard overview"""
    st.header("Resumen General")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("RFC", st.session_state.user.get("fiscal_profile", {}).get("rfc", "Sin RFC"))
    
    with col2:
        st.metric("Documentos", "0")
    
    with col3:
        st.metric("Notificaciones", "0")
    
    st.divider()
    
    st.subheader("📊 Estado de Cumplimiento")
    st.info("🔄 Conecta tus credenciales SAT para ver tu estado fiscal")
    
    st.subheader("🔔 Notificaciones Recientes")
    st.write("No hay notificaciones pendientes")


def show_fiscal_profile():
    """Fiscal profile management"""
    st.header("👤 Perfil Fiscal")
    
    # Get current profile
    response = api_request("/fiscal/profile")
    
    if response and response.status_code == 200:
        profile = response.json()
        
        with st.form("fiscal_form"):
            st.subheader("Datos Fiscales")
            
            rfc = st.text_input("RFC", value=profile.get("rfc", ""), max_chars=13)
            curp = st.text_input("CURP", value=profile.get("curp", ""), max_chars=18)
            legal_name = st.text_input("Nombre/Razón Social", value=profile.get("legal_name", ""))
            
            tax_regime = st.selectbox("Régimen Fiscal", [
                "605 - Sueldos y Salarios",
                "621 - Incorporación Fiscal",
                "626 - Régimen Simplificado de Confianza",
                "612 - Personas Físicas con Actividades Empresariales",
                "606 - Arrendamiento",
                "601 - Régimen General de Personas Morales",
                "616 - Sin Obligaciones Fiscales"
            ])
            
            submit = st.form_submit_button("💾 Guardar Cambios")
            
            if submit:
                regime_code = tax_regime.split(" - ")[0]
                
                update_response = api_request("/fiscal/profile", "PUT", {
                    "rfc": rfc if rfc else None,
                    "curp": curp if curp else None,
                    "legal_name": legal_name if legal_name else None,
                    "tax_regime": regime_code if rfc else None
                })
                
                if update_response and update_response.status_code == 200:
                    st.success("✅ Perfil fiscal actualizado")
                    st.rerun()
                else:
                    error_msg = update_response.json().get("detail", "Error al actualizar") if update_response else "Error de conexión"
                    st.error(f"❌ {error_msg}")
    
    elif response and response.status_code == 404:
        st.info("📝 Completa tu perfil fiscal para comenzar")
        
        with st.form("fiscal_form_new"):
            rfc = st.text_input("RFC", max_chars=13)
            curp = st.text_input("CURP", max_chars=18)
            legal_name = st.text_input("Nombre/Razón Social")
            
            submit = st.form_submit_button("💾 Crear Perfil")
            
            if submit:
                response = api_request("/fiscal/profile", "POST", {
                    "rfc": rfc if rfc else None,
                    "curp": curp if curp else None,
                    "legal_name": legal_name if legal_name else None
                })
                
                if response and response.status_code == 200:
                    st.success("✅ Perfil fiscal creado")
                    st.rerun()


def show_documents():
    """Documents management"""
    st.header("📄 Mis Documentos")
    
    st.info("🚧 Sección de documentos en desarrollo")
    
    # Upload section
    st.subheader("📤 Subir Documento")
    
    with st.form("upload_form"):
        doc_type = st.selectbox("Tipo de Documento", [
            "Constancia de Situación Fiscal",
            "e.firma (Certificado .cer)",
            "e.firma (Llave .key)",
            "CFDI",
            "Opinión de Cumplimiento",
            "Otro"
        ])
        
        title = st.text_input("Título del Documento")
        file = st.file_uploader("Seleccionar Archivo")
        
        submit = st.form_submit_button("📤 Subir")
        
        if submit and file:
            st.success(f"✅ Documento '{title}' preparado para subir (API endpoint pendiente)")


def show_sat_credentials():
    """SAT credentials management"""
    st.header("🔐 Credenciales SAT")
    
    st.warning("⚠️ Tus credenciales se almacenan de forma segura con encriptación AES-256")
    
    response = api_request("/fiscal/sat-credentials")
    
    if response and response.status_code == 200:
        creds = response.json()
        
        st.success("✅ Credenciales SAT configuradas")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Contraseña SAT", "Configurada ✓")
        with col2:
            efirma_status = "Configurada ✓" if creds.get("has_efirma") else "No configurada"
            st.metric("e.firma", efirma_status)
        
        if st.button("🔄 Actualizar Credenciales"):
            st.rerun()
    
    else:
        st.info("📝 Configura tus credenciales para automatizar consultas al SAT")
        
        with st.form("sat_creds_form"):
            sat_password = st.text_input("Contraseña del Portal SAT", type="password")
            
            st.subheader("e.firma (Opcional)")
            cer_file = st.file_uploader("Certificado .cer", type=["cer"])
            key_file = st.file_uploader("Llave privada .key", type=["key"])
            efirma_password = st.text_input("Contraseña e.firma", type="password")
            
            submit = st.form_submit_button("💾 Guardar Credenciales")
            
            if submit:
                st.info("🚧 Endpoint de credenciales en desarrollo")


def main():
    """Main application"""
    st.set_page_config(
        page_title="Gestor Fiscal SAT",
        page_icon="🏛️",
        layout="wide"
    )
    
    # Check if logged in
    if st.session_state.token is None:
        login_page()
    else:
        dashboard_page()


if __name__ == "__main__":
    main()
