# 📱 Mobile App - Gestor Fiscal Personal

App móvil multiplataforma (iOS/Android) construida con Flutter o React Native.

## 🚧 En Desarrollo

Esta carpeta contendrá la aplicación móvil.

### Stack sugerido:
- **Framework**: Flutter o React Native
- **State Management**: Riverpod / Redux
- **Storage**: SQLite + Secure Storage
- **HTTP Client**: Dio / Axios
- **Biometrics**: local_auth / react-native-biometrics

### Funcionalidades principales:
1. ✅ Autenticación biométrica
2. 📄 Gestión de documentos cifrados
3. 📊 Dashboard fiscal
4. 🔔 Notificaciones push
5. 📥 Descarga de CFDI
6. 🔐 Almacenamiento seguro de credenciales
7. 📸 Captura y OCR de documentos

## 📋 Estructura propuesta

```
mobile/
├── lib/
│   ├── main.dart
│   ├── screens/
│   ├── widgets/
│   ├── services/
│   ├── models/
│   └── utils/
├── android/
├── ios/
└── pubspec.yaml
```

## 🚀 Configuración

```bash
flutter pub get
flutter run
```
