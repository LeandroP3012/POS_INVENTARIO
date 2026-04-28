import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../core/api_client.dart';

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

  // ── Impresión ─────────────────────────────────────────────────────────────

  /// Envía el ticket al backend para imprimir en [printer].
  /// [saleData] es el resultado de /api/sales/.
  Future<bool> printTicket({
    required PrinterConfig printer,
    required Map<String, dynamic> saleData,
  }) async {
    _printing = true;
    _lastPrintError = null;
    notifyListeners();

    try {
      await ApiClient.instance.post('/print/ticket', data: {
        'printer_ip': printer.ip,
        'printer_port': printer.port,
        'sale': saleData,
      });
      _printing = false;
      notifyListeners();
      return true;
    } catch (e) {
      _lastPrintError = _parseError(e);
      _printing = false;
      notifyListeners();
      return false;
    }
  }

  /// Prueba de conexión con la impresora (imprime línea de prueba).
  Future<bool> testPrinter(PrinterConfig printer) async {
    _printing = true;
    _lastPrintError = null;
    notifyListeners();

    try {
      await ApiClient.instance.post('/print/test', data: {
        'printer_ip': printer.ip,
        'printer_port': printer.port,
      });
      _printing = false;
      notifyListeners();
      return true;
    } catch (e) {
      _lastPrintError = _parseError(e);
      _printing = false;
      notifyListeners();
      return false;
    }
  }

  String _parseError(dynamic e) {
    try {
      final data = (e as dynamic).response?.data;
      if (data is Map) return data['detail']?.toString() ?? 'Error';
    } catch (_) {}
    return 'Error de conexión con la impresora';
  }
}
