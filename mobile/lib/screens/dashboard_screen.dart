import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../core/api_client.dart';
import '../core/app_theme.dart';
import '../providers/auth_provider.dart';
import '../providers/product_provider.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Map<String, dynamic>? _dailyData;
  Map<String, dynamic>? _salesData;
  bool _loading = true;

  final _currency = NumberFormat.currency(locale: 'es_PE', symbol: 'S/ ');
  final _fmt = DateFormat('yyyy-MM-dd');

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ProductProvider>().loadProducts();
      _loadData();
    });
  }

  Future<void> _loadData() async {
    setState(() => _loading = true);
    try {
      final today = _fmt.format(DateTime.now());
      final start = _fmt.format(DateTime.now().subtract(const Duration(days: 6)));

      final results = await Future.wait([
        ApiClient.instance.get('/reports/daily', params: {'report_date': today}),
        ApiClient.instance.get('/reports/sales', params: {'start_date': start, 'end_date': today}),
      ]);

      if (!mounted) return;
      setState(() {
        _dailyData = results[0].data as Map<String, dynamic>?;
        _salesData = results[1].data as Map<String, dynamic>?;
        _loading = false;
      });
    } catch (_) {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthProvider>().currentUser;
    final greeting = _getGreeting();

    return Scaffold(
      backgroundColor: AppColors.background,
      body: RefreshIndicator(
        onRefresh: _loadData,
        color: AppColors.accent,
        child: CustomScrollView(
          slivers: [
            // ── Encabezado ─────────────────────────────────────────────────
            SliverToBoxAdapter(
              child: Container(
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    colors: [AppColors.primary, Color(0xFF34495E)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                ),
                padding: const EdgeInsets.fromLTRB(24, 28, 24, 32),
                child: Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            greeting,
                            style: GoogleFonts.inter(
                              color: Colors.white60,
                              fontSize: 13,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            user?.fullName ?? 'Usuario',
                            style: GoogleFonts.inter(
                              color: Colors.white,
                              fontSize: 22,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            _spanishDate(DateTime.now()),
                            style: GoogleFonts.inter(
                              color: Colors.white54,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      width: 50,
                      height: 50,
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.12),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.dashboard_rounded,
                        color: Colors.white,
                        size: 26,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            SliverPadding(
              padding: const EdgeInsets.all(16),
              sliver: _loading
                  ? const SliverFillRemaining(
                      child: Center(child: CircularProgressIndicator()),
                    )
                  : SliverList(
                      delegate: SliverChildListDelegate([
                        // ── KPIs de hoy ─────────────────────────────────────
                        const SectionHeader(title: 'Resumen del día'),
                        const SizedBox(height: 12),
                        _buildKpiGrid(),
                        const SizedBox(height: 24),

                        // ── Inventario ──────────────────────────────────────
                        const SectionHeader(title: 'Estado del inventario'),
                        const SizedBox(height: 12),
                        _buildInventoryRow(),
                        const SizedBox(height: 24),

                        // ── Accesos rápidos ─────────────────────────────────
                        const SectionHeader(title: 'Accesos rápidos'),
                        const SizedBox(height: 12),
                        _buildQuickActions(context),
                        const SizedBox(height: 16),
                      ]),
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildKpiGrid() {
    final daily = _dailyData?['summary'] as Map<String, dynamic>?;
    final totalSales = daily?['total_sales'] ?? 0;
    final totalRevenue = (daily?['total_revenue'] as num?)?.toDouble() ?? 0.0;
    final avgTicket = totalSales > 0 ? totalRevenue / (totalSales as num) : 0.0;

    return LayoutBuilder(builder: (context, constraints) {
      final isWide = constraints.maxWidth > 500;
      final cards = [
        KpiCard(
          title: 'Ventas hoy',
          value: '$totalSales',
          icon: Icons.receipt_long_rounded,
          color: AppColors.accent,
          subtitle: 'transacciones',
        ),
        KpiCard(
          title: 'Ingresos hoy',
          value: _currency.format(totalRevenue),
          icon: Icons.attach_money_rounded,
          color: AppColors.success,
          subtitle: 'total cobrado',
        ),
        KpiCard(
          title: 'Ticket promedio',
          value: _currency.format(avgTicket),
          icon: Icons.trending_up_rounded,
          color: AppColors.warning,
          subtitle: 'por venta',
        ),
        KpiCard(
          title: 'Período (7 días)',
          value: '${_salesData?['summary']?['total_transactions'] ?? 0}',
          icon: Icons.calendar_today_rounded,
          color: AppColors.info,
          subtitle: 'ventas totales',
        ),
      ];

      if (isWide) {
        return Row(
          children: cards
              .asMap()
              .entries
              .map((e) => Expanded(
                    child: Padding(
                      padding: EdgeInsets.only(left: e.key > 0 ? 10 : 0),
                      child: e.value,
                    ),
                  ))
              .toList(),
        );
      }

      return Column(
        children: cards
            .map((c) => Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: c,
                ))
            .toList(),
      );
    });
  }

  Widget _buildInventoryRow() {
    return Consumer<ProductProvider>(builder: (_, pp, __) {
      final total = pp.products.length;
      final active = pp.products.where((p) => p.status == 'active').length;
      final lowStock = pp.lowStockProducts.length;
      final outOfStock = pp.products.where((p) => p.stockQuantity <= 0).length;

      return LayoutBuilder(builder: (context, constraints) {
        final isWide = constraints.maxWidth > 500;
        final cards = [
          KpiCard(
            title: 'Total productos',
            value: '$total',
            icon: Icons.inventory_2_rounded,
            color: AppColors.primary,
          ),
          KpiCard(
            title: 'Activos',
            value: '$active',
            icon: Icons.check_circle_outline_rounded,
            color: AppColors.success,
          ),
          KpiCard(
            title: 'Stock bajo',
            value: '$lowStock',
            icon: Icons.warning_amber_rounded,
            color: AppColors.warning,
          ),
          KpiCard(
            title: 'Sin stock',
            value: '$outOfStock',
            icon: Icons.remove_shopping_cart_outlined,
            color: AppColors.danger,
          ),
        ];

        if (isWide) {
          return Row(
            children: cards
                .asMap()
                .entries
                .map((e) => Expanded(
                      child: Padding(
                        padding: EdgeInsets.only(left: e.key > 0 ? 10 : 0),
                        child: e.value,
                      ),
                    ))
                .toList(),
          );
        }

        return Column(
          children: cards
              .map((c) => Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: c,
                  ))
              .toList(),
        );
      });
    });
  }

  Widget _buildQuickActions(BuildContext context) {
    final actions = [
      _QuickAction(
        label: 'Nueva Venta',
        icon: Icons.add_shopping_cart_rounded,
        color: AppColors.accent,
        onTap: () {
          // Navegar al tab Punto de Venta (index 1)
          final home = context.findAncestorStateOfType<State>();
          if (home != null) {
            final homeState = home as dynamic;
            try {
              homeState._onSelect(1);
            } catch (_) {}
          }
        },
      ),
      _QuickAction(
        label: 'Ver Productos',
        icon: Icons.inventory_2_rounded,
        color: AppColors.success,
        onTap: () {},
      ),
      _QuickAction(
        label: 'Ver Reportes',
        icon: Icons.bar_chart_rounded,
        color: AppColors.warning,
        onTap: () {},
      ),
    ];

    return Row(
      children: actions
          .asMap()
          .entries
          .map(
            (e) => Expanded(
              child: Padding(
                padding: EdgeInsets.only(left: e.key > 0 ? 10 : 0),
                child: _buildQuickActionCard(e.value),
              ),
            ),
          )
          .toList(),
    );
  }

  Widget _buildQuickActionCard(_QuickAction action) {
    return InkWell(
      onTap: action.onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
        decoration: BoxDecoration(
          color: action.color.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: action.color.withValues(alpha: 0.2)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 44,
              height: 44,
              decoration: BoxDecoration(
                color: action.color.withValues(alpha: 0.15),
                shape: BoxShape.circle,
              ),
              child: Icon(action.icon, color: action.color, size: 22),
            ),
            const SizedBox(height: 8),
            Text(
              action.label,
              textAlign: TextAlign.center,
              style: GoogleFonts.inter(
                color: action.color,
                fontSize: 12,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }

  static String _getGreeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return 'Buenos días,';
    if (hour < 18) return 'Buenas tardes,';
    return 'Buenas noches,';
  }

  static String _spanishDate(DateTime d) {
    const dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'];
    const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                   'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
    final dia = dias[d.weekday - 1];
    final mes = meses[d.month - 1];
    return '$dia, ${d.day} de $mes de ${d.year}';
  }
}

class _QuickAction {
  final String label;
  final IconData icon;
  final Color color;
  final VoidCallback onTap;

  const _QuickAction({
    required this.label,
    required this.icon,
    required this.color,
    required this.onTap,
  });
}
