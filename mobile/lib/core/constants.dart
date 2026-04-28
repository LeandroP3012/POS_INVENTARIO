// URL base del backend.
// Para producción Railway, compila con:
//   flutter build web --dart-define=API_URL=https://tu-app.up.railway.app/api
// Para desarrollo local simplemente usa el valor por defecto.
const String kBaseUrl = String.fromEnvironment(
  'API_URL',
  defaultValue: 'http://localhost:8000/api',
);

// Nombre de la app
const String kAppName = 'T-Gestiona POS';

// Timeout de peticiones HTTP (segundos)
const int kRequestTimeout = 15;

// Clave de almacenamiento del token JWT
const String kTokenKey = 'auth_token';
const String kUserKey = 'current_user';
