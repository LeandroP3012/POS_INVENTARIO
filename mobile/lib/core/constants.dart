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

// Timeout de peticiones HTTP (segundos) — Railway puede tardar en despertar
const int kRequestTimeout = 30;

// Clave de almacenamiento del token JWT
const String kTokenKey = 'auth_token';
const String kUserKey = 'current_user';

// Clave para el timestamp de inicio de sesión (usado para expirar la sesión)
const String kSessionTimestampKey = 'session_timestamp';

// Duración máxima de la sesión en segundos antes de requerir nuevo login
const int kSessionMaxSeconds = 180;
