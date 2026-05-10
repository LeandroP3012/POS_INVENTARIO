import 'package:flutter/foundation.dart';

/// Notificador global para cambiar el tab activo en [HomeScreen].
///
/// Por qué existe este archivo: HomeScreen importa DashboardScreen, por lo que
/// DashboardScreen no puede importar HomeScreen sin crear una dependencia
/// circular. Colocar el notificador aquí rompe el ciclo: ambas pantallas
/// importan `navigation_state.dart` y no se importan entre sí.
///
/// Uso:
///   tabIndexNotifier.value = 1; // navega al tab "Punto de Venta"
final tabIndexNotifier = ValueNotifier<int>(0);
