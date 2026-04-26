import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';

import '../core/api_client.dart';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({super.key});

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  bool _loading = false;
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

    final fmt = DateFormat('yyyy-MM-dd');
    try {
      final salesRes = await ApiClient.instance.get('/reports/sales', params: {
        'start_date': fmt.format(_startDate),
        'end_date': fmt.format(_endDate),
      });
      final dailyRes = await ApiClient.instance.get('/reports/daily', params: {
        'report_date': fmt.format(DateTime.now()),
      });

      setState(() {
        _salesData = salesRes.data as Map<String, dynamic>;
        _dailyData = dailyRes.data as Map<String, dynamic>;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }

    final summary = _salesData?['summary'] as Map<String, dynamic>?;
    final dailySummary = _dailyData?['summary'] as Map<String, dynamic>?;

    return RefreshIndicator(
      onRefresh: _loadReports,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Hoy
          Text('Hoy - ${DateFormat('dd/MM/yyyy').format(DateTime.now())}',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: _StatCard(
                  title: 'Ventas',
                  value: dailySummary?['total_sales']?.toString() ?? '0',
                  icon: Icons.receipt,
                  color: Colors.blue,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _StatCard(
                  title: 'Ingresos',
                  value: _currency.format(
                      (dailySummary?['total_revenue'] as num?)?.toDouble() ?? 0),
                  icon: Icons.attach_money,
                  color: Colors.green,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          // Periodo
          Text(
              'Últimos 30 días',
              style: Theme.of(context)
                  .textTheme
                  .titleMedium
                  ?.copyWith(fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: _StatCard(
                  title: 'Total ventas',
                  value: summary?['total_transactions']?.toString() ?? '0',
                  icon: Icons.shopping_cart,
                  color: Colors.purple,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _StatCard(
                  title: 'Total ingresos',
                  value: _currency.format(
                      (summary?['total_revenue'] as num?)?.toDouble() ?? 0),
                  icon: Icons.trending_up,
                  color: Colors.orange,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          // Gráfico de ventas diarias
          if (_salesData?['daily_sales'] != null) ...[
            Text('Ventas por día',
                style: Theme.of(context)
                    .textTheme
                    .titleMedium
                    ?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            SizedBox(
              height: 200,
              child: _SalesChart(
                  dailySales: _salesData!['daily_sales'] as List),
            ),
          ],
        ],
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;

  const _StatCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(value,
                style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: color)),
            const SizedBox(height: 4),
            Text(title,
                style: const TextStyle(color: Colors.grey, fontSize: 12)),
          ],
        ),
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
      final revenue =
          (e.value['total_revenue'] as num?)?.toDouble() ?? 0;
      return FlSpot(e.key.toDouble(), revenue);
    }).toList();

    return LineChart(
      LineChartData(
        gridData: const FlGridData(show: false),
        titlesData: const FlTitlesData(show: false),
        borderData: FlBorderData(show: false),
        lineBarsData: [
          LineChartBarData(
            spots: spots,
            isCurved: true,
            color: const Color(0xFF3498db),
            barWidth: 3,
            belowBarData: BarAreaData(
              show: true,
              color: const Color(0xFF3498db).withValues(alpha: 0.15),
            ),
            dotData: const FlDotData(show: false),
          ),
        ],
      ),
    );
  }
}
