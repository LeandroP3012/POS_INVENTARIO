import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

import '../core/app_theme.dart';
import '../core/navigation_state.dart';
import '../providers/auth_provider.dart';
import 'dashboard_screen.dart';
import 'pos_screen.dart';
import 'products_screen.dart';
import 'reports_screen.dart';
import 'categories_screen.dart';
import 'settings_screen.dart';

// ── Modelo de elemento de navegación ─────────────────────────────────────────

class _NavTab {
  final IconData icon;
  final IconData activeIcon;
  final String label;
  final String section;

  const _NavTab({
    required this.icon,
    required this.activeIcon,
    required this.label,
    required this.section,
  });
}

// ── Pantalla principal con sidebar ────────────────────────────────────────────

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  @override
  void initState() {
    super.initState();
    tabIndexNotifier.addListener(_handleTabChange);
  }

  void _handleTabChange() => _onSelect(tabIndexNotifier.value);

  @override
  void dispose() {
    tabIndexNotifier.removeListener(_handleTabChange);
    super.dispose();
  }

  static const _tabs = [
    _NavTab(
      icon: Icons.dashboard_outlined,
      activeIcon: Icons.dashboard_rounded,
      label: 'Dashboard',
      section: 'Inicio',
    ),
    _NavTab(
      icon: Icons.point_of_sale_outlined,
      activeIcon: Icons.point_of_sale_rounded,
      label: 'Punto de Venta',
      section: 'Operaciones',
    ),
    _NavTab(
      icon: Icons.inventory_2_outlined,
      activeIcon: Icons.inventory_2_rounded,
      label: 'Productos',
      section: 'Operaciones',
    ),
    _NavTab(
      icon: Icons.bar_chart_outlined,
      activeIcon: Icons.bar_chart_rounded,
      label: 'Reportes',
      section: 'Análisis',
    ),
    _NavTab(
      icon: Icons.category_outlined,
      activeIcon: Icons.category_rounded,
      label: 'Categorías',
      section: 'Operaciones',
    ),
    _NavTab(
      icon: Icons.settings_outlined,
      activeIcon: Icons.settings_rounded,
      label: 'Configuración',
      section: 'Sistema',
    ),
  ];

  static const _screens = [
    DashboardScreen(),
    PosScreen(),
    ProductsScreen(),
    ReportsScreen(),
    CategoriesScreen(),
    SettingsScreen(),
  ];

  void _onSelect(int index) => setState(() => _selectedIndex = index);

  @override
  Widget build(BuildContext context) {
    final isWide = MediaQuery.sizeOf(context).width >= 900;

    if (isWide) {
      // ── Desktop / Tablet: sidebar permanente ──────────────────────────────
      return Scaffold(
        backgroundColor: AppColors.background,
        body: Row(
          children: [
            _AppSidebar(
              tabs: _tabs,
              selectedIndex: _selectedIndex,
              onSelect: _onSelect,
            ),
            const VerticalDivider(width: 1, thickness: 1),
            Expanded(child: _screens[_selectedIndex]),
          ],
        ),
      );
    }

    // ── Mobile: drawer + bottom nav ───────────────────────────────────────
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.primary,
        titleSpacing: 4,
        title: Row(
          children: [
            Container(
              width: 28,
              height: 28,
              decoration: BoxDecoration(
                color: AppColors.accent,
                borderRadius: BorderRadius.circular(6),
              ),
              child: const Icon(Icons.point_of_sale,
                  color: Colors.white, size: 16),
            ),
            const SizedBox(width: 8),
            Text(
              _tabs[_selectedIndex].label,
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w600,
                fontSize: 16,
              ),
            ),
          ],
        ),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      drawer: Drawer(
        width: 280,
        backgroundColor: AppColors.sidebarBg,
        child: _SidebarContent(
          tabs: _tabs,
          selectedIndex: _selectedIndex,
          onSelect: (i) {
            _onSelect(i);
            Navigator.pop(context);
          },
        ),
      ),
      body: _screens[_selectedIndex],
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          border: Border(top: BorderSide(color: AppColors.divider, width: 1)),
        ),
        child: NavigationBar(
          selectedIndex: _selectedIndex,
          onDestinationSelected: _onSelect,
          height: 64,
          destinations: _tabs
              .map((t) => NavigationDestination(
                    icon: Icon(t.icon),
                    selectedIcon: Icon(t.activeIcon),
                    label: t.label.split(' ').first,
                  ))
              .toList(),
        ),
      ),
    );
  }
}

// ── Sidebar (wrapper para desktop) ────────────────────────────────────────────

class _AppSidebar extends StatelessWidget {
  final List<_NavTab> tabs;
  final int selectedIndex;
  final void Function(int) onSelect;

  const _AppSidebar({
    required this.tabs,
    required this.selectedIndex,
    required this.onSelect,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 260,
      child: _SidebarContent(
        tabs: tabs,
        selectedIndex: selectedIndex,
        onSelect: onSelect,
      ),
    );
  }
}

// ── Contenido del sidebar ──────────────────────────────────────────────────────

class _SidebarContent extends StatelessWidget {
  final List<_NavTab> tabs;
  final int selectedIndex;
  final void Function(int) onSelect;

  const _SidebarContent({
    required this.tabs,
    required this.selectedIndex,
    required this.onSelect,
  });

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthProvider>().currentUser;

