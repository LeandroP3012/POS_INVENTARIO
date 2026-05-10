import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../core/api_client.dart';
import '../core/app_theme.dart';
import '../core/navigation_state.dart';
import '../providers/auth_provider.dart';
import '../providers/product_provider.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen>
    with WidgetsBindingObserver {
  Map<String, dynamic>? _dailyData;
  Map<String, dynamic>? _salesData;
  bool _loading = true;
  bool _refreshing = false; // refresco silencioso en fondo
  String? _error;

  // Última vez que los datos se cargaron con éxito.
  // Evita el "retry storm" cuando la app reanuda: si la carga anterior
  // fue hace menos de 30 s y hay datos, no se vuelve a pedir.
  DateTime? _lastSuccessfulLoad;

  static const _kMinRefreshInterval = Duration(seconds: 30);

  final _currency = NumberFormat.currency(locale: 'es_PE', symbol: 'S/ ');
  final _fmt = DateFormat('yyyy-MM-dd');

  static const _cacheKeyDaily = 'dashboard_cache_daily';
  static const _cacheKeySales = 'dashboard_cache_sales';

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ProductProvider>().loadProducts();
      _initData();
    });
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  /// Recarga datos cuando la app vuelve al primer plano.
  /// Guarda freno de 30 s para no disparar peticiones en cascada cuando
  /// el pool de BD está saturado (retry storm).
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state != AppLifecycleState.resumed) return;

    // Nunca lanzar si ya hay una carga en vuelo
    if (_loading || _refreshing) return;

    // Si hay datos recientes (< 30 s), no volver a pedir
    if (_dailyData != null && _lastSuccessfulLoad != null) {
      final elapsed = DateTime.now().difference(_lastSuccessfulLoad!);
      if (elapsed < _kMinRefreshInterval) return;
    }

    _loadData(silent: _dailyData != null);
  }

  /// Siempre carga datos frescos del servidor al entrar al tab.
  Future<void> _initData() async {
    _loadData(silent: false);
  }

  Future<void> _loadFromCache() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final dailyJson = prefs.getString(_cacheKeyDaily);
      final salesJson = prefs.getString(_cacheKeySales);
      if (dailyJson != null && salesJson != null && mounted) {
        setState(() {
          _dailyData = jsonDecode(dailyJson) as Map<String, dynamic>;
          _salesData = jsonDecode(salesJson) as Map<String, dynamic>;
          _loading = false;
        });
      }
    } catch (_) {}
  }

  Future<void> _saveToCache(
      Map<String, dynamic> daily, Map<String, dynamic> sales) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_cacheKeyDaily, jsonEncode(daily));
      await prefs.setString(_cacheKeySales, jsonEncode(sales));
    } catch (_) {}
  }

  Future<void> _loadData({bool silent = false}) async {
    if (silent) {
      if (mounted) setState(() => _refreshing = true);
    } else {
      if (mounted)
        setState(() {
          _loading = true;
          _error = null;
        });
    }
    try {
      final today = _fmt.format(DateTime.now());
      final start =
          _fmt.format(DateTime.now().subtract(const Duration(days: 6)));

      final results = await Future.wait([
        ApiClient.instance
            .get('/reports/daily', params: {'report_date': today}),
        ApiClient.instance.get('/reports/sales',
            params: {'start_date': start, 'end_date': today}),
      ]);

      if (!mounted) return;
      final daily = results[0].data as Map<String, dynamic>;
      final sales = results[1].data as Map<String, dynamic>;

      // Verificar éxito a nivel de API. El backend puede responder HTTP 200
      // con {success: false, message: '...'} cuando la BD falla, lo que no
      // lanza excepción de red y haría que todos los valores queden en 0.
      if (daily['success'] != true) {
        throw Exception(
            daily['message'] ?? 'Error al obtener el reporte diario');
      }
      if (sales['success'] != true) {
        throw Exception(
            sales['message'] ?? 'Error al obtener el reporte de ventas');
      }

      await _saveToCache(daily, sales);
      if (mounted) {
        setState(() {
          _dailyData = daily;
          _salesData = sales;
          _loading = false;
          _refreshing = false;
          _error = null;
          _lastSuccessfulLoad = DateTime.now();
        });
      }
    } catch (e) {
      if (mounted) {
        final msg = e.toString().contains('SocketException') ||
                e.toString().contains('Connection')
            ? 'Sin conexión a internet'
            : e.toString().contains('401')
                ? 'Sesión expirada — vuelve a iniciar sesión'
                : e.toString().contains('TimeoutException') ||
                        e.toString().contains('timeout')
                    ? 'El servidor tardó demasiado. Intenta de nuevo.'
                    : 'Error: ${e.toString().length > 80 ? e.toString().substring(0, 80) : e.toString()}';
        setState(() {
          _loading = false;
          _refreshing = false;
          if (_dailyData == null) _error = msg;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthProvider>().currentUser;
    final greeting = _getGreeting();

    return Scaffold(
      backgroundColor: AppColors.background,
      body: RefreshIndicator(
        onRefresh: () => _loadData(silent: false),
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
                    // Indicador de refresco silencioso
                    if (_refreshing)
                      const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white54,
                        ),
                      )
                    else
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

            // Banner sin conexión (solo cuando hay caché disponible)
            if (_error != null && _dailyData != null)
              SliverToBoxAdapter(
                child: Container(
                  margin: const EdgeInsets.fromLTRB(16, 12, 16, 0),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: AppColors.warning.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(
                        color: AppColors.warning.withValues(alpha: 0.4)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.wifi_off_rounded,
                          color: AppColors.warning, size: 18),
                      const SizedBox(width: 10),
                      const Expanded(
                        child: Text(
                          'Sin conexión — mostrando datos guardados',
                          style:
                              TextStyle(color: AppColors.warning, fontSize: 12),
                        ),
                      ),
                      TextButton(
                        style: TextButton.styleFrom(
                          padding: EdgeInsets.zero,
                          minimumSize: const Size(0, 0),
                          tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                        ),
                        onPressed: () => _loadData(silent: false),
                        child: const Text('Reintentar',
                            style: TextStyle(
                                fontSize: 12, color: AppColors.warning)),
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
                  : (_error != null && _dailyData == null)
                      ? SliverFillRemaining(
                          child: Center(
                            child: Padding(
                              padding: const EdgeInsets.all(24),
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const Icon(Icons.wifi_off_rounded,
                                      color: AppColors.danger, size: 48),
                                  const SizedBox(height: 16),
                                  Text(_error!,
                                      textAlign: TextAlign.center,
                                      style: const TextStyle(
                                          color: AppColors.textSecondary)),
                                  const SizedBox(height: 16),
                                  OutlinedButton.icon(
                                    icon: const Icon(Icons.refresh_rounded,
                                        size: 16),
                                    label: const Text('Reintentar'),
                                    onPressed: () => _loadData(silent: false),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        )
                      : SliverList(
                          delegate: SliverChildListDelegate([
                            // ── KPIs de hoy ─────────────────────────────────────
                            const SectionHeader(title: 'Resumen del día'),
                            const SizedBox(height: 12),
                            _buildKpiGrid(),
                            const SizedBox(height: 24),

                            // ── Métodos de pago hoy (condicional) ───────────────
                            _buildPaymentSection(),

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
    final daily = (_dailyData?['data']
        as Map<String, dynamic>?)?['sales_summary'] as Map<String, dynamic>?;
    final totalSales = daily?['total_sales'] ?? 0;
    final totalRevenue = (daily?['total_amount'] as num?)?.toDouble() ?? 0.0;
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
          title: 'Ingresos 7 días',
          value: _currency.format(
            (((_salesData?['data'] as Map?)?['summary']
                        as Map?)?['total_amount'] as num?)
                    ?.toDouble() ??
                0.0,
          ),
          icon: Icons.calendar_today_rounded,
          color: AppColors.info,
          subtitle:
              '${((_salesData?['data'] as Map?)?['summary'] as Map?)?['total_sales'] ?? 0} ventas',
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
        onTap: () => tabIndexNotifier.value = 1,
      ),
      _QuickAction(
        label: 'Ver Productos',
        icon: Icons.inventory_2_rounded,
        color: AppColors.success,
        onTap: () => tabIndexNotifier.value = 2,
      ),
      _QuickAction(
        label: 'Ver Reportes',
        icon: Icons.bar_chart_rounded,
        color: AppColors.warning,
        onTap: () => tabIndexNotifier.value = 3,
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

  // ── Sección de métodos de pago ──────────────────────────────────────────────

  Widget _buildPaymentSection() {
    final summary = (_dailyData?['data'] as Map?)?['sales_summary'] as Map?;
    final methods = summary?['payment_methods'] as Map?;
    if (methods == null || methods.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SectionHeader(title: 'Pagos de hoy'),
        const SizedBox(height: 12),
        ...methods.entries.map((e) {
          final name = e.key as String;
          final data = e.value as Map;
          final count = data['count'] as int? ?? 0;
          final amount = (data['amount'] as num?)?.toDouble() ?? 0.0;
          return Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppColors.cardBorder),
              ),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
              child: Row(
                children: [
                  Icon(_paymentIcon(name), size: 20, color: AppColors.accent),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      _capitalize(name),
                      style: GoogleFonts.inter(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: AppColors.textPrimary,
                      ),
                    ),
                  ),
                  Text(
                    '$count ${count == 1 ? 'venta' : 'ventas'}',
                    style: GoogleFonts.inter(
                        fontSize: 12, color: AppColors.textSecondary),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    _currency.format(amount),
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimary,
                    ),
                  ),
                ],
              ),
            ),
          );
        }),
        const SizedBox(height: 16),
      ],
    );
  }

  static IconData _paymentIcon(String method) {
    switch (method.toLowerCase()) {
      case 'efectivo':
        return Icons.payments_outlined;
      case 'tarjeta':
      case 'tarjeta_credito':
      case 'tarjeta_debito':
        return Icons.credit_card_rounded;
      case 'transferencia':
      case 'yape':
      case 'plin':
        return Icons.phone_android_rounded;
      default:
        return Icons.attach_money_rounded;
    }
  }

  static String _capitalize(String s) => s.isEmpty
      ? s
      : '${s[0].toUpperCase()}${s.substring(1).toLowerCase().replaceAll('_', ' ')}';

  static String _getGreeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return 'Buenos días,';
    if (hour < 18) return 'Buenas tardes,';
    return 'Buenas noches,';
  }

  static String _spanishDate(DateTime d) {
    const dias = [
      'lunes',
      'martes',
      'miércoles',
      'jueves',
      'viernes',
      'sábado',
      'domingo'
    ];
    const meses = [
      'enero',
      'febrero',
      'marzo',
      'abril',
      'mayo',
      'junio',
      'julio',
      'agosto',
      'septiembre',
      'octubre',
      'noviembre',
      'diciembre'
    ];
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
