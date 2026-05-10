import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

// ── Modelo ────────────────────────────────────────────────────────────────────

class PrinterConfig {
  final String id;
  String name;
  String ip;
  int port;
  bool isDefault;

  PrinterConfig({
    required this.id,
    required this.name,
    required this.ip,
    this.port = 9100,
    this.isDefault = false,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'ip': ip,
        'port': port,
        'isDefault': isDefault,
      };

  factory PrinterConfig.fromJson(Map<String, dynamic> j) => PrinterConfig(
        id: j['id'] as String,
        name: j['name'] as String,
        ip: j['ip'] as String,
        port: (j['port'] as num?)?.toInt() ?? 9100,
        isDefault: (j['isDefault'] as bool?) ?? false,
      );

  PrinterConfig copyWith({
    String? name,
    String? ip,
    int? port,
    bool? isDefault,
  }) =>
      PrinterConfig(
        id: id,
        name: name ?? this.name,
        ip: ip ?? this.ip,
        port: port ?? this.port,
        isDefault: isDefault ?? this.isDefault,
      );
}

// ── Provider ──────────────────────────────────────────────────────────────────

class PrinterProvider extends ChangeNotifier {
  static const _prefsKey = 'printer_configs';

  List<PrinterConfig> _printers = [];
  bool _printing = false;
  String? _lastPrintError;

  List<PrinterConfig> get printers => List.unmodifiable(_printers);
  bool get printing => _printing;
  String? get lastPrintError => _lastPrintError;

  PrinterConfig? get defaultPrinter =>
      _printers.where((p) => p.isDefault).firstOrNull;

  // ── Persistencia ─────────────────────────────────────────────────────────

