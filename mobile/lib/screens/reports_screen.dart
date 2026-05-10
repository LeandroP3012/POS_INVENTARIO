import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';

import '../core/api_client.dart';
import '../core/app_theme.dart';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({super.key});

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  bool _loading = false;
  String? _errorMsg;
  Map<String, dynamic>? _salesData;
  Map<String, dynamic>? _dailyData;
  final _currency = NumberFormat.currency(locale: 'es_PE', symbol: 'S/ ');

  final DateTime _startDate = DateTime.now().subtract(const Duration(days: 30));
  final DateTime _endDate = DateTime.now();

  @override
  void initState() {
    super.initState();
    _loadReports();
  }

  Future<void> _loadReports() async {
    setState(() => _loading = true);
    _errorMsg = null;

    final fmt = DateFormat('yyyy-MM-dd');
    try {
      final salesRes = await ApiClient.instance.get('/reports/sales', params: {
        'start_date': fmt.format(_startDate),
        'end_date': fmt.format(_endDate),
      });
      final dailyRes = await ApiClient.instance.get('/reports/daily', params: {
        'report_date': fmt.format(DateTime.now()),
      });

      if (!mounted) return;
      setState(() {
        _salesData = salesRes.data as Map<String, dynamic>;
        _dailyData = dailyRes.data as Map<String, dynamic>;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      final msg = e.toString().contains('SocketException') ||
              e.toString().contains('Connection')
          ? 'Sin conexión a internet'
          : e.toString().contains('401')
              ? 'Sesión expirada — vuelve a iniciar sesión'
              : e.toString().contains('TimeoutException') ||
                      e.toString().contains('timeout')
                  ? 'El servidor tardó demasiado (Railway puede estar iniciando). Intenta de nuevo.'
                  : 'Error: ${e.toString().length > 100 ? e.toString().substring(0, 100) : e.toString()}';
      setState(() {
        _loading = false;
        _errorMsg = msg;
        _salesData = null;
        _dailyData = null;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        backgroundColor: AppColors.background,
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              CircularProgressIndicator(color: AppColors.accent),
              SizedBox(height: 12),
              Text('Cargando reportes...',
                  style: TextStyle(color: AppColors.textSecondary)),
            ],
          ),
        ),
      );
    }

    final summary = (_salesData?['data'] as Map<String, dynamic>?)?['summary']
        as Map<String, dynamic>?;
    final dailySummary = (_dailyData?['data']
        as Map<String, dynamic>?)?['sales_summary'] as Map<String, dynamic>?;
    final hasError = _salesData == null && _dailyData == null;

    if (hasError) {
      return Scaffold(
        backgroundColor: AppColors.background,
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 64,
                  height: 64,
                  decoration: BoxDecoration(
                    color: AppColors.danger.withValues(alpha: 0.1),
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.bar_chart_outlined,
                      color: AppColors.danger, size: 30),
                ),
                const SizedBox(height: 16),
                Text('No se pudieron cargar los reportes',
                    textAlign: TextAlign.center,
                    style: GoogleFonts.inter(
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimary,
                      fontSize: 16,
                    )),
                const SizedBox(height: 8),
                Text(_errorMsg ?? 'Verifica tu conexión e intenta de nuevo.',
                    textAlign: TextAlign.center,
                    style: GoogleFonts.inter(
                        color: AppColors.textSecondary, fontSize: 13)),
                const SizedBox(height: 24),
                ElevatedButton.icon(
                  icon: const Icon(Icons.refresh_rounded, size: 16),
                  label: const Text('Reintentar'),
                  onPressed: _loadReports,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.accent,
                    foregroundColor: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.background,
      body: RefreshIndicator(
        onRefresh: _loadReports,
        color: AppColors.accent,
        child: CustomScrollView(
          slivers: [
            // Encabezado resumen hoy
            SliverToBoxAdapter(
              child: Container(
                margin: const EdgeInsets.fromLTRB(16, 16, 16, 0),
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [AppColors.primary, Color(0xFF2E86C1)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Hoy — ${_spanishDate(DateTime.now())}',
                      style: GoogleFonts.inter(
                        color: Colors.white70,
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: _GradientKpi(
                            label: 'Ventas',
                            value:
                                dailySummary?['total_sales']?.toString() ?? '0',
                            icon: Icons.receipt_long_outlined,
                          ),
                        ),
                        Container(
                            width: 1,
                            height: 48,
                            color: Colors.white.withValues(alpha: 0.2)),
                        Expanded(
                          child: _GradientKpi(
                            label: 'Ingresos',
                            value: _currency.format(
                                (dailySummary?['total_amount'] as num?)
                                        ?.toDouble() ??
                                    0),
                            icon: Icons.attach_money_rounded,
                          ),
                        ),
                        Container(
                            width: 1,
                            height: 48,
                            color: Colors.white.withValues(alpha: 0.2)),
                        Expanded(
                          child: _GradientKpi(
                            label: 'Ticket prom.',
                            value: dailySummary?['total_sales'] != null &&
                                    (dailySummary!['total_sales'] as int) > 0
                                ? _currency.format(
                                    ((dailySummary['total_amount'] as num?)
                                                ?.toDouble() ??
                                            0) /
                                        (dailySummary['total_sales'] as int))
                                : 'S/ 0.00',
                            icon: Icons.shopping_bag_outlined,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            // KPIs últimos 30 días
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const _SectionLabel(
                        label: 'Últimos 30 días',
                        icon: Icons.calendar_month_outlined),
                    const SizedBox(height: 10),
                    Row(children: [
                      Expanded(
                        child: _KpiCard(
                          title: 'Transacciones',
                          value: summary?['total_sales']?.toString() ?? '0',
                          icon: Icons.point_of_sale_rounded,
                          iconColor: AppColors.accent,
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: _KpiCard(
                          title: 'Total ingresos',
                          value: _currency.format(
                              (summary?['total_amount'] as num?)?.toDouble() ??
                                  0),
                          icon: Icons.trending_up_rounded,
                          iconColor: AppColors.success,
                        ),
                      ),
                    ]),
                    const SizedBox(height: 10),
                    Row(children: [
                      Expanded(
                        child: _KpiCard(
                          title: 'Ticket promedio',
                          value: summary?['total_sales'] != null &&
                                  (summary!['total_sales'] as int) > 0
                              ? _currency.format(
                                  ((summary['total_amount'] as num?)
                                              ?.toDouble() ??
                                          0) /
                                      (summary['total_sales'] as int))
                              : 'S/ 0.00',
                          icon: Icons.receipt_outlined,
                          iconColor: AppColors.warning,
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: _KpiCard(
                          title: 'Promedio diario',
                          value: _currency.format(
                              ((summary?['total_amount'] as num?)?.toDouble() ??
                                      0) /
                                  30),
                          icon: Icons.today_outlined,
                          iconColor: const Color(0xFF9B59B6),
                        ),
                      ),
                    ]),
                  ],
                ),
              ),
            ),

            // Gráfico ventas diarias
            if ((_salesData?['data'] as Map?)?['daily_sales'] != null &&
                ((_salesData!['data'] as Map)['daily_sales'] as List)
                    .isNotEmpty)
              SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(16, 20, 16, 0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const _SectionLabel(
                          label: 'Ingresos por día',
                          icon: Icons.bar_chart_rounded),
                      const SizedBox(height: 12),
                      Container(
                        height: 200,
                        padding: const EdgeInsets.fromLTRB(8, 16, 16, 12),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(14),
                          border: Border.all(color: AppColors.cardBorder),
                        ),
                        child: _SalesChart(
                            dailySales: (_salesData!['data']
                                as Map)['daily_sales'] as List),
                      ),
                    ],
                  ),
                ),
              ),

            const SliverToBoxAdapter(child: SizedBox(height: 32)),
          ],
        ),
      ),
    );
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
    return '$dia, ${d.day} de $mes';
  }
}