    return Container(
      color: AppColors.sidebarBg,
      child: Column(
        children: [
          // ── Logo ──────────────────────────────────────────────────────────
          SafeArea(
            bottom: false,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 18),
              decoration: BoxDecoration(
                border: Border(
                  bottom: BorderSide(
                    color: Colors.white.withValues(alpha: 0.07),
                    width: 1,
                  ),
                ),
              ),
              child: Row(
                children: [
                  Container(
                    width: 38,
                    height: 38,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [AppColors.accent, AppColors.accentDark],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(9),
                    ),
                    child: const Icon(Icons.point_of_sale,
                        color: Colors.white, size: 20),
                  ),
                  const SizedBox(width: 12),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        'T-Gestiona',
                        style: GoogleFonts.inter(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                          height: 1.1,
                        ),
                      ),
                      Text(
                        'POS System',
                        style: GoogleFonts.inter(
                          color: AppColors.sidebarText,
                          fontSize: 11,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),

          // ── Usuario actual ─────────────────────────────────────────────────
          Container(
            margin: const EdgeInsets.fromLTRB(12, 12, 12, 4),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.06),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(
                color: Colors.white.withValues(alpha: 0.08),
              ),
            ),
            child: Row(
              children: [
                CircleAvatar(
                  radius: 19,
                  backgroundColor: AppColors.accent,
                  child: Text(
                    (user?.fullName.isNotEmpty == true
                            ? user!.fullName[0]
                            : 'U')
                        .toUpperCase(),
                    style: GoogleFonts.inter(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 15,
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        user?.fullName ?? 'Usuario',
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: GoogleFonts.inter(
                          color: Colors.white,
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                          height: 1.2,
                        ),
                      ),
                      Text(
                        _getRoleLabel(user?.userType),
                        style: GoogleFonts.inter(
                          color: AppColors.sidebarText,
                          fontSize: 11,
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: AppColors.success.withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    'Activo',
                    style: GoogleFonts.inter(
                      color: AppColors.success,
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),

          // ── Navegación ─────────────────────────────────────────────────────
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              child: _buildNavGroups(context),
            ),
          ),

          // ── Cerrar sesión ──────────────────────────────────────────────────
          Container(
            decoration: BoxDecoration(
              border: Border(
                top: BorderSide(color: Colors.white.withValues(alpha: 0.07)),
              ),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
            child: _SidebarNavItem(
              icon: Icons.logout_rounded,
              label: 'Cerrar Sesión',
              isSelected: false,
              isDanger: true,
              onTap: () async {
                final nav = Navigator.of(context);
                await context.read<AuthProvider>().logout();
                nav.pushReplacementNamed('/login');
              },
            ),
          ),
          const SafeArea(top: false, child: SizedBox(height: 4)),
        ],
      ),
    );
  }

  Widget _buildNavGroups(BuildContext context) {
    String? lastSection;
    final items = <Widget>[];

    for (int i = 0; i < tabs.length; i++) {
      final tab = tabs[i];

      if (tab.section != lastSection) {
        if (lastSection != null) items.add(const SizedBox(height: 6));
        items.add(Padding(
          padding: const EdgeInsets.fromLTRB(12, 14, 12, 6),
          child: Text(
            tab.section.toUpperCase(),
            style: GoogleFonts.inter(
              color: AppColors.sidebarTextSection,
              fontSize: 10,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.2,
            ),
          ),
        ));
        lastSection = tab.section;
      }

      items.add(_SidebarNavItem(
        icon: selectedIndex == i ? tab.activeIcon : tab.icon,
        label: tab.label,
        isSelected: selectedIndex == i,
        onTap: () => onSelect(i),
      ));
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: items,
    );
  }

  static String _getRoleLabel(String? userType) {
    switch (userType) {
      case 'admin':
        return 'Administrador';
      case 'manager':
      case 'supervisor':
        return 'Supervisor';
      case 'cashier':
        return 'Cajero';
      case 'employee':
        return 'Empleado';
      default:
        return 'Usuario';
    }
  }
}

// ── Item de navegación del sidebar ────────────────────────────────────────────

class _SidebarNavItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool isSelected;
  final bool isDanger;
  final VoidCallback onTap;

  const _SidebarNavItem({
    required this.icon,
    required this.label,
    required this.isSelected,
    required this.onTap,
    this.isDanger = false,
  });

  @override
  Widget build(BuildContext context) {
    final textColor = isDanger
        ? AppColors.danger.withValues(alpha: 0.85)
        : isSelected
            ? Colors.white
            : AppColors.sidebarText;

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 1),
      decoration: BoxDecoration(
        color: isSelected
            ? Colors.white.withValues(alpha: 0.1)
            : Colors.transparent,
        borderRadius: BorderRadius.circular(8),
        border: isSelected
            ? const Border(
                left: BorderSide(color: AppColors.accent, width: 3),
              )
            : null,
      ),
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(8),
        child: InkWell(
          borderRadius: BorderRadius.circular(8),
          onTap: onTap,
          splashColor: Colors.white.withValues(alpha: 0.06),
          highlightColor: Colors.white.withValues(alpha: 0.04),
          child: Padding(
            padding: EdgeInsets.fromLTRB(
              isSelected ? 9 : 12,
              10,
              12,
              10,
            ),
            child: Row(
              children: [
                Icon(icon, color: textColor, size: 19),
                const SizedBox(width: 12),
                Text(
                  label,
                  style: GoogleFonts.inter(
                    color: textColor,
                    fontSize: 13.5,
                    fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
