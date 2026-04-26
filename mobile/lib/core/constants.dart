// URL base del backend
// Para pruebas en Chrome/Windows: http://localhost:8000/api
// Para emulador Android:          http://10.0.2.2:8000/api
// Para producción Railway:        https://tu-app.up.railway.app/api
const String kBaseUrl = 'http://localhost:8000/api';

// Nombre de la app
const String kAppName = 'T-Gestiona POS';

// Timeout de peticiones HTTP (segundos)
const int kRequestTimeout = 30;

// Clave de almacenamiento del token JWT
const String kTokenKey = 'auth_token';
const String kUserKey = 'current_user';