// ── Widgets auxiliares ────────────────────────────────────────────────────────

class _SectionLabel extends StatelessWidget {
  final String label;
  final IconData icon;

  const _SectionLabel({required this.label, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Row(children: [
      Icon(icon, size: 16, color: AppColors.textSecondary),
      const SizedBox(width: 6),
      Text(
        label,
        style: GoogleFonts.inter(
          fontSize: 13,
          fontWeight: FontWeight.w700,
          color: AppColors.textPrimary,
          letterSpacing: 0.2,
        ),
      ),
    ]);
  }
}

class _GradientKpi extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;

  const _GradientKpi(
      {required this.label, required this.value, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Icon(icon, color: Colors.white70, size: 18),
        const SizedBox(height: 6),
        Text(
          value,
          style: GoogleFonts.inter(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        const SizedBox(height: 2),
        Text(
          label,
          style: GoogleFonts.inter(color: Colors.white60, fontSize: 11),
        ),
      ],
    );
  }
}

class _KpiCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color iconColor;

  const _KpiCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: iconColor.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, color: iconColor, size: 20),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  value,
                  style: GoogleFonts.inter(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textPrimary,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                Text(
                  title,
                  style: GoogleFonts.inter(
                    fontSize: 11,
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _SalesChart extends StatelessWidget {
  final List dailySales;

  const _SalesChart({required this.dailySales});

  @override
  Widget build(BuildContext context) {
    final spots = dailySales.asMap().entries.map((e) {
      final revenue = (e.value['total_amount'] as num?)?.toDouble() ?? 0;
      return FlSpot(e.key.toDouble(), revenue);
    }).toList();

    if (spots.isEmpty) {
      return Center(
        child: Text(
          'Sin datos para mostrar',
          style:
              GoogleFonts.inter(color: AppColors.textSecondary, fontSize: 13),
        ),
      );
    }

    return LineChart(
      LineChartData(
        gridData: FlGridData(
          show: true,
          drawVerticalLine: false,
          horizontalInterval: null,
          getDrawingHorizontalLine: (_) => const FlLine(
            color: AppColors.divider,
            strokeWidth: 1,
          ),
        ),
        titlesData: FlTitlesData(
          leftTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 40,
              getTitlesWidget: (value, _) => Text(
                'S/${value.toInt()}',
                style: GoogleFonts.inter(
                    fontSize: 9, color: AppColors.textSecondary),
              ),
            ),
          ),
          bottomTitles:
              const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles:
              const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          topTitles:
              const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        ),
        borderData: FlBorderData(show: false),
        lineBarsData: [
          LineChartBarData(
            spots: spots,
            isCurved: true,
            curveSmoothness: 0.3,
            color: AppColors.accent,
            barWidth: 2.5,
            belowBarData: BarAreaData(
              show: true,
              gradient: LinearGradient(
                colors: [
                  AppColors.accent.withValues(alpha: 0.2),
                  AppColors.accent.withValues(alpha: 0.01),
                ],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
              ),
            ),
            dotData: FlDotData(
              show: true,
              getDotPainter: (spot, _, __, ___) => FlDotCirclePainter(
                radius: 3,
                color: AppColors.accent,
                strokeWidth: 0,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
