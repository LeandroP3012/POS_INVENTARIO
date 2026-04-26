import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Paleta de colores centralizada de T-Gestiona POS
class AppColors {
  AppColors._();

  // ── Primarios ─────────────────────────────────────────────────────────────
  static const Color primary      = Color(0xFF2C3E50); // Azul marino
  static const Color primaryDark  = Color(0xFF1A252F); // Versión oscura
  static const Color sidebarBg    = Color(0xFF1E2D3D); // Fondo sidebar
  static const Color sidebarItem  = Color(0xFF253647); // Item al hover

  // ── Acentos ───────────────────────────────────────────────────────────────
  static const Color accent       = Color(0xFF3498DB); // Azul claro
  static const Color accentDark   = Color(0xFF2980B9); // Azul más oscuro

  // ── Estados ───────────────────────────────────────────────────────────────
  static const Color success      = Color(0xFF27AE60); // Verde
  static const Color warning      = Color(0xFFF39C12); // Naranja
  static const Color danger       = Color(0xFFE74C3C); // Rojo
  static const Color info         = Color(0xFF2980B9); // Azul info

  // ── Fondo y superficies ────────────────────────────────────────────────────
  static const Color background   = Color(0xFFF0F2F5); // Fondo app
  static const Color surface      = Colors.white;
  static const Color cardBorder   = Color(0xFFE9ECEF);
  static const Color divider      = Color(0xFFDEE2E6);

  // ── Texto ─────────────────────────────────────────────────────────────────
  static const Color textPrimary   = Color(0xFF2C3E50);
  static const Color textSecondary = Color(0xFF6C757D);
  static const Color textMuted     = Color(0xFFADB5BD);

  // ── Sidebar texto ─────────────────────────────────────────────────────────
  static const Color sidebarText        = Color(0xFFB2BABB);
  static const Color sidebarTextActive  = Colors.white;
  static const Color sidebarTextSection = Color(0xFF566573);
}

/// Tema global de la aplicación
class AppTheme {
  AppTheme._();

  static ThemeData get theme {
    final base = GoogleFonts.interTextTheme();

    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        primary: AppColors.primary,
        secondary: AppColors.accent,
        surface: AppColors.surface,
      ),
      scaffoldBackgroundColor: AppColors.background,
      textTheme: base,

      // AppBar
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.inter(
          color: Colors.white,
          fontSize: 17,
          fontWeight: FontWeight.w600,
        ),
        iconTheme: const IconThemeData(color: Colors.white),
      ),

      // Cards
      cardTheme: CardThemeData(
        elevation: 0,
        color: Colors.white,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: const BorderSide(color: AppColors.cardBorder, width: 1),
        ),
      ),

      // Inputs
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        hintStyle: GoogleFonts.inter(
          color: AppColors.textMuted,
          fontSize: 14,
        ),
        labelStyle: GoogleFonts.inter(color: AppColors.textSecondary),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: AppColors.divider),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: AppColors.divider),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: AppColors.accent, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: AppColors.danger, width: 1),
        ),
        focusedErrorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: AppColors.danger, width: 2),
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        prefixIconColor: AppColors.textSecondary,
        suffixIconColor: AppColors.textSecondary,
      ),

      // FilledButton
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: AppColors.accent,
          foregroundColor: Colors.white,
          minimumSize: const Size(0, 48),
          padding: const EdgeInsets.symmetric(horizontal: 24),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          textStyle: GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 14),
        ),
      ),

      // ElevatedButton
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.accent,
          foregroundColor: Colors.white,
          minimumSize: const Size(0, 44),
          padding: const EdgeInsets.symmetric(horizontal: 20),
          elevation: 0,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          textStyle: GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 13),
        ),
      ),

      // OutlinedButton
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: AppColors.accent,
          minimumSize: const Size(0, 44),
          padding: const EdgeInsets.symmetric(horizontal: 20),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          side: const BorderSide(color: AppColors.accent),
          textStyle: GoogleFonts.inter(fontWeight: FontWeight.w500, fontSize: 13),
        ),
      ),

      // Chips
      chipTheme: ChipThemeData(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        labelStyle: GoogleFonts.inter(fontSize: 12),
        padding: const EdgeInsets.symmetric(horizontal: 8),
      ),

      // NavigationBar (mobile bottom)
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: Colors.white,
        elevation: 0,
        shadowColor: Colors.black12,
        indicatorColor: AppColors.accent.withValues(alpha: 0.12),
        labelTextStyle: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return GoogleFonts.inter(
              fontSize: 11,
              fontWeight: FontWeight.w600,
              color: AppColors.accent,
            );
          }
          return GoogleFonts.inter(
            fontSize: 11,
            fontWeight: FontWeight.w400,
            color: AppColors.textSecondary,
          );
        }),
        iconTheme: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return const IconThemeData(color: AppColors.accent, size: 22);
          }
          return const IconThemeData(color: AppColors.textSecondary, size: 22);
        }),
      ),

      // Divider
      dividerTheme: const DividerThemeData(
        color: AppColors.divider,
        space: 1,
        thickness: 1,
      ),

      // SnackBar
      snackBarTheme: SnackBarThemeData(
        behavior: SnackBarBehavior.floating,
        backgroundColor: AppColors.primary,
        contentTextStyle: GoogleFonts.inter(color: Colors.white),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),

      // ListTile
      listTileTheme: ListTileThemeData(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }
}

/// Widget de tarjeta KPI reutilizable
class KpiCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;
  final String? subtitle;

  const KpiCard({
    super.key,
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
    this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: const Border(left: BorderSide(color: AppColors.cardBorder, width: 1)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, color: color, size: 22),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  title,
                  style: GoogleFonts.inter(
                    color: AppColors.textSecondary,
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: GoogleFonts.inter(
                    color: AppColors.textPrimary,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                if (subtitle != null) ...[
                  const SizedBox(height: 2),
                  Text(
                    subtitle!,
                    style: GoogleFonts.inter(
                      color: AppColors.textMuted,
                      fontSize: 11,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// Widget de sección con título
class SectionHeader extends StatelessWidget {
  final String title;
  final Widget? action;

  const SectionHeader({super.key, required this.title, this.action});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(
          title,
          style: GoogleFonts.inter(
            fontSize: 15,
            fontWeight: FontWeight.w700,
            color: AppColors.textPrimary,
          ),
        ),
        const Spacer(),
        if (action != null) action!,
      ],
    );
  }
}

/// SnackBar de éxito
void showSuccess(BuildContext context, String message) {
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(
    content: Row(children: [
      const Icon(Icons.check_circle_outline, color: Colors.white, size: 18),
      const SizedBox(width: 8),
      Expanded(child: Text(message)),
    ]),
    backgroundColor: AppColors.success,
  ));
}

/// SnackBar de error
void showError(BuildContext context, String message) {
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(
    content: Row(children: [
      const Icon(Icons.error_outline, color: Colors.white, size: 18),
      const SizedBox(width: 8),
      Expanded(child: Text(message)),
    ]),
    backgroundColor: AppColors.danger,
  ));
}