  Future<void> load() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final raw = prefs.getString(_prefsKey);
      if (raw != null) {
        final list = jsonDecode(raw) as List<dynamic>;
        _printers = list
            .map((e) => PrinterConfig.fromJson(e as Map<String, dynamic>))
            .toList();
        notifyListeners();
      }
    } catch (_) {}
  }

  Future<void> _save() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(
          _prefsKey, jsonEncode(_printers.map((p) => p.toJson()).toList()));
    } catch (_) {}
  }

  // ── CRUD ──────────────────────────────────────────────────────────────────

  Future<void> addPrinter(PrinterConfig printer) async {
    // Si es la primera, la marcamos como default automáticamente
    if (_printers.isEmpty) {
      _printers.add(printer.copyWith(isDefault: true));
    } else {
      if (printer.isDefault) _clearDefault();
      _printers.add(printer);
    }
    await _save();
    notifyListeners();
  }

  Future<void> updatePrinter(PrinterConfig updated) async {
    final idx = _printers.indexWhere((p) => p.id == updated.id);
    if (idx < 0) return;
    if (updated.isDefault) _clearDefault();
    _printers[idx] = updated;
    await _save();
    notifyListeners();
  }

  Future<void> deletePrinter(String id) async {
    final wasDefault = _printers.any((p) => p.id == id && p.isDefault);
    _printers.removeWhere((p) => p.id == id);
    // Si borramos el default, asignamos el primero si existe
    if (wasDefault && _printers.isNotEmpty) {
      _printers[0] = _printers[0].copyWith(isDefault: true);
    }
    await _save();
    notifyListeners();
  }

  Future<void> setDefault(String id) async {
    _clearDefault();
    final idx = _printers.indexWhere((p) => p.id == id);
    if (idx >= 0) {
      _printers[idx] = _printers[idx].copyWith(isDefault: true);
    }
    await _save();
    notifyListeners();
  }

  void _clearDefault() {
    for (var i = 0; i < _printers.length; i++) {
      if (_printers[i].isDefault) {
        _printers[i] = _printers[i].copyWith(isDefault: false);
      }
    }
  }

  // ── Impresión directa por TCP ────────────────────────────────────────────

  /// Genera bytes ESC/POS del ticket y los envía directamente a la impresora.
  Future<bool> printTicket({
    required PrinterConfig printer,
    required Map<String, dynamic> saleData,
  }) async {
    _printing = true;
    _lastPrintError = null;
    notifyListeners();
    try {
      final bytes = _buildTicket(saleData);
      await _sendToPrinter(printer.ip, printer.port, bytes);
      _printing = false;
      notifyListeners();
      return true;
    } catch (e) {
      _lastPrintError = e.toString();
      _printing = false;
      notifyListeners();
      return false;
    }
  }

  /// Envía una línea de prueba a la impresora.
  Future<bool> testPrinter(PrinterConfig printer) async {
    _printing = true;
    _lastPrintError = null;
    notifyListeners();
    try {
      final buf = BytesBuilder();
      buf.add(_esc(0x40)); // INIT
      buf.add(_esc2(0x61, 0x01)); // CENTER
      buf.add(_esc(0x45, 0x01)); // BOLD ON
      buf.add(_latin('-- PRUEBA DE IMPRESION --\n'));
      buf.add(_esc(0x45, 0x00)); // BOLD OFF
      buf.add(_latin('T-Gestiona POS\n'));
      buf.add(List.filled(42, 0x2D) + [0x0A]); // línea
      buf.add(_latin('Impresora configurada OK\n'));
      buf.add([0x0A, 0x0A, 0x0A]);
      buf.add([0x1D, 0x56, 0x41, 0x03]); // CORTE
      await _sendToPrinter(printer.ip, printer.port, buf.toBytes());
      _printing = false;
      notifyListeners();
      return true;
    } catch (e) {
      _lastPrintError = e.toString();
      _printing = false;
      notifyListeners();
      return false;
    }
  }

  // ── TCP helper ────────────────────────────────────────────────────────────

  Future<void> _sendToPrinter(String ip, int port, List<int> data) async {
    final socket =
        await Socket.connect(ip, port, timeout: const Duration(seconds: 5));
    socket.add(data);
    await socket.flush();
    await socket.close();
  }

  // ── ESC/POS builder ───────────────────────────────────────────────────────

  List<int> _esc(int cmd, [int? param]) =>
      param == null ? [0x1B, cmd] : [0x1B, cmd, param];

  List<int> _esc2(int cmd, int param) => [0x1B, cmd, param];

  List<int> _gs(int cmd, int param) => [0x1D, cmd, param];

  List<int> _latin(String text) => latin1.encode(text.replaceAll('\n', '\n'));

  List<int> _buildTicket(Map<String, dynamic> sale) {
    final buf = BytesBuilder();
    const lf = [0x0A];
    final sep = List.filled(42, 0x2D) + lf;

    buf.add(_esc(0x40)); // INIT
    buf.add(_esc2(0x61, 0x01)); // CENTER
    buf.add(_gs(0x21, 0x11)); // 2x tamaño
    buf.add(_esc(0x45, 0x01)); // BOLD
    buf.add(_latin('T-GESTIONA POS\n'));
    buf.add(_gs(0x21, 0x00)); // Normal
    buf.add(_esc(0x45, 0x00)); // BOLD OFF
    buf.add(_latin('Sistema de Punto de Venta\n'));
    buf.add(sep);

    buf.add(_esc2(0x61, 0x00)); // LEFT
    final saleId = sale['sale_id'] ?? sale['id'] ?? '';
    final date = (sale['sale_date'] ?? sale['created_at'] ?? '').toString();
    final cashier = sale['cashier_name'] ?? sale['user'] ?? '';
    buf.add(_latin('Venta N: $saleId\n'));
    buf.add(
        _latin('Fecha : ${date.length > 19 ? date.substring(0, 19) : date}\n'));
    if (cashier.isNotEmpty) buf.add(_latin('Cajero: $cashier\n'));
    buf.add(sep);

    final items = (sale['items'] ?? sale['cart_items'] ?? []) as List;
    for (final item in items) {
      final name =
          (item['product_name'] ?? item['name'] ?? 'Producto').toString();
      final qty = item['quantity'] ?? 1;
      final price = double.tryParse(item['unit_price']?.toString() ??
              item['price']?.toString() ??
              '0') ??
          0;
      final sub =
          double.tryParse(item['subtotal']?.toString() ?? '0') ?? qty * price;
      buf.add(_latin('  ${name.length > 30 ? name.substring(0, 30) : name}\n'));
      buf.add(_twoCol('  $qty x S/ ${price.toStringAsFixed(2)}',
          'S/ ${sub.toStringAsFixed(2)}'));
    }
    buf.add(sep);

    final payment = (sale['payment_info'] ?? {}) as Map;
    final total = double.tryParse(
            (sale['total_amount'] ?? payment['total'] ?? 0).toString()) ??
        0;
    final paid = double.tryParse(
            (payment['paid_amount'] ?? sale['paid_amount'] ?? total)
                .toString()) ??
        0;
    final change = double.tryParse(
            (payment['change_amount'] ?? sale['change_amount'] ?? 0)
                .toString()) ??
        0;
    final method = (payment['method'] ?? sale['payment_method'] ?? 'Efectivo')
        .toString()
        .toUpperCase();
    final hasTax = payment['include_tax'] ?? true;

    if (hasTax == true && total > 0) {
      final base = total / 1.18;
      final igv = total - base;
      buf.add(_twoCol('  OP. GRAVADA:', 'S/ ${base.toStringAsFixed(2)}'));
      buf.add(_twoCol('  IGV (18%):', 'S/ ${igv.toStringAsFixed(2)}'));
    }
    buf.add(_esc(0x45, 0x01)); // BOLD
    buf.add(_twoCol('  TOTAL:', 'S/ ${total.toStringAsFixed(2)}'));
    buf.add(_esc(0x45, 0x00)); // BOLD OFF
    buf.add(_twoCol('  $method:', 'S/ ${paid.toStringAsFixed(2)}'));
    if (change > 0)
      buf.add(_twoCol('  VUELTO:', 'S/ ${change.toStringAsFixed(2)}'));

    buf.add(sep);
    buf.add(_esc2(0x61, 0x01)); // CENTER
    buf.add(_latin('Gracias por su compra\n'));
    buf.add(_latin('Conserve su ticket\n'));
    buf.add([0x0A, 0x0A, 0x0A]);
    buf.add([0x1D, 0x56, 0x41, 0x03]); // CORTE
    return buf.toBytes();
  }

  List<int> _twoCol(String left, String right, {int width = 42}) {
    final r = right.length > 20 ? right.substring(right.length - 20) : right;
    final l = left.length > (width - r.length - 1)
        ? left.substring(0, width - r.length - 1)
        : left;
    final line = l.padRight(width - r.length) + r;
    return _latin('$line\n');
  }

  String _parseError(dynamic e) {
    try {
      final data = (e as dynamic).response?.data;
      if (data is Map) return data['detail']?.toString() ?? 'Error';
    } catch (_) {}
    return 'Error de conexi\u00f3n con la impresora';
  }
}
