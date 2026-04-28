import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:provider/provider.dart';

import 'core/app_theme.dart';
import 'providers/auth_provider.dart';
import 'providers/printer_provider.dart';
import 'providers/product_provider.dart';
import 'providers/sale_provider.dart';
import 'screens/splash_screen.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting('es', null);
  await initializeDateFormatting('es_PE', null);

  // Cargar configuración de impresoras antes de arrancar
  final printerProvider = PrinterProvider();
  await printerProvider.load();

  runApp(PosApp(printerProvider: printerProvider));
}

class PosApp extends StatelessWidget {
  final PrinterProvider printerProvider;
  const PosApp({super.key, required this.printerProvider});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => ProductProvider()),
        ChangeNotifierProvider(create: (_) => SaleProvider()),
        ChangeNotifierProvider.value(value: printerProvider),
      ],
      child: MaterialApp(
        title: 'T-Gestiona POS',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.theme,
        initialRoute: '/',
        routes: {
          '/': (_) => const SplashScreen(),
          '/login': (_) => const LoginScreen(),
          '/home': (_) => const HomeScreen(),
        },
      ),
    );
  }
}
