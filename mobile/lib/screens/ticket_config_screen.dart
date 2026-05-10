import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../core/api_client.dart';
import '../core/app_theme.dart';

class TicketConfigScreen extends StatefulWidget {
  const TicketConfigScreen({super.key});

  @override
  State<TicketConfigScreen> createState() => _TicketConfigScreenState();
}

class _TicketConfigScreenState extends State<TicketConfigScreen> {
  bool _loading = true;
  bool _saving = false;
  String? _error;

  final _nameCtrl = TextEditingController();
  final _rucCtrl = TextEditingController();
  final _addressCtrl = TextEditingController();
  final _cityCtrl = TextEditingController();
  final _phoneCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _footer1Ctrl = TextEditingController();
  final _footer2Ctrl = TextEditingController();

  bool _printCopy = true;
  bool _showLogo = false;
  bool _showBarcode = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void dispose() {
    for (final c in [
      _nameCtrl,
      _rucCtrl,
      _addressCtrl,
      _cityCtrl,
      _phoneCtrl,
      _emailCtrl,
      _footer1Ctrl,
      _footer2Ctrl
    ]) {
      c.dispose();
    }
    super.dispose();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final res = await ApiClient.instance.get('/settings/ticket');
      final data =
          (res.data as Map<String, dynamic>)['data'] as Map<String, dynamic>;
      setState(() {
        _nameCtrl.text = data['company_name'] ?? '';
        _rucCtrl.text = data['company_ruc'] ?? '';
        _addressCtrl.text = data['company_address'] ?? '';
        _cityCtrl.text = data['company_city'] ?? '';
        _phoneCtrl.text = data['company_phone'] ?? '';
        _emailCtrl.text = data['company_email'] ?? '';
        _footer1Ctrl.text = data['footer_message'] ?? '';
        _footer2Ctrl.text = data['footer_message_2'] ?? '';
        _printCopy = data['print_copy'] ?? true;
        _showLogo = data['show_logo'] ?? false;
        _showBarcode = data['show_barcode'] ?? false;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _loading = false;
        _error =
            'No se pudo cargar la configuración.\n${e.toString().length > 100 ? e.toString().substring(0, 100) : e.toString()}';
      });
    }
  }

  Future<void> _save() async {
    setState(() => _saving = true);
    try {
      await ApiClient.instance.put('/settings/ticket', data: {
        'company_name': _nameCtrl.text.trim(),
        'company_ruc': _rucCtrl.text.trim(),
        'company_address': _addressCtrl.text.trim(),
        'company_city': _cityCtrl.text.trim(),
        'company_phone': _phoneCtrl.text.trim(),
        'company_email': _emailCtrl.text.trim(),
        'footer_message': _footer1Ctrl.text.trim(),
        'footer_message_2': _footer2Ctrl.text.trim(),
        'print_copy': _printCopy,
        'show_logo': _showLogo,
        'show_barcode': _showBarcode,
      });
      if (mounted) showSuccess(context, 'Configuración guardada correctamente');
    } catch (e) {
      if (mounted) showError(context, 'Error al guardar: $e');
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.primary,
        iconTheme: const IconThemeData(color: Colors.white),
        title: Text('Configuración del ticket',
            style: GoogleFonts.inter(
                color: Colors.white, fontWeight: FontWeight.w600)),
        actions: [
          if (!_loading && _error == null)
            TextButton(
              onPressed: _saving ? null : _save,
              child: _saving
                  ? const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(
                          color: Colors.white, strokeWidth: 2))
                  : Text('Guardar',
                      style: GoogleFonts.inter(
                          color: Colors.white, fontWeight: FontWeight.w600)),
            ),
        ],
      ),
      body: _loading
          ? const Center(
              child: CircularProgressIndicator(color: AppColors.accent))
          : _error != null
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(32),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.error_outline_rounded,
                            color: AppColors.danger, size: 48),
                        const SizedBox(height: 16),
                        Text(_error!,
                            textAlign: TextAlign.center,
                            style: GoogleFonts.inter(
                                color: AppColors.textSecondary)),
                        const SizedBox(height: 16),
                        OutlinedButton.icon(
                          icon: const Icon(Icons.refresh_rounded, size: 16),
                          label: const Text('Reintentar'),
                          onPressed: _load,
                        ),
                      ],
                    ),
                  ),
                )
              : ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    _Section(
                      title: 'Datos de la empresa',
                      icon: Icons.business_rounded,
                      children: [
                        _Field(
                            controller: _nameCtrl,
                            label: 'Nombre de la empresa',
                            icon: Icons.store_outlined),
                        _Field(
                            controller: _rucCtrl,
                            label: 'RUC',
                            icon: Icons.numbers_rounded,
                            keyboardType: TextInputType.number),
                        _Field(
                            controller: _addressCtrl,
                            label: 'Dirección',
                            icon: Icons.location_on_outlined),
                        _Field(
                            controller: _cityCtrl,
                            label: 'Ciudad / Distrito',
                            icon: Icons.location_city_outlined),
                        _Field(
                            controller: _phoneCtrl,
                            label: 'Teléfono',
                            icon: Icons.phone_outlined,
                            keyboardType: TextInputType.phone),
                        _Field(
                            controller: _emailCtrl,
                            label: 'Correo electrónico',
                            icon: Icons.email_outlined,
                            keyboardType: TextInputType.emailAddress),
                      ],
                    ),
                    const SizedBox(height: 16),
                    _Section(
                      title: 'Mensajes del ticket',
                      icon: Icons.message_outlined,
                      children: [
                        _Field(
                            controller: _footer1Ctrl,
                            label: 'Mensaje de pie 1',
                            icon: Icons.short_text_rounded),
                        _Field(
                            controller: _footer2Ctrl,
                            label: 'Mensaje de pie 2',
                            icon: Icons.short_text_rounded),
                      ],
                    ),
                    const SizedBox(height: 16),
                    _Section(
                      title: 'Opciones de impresión',
                      icon: Icons.print_outlined,
                      children: [
                        SwitchListTile(
                          value: _printCopy,
                          activeColor: AppColors.accent,
                          onChanged: (v) => setState(() => _printCopy = v),
                          title: Text('Imprimir copia',
                              style: GoogleFonts.inter(
                                  fontSize: 14, color: AppColors.textPrimary)),
                          subtitle: Text('Imprime duplicado del ticket',
                              style: GoogleFonts.inter(
                                  fontSize: 12,
                                  color: AppColors.textSecondary)),
                          secondary: const Icon(Icons.copy_outlined,
                              color: AppColors.textMuted),
                        ),
                        SwitchListTile(
                          value: _showLogo,
                          activeColor: AppColors.accent,
                          onChanged: (v) => setState(() => _showLogo = v),
                          title: Text('Mostrar logo',
                              style: GoogleFonts.inter(
                                  fontSize: 14, color: AppColors.textPrimary)),
                          subtitle: Text('Logo de empresa en el encabezado',
                              style: GoogleFonts.inter(
                                  fontSize: 12,
                                  color: AppColors.textSecondary)),
                          secondary: const Icon(Icons.image_outlined,
                              color: AppColors.textMuted),
                        ),
                        SwitchListTile(
                          value: _showBarcode,
                          activeColor: AppColors.accent,
                          onChanged: (v) => setState(() => _showBarcode = v),
                          title: Text('Código de barras',
                              style: GoogleFonts.inter(
                                  fontSize: 14, color: AppColors.textPrimary)),
                          subtitle: Text('Código de barras de la venta',
                              style: GoogleFonts.inter(
                                  fontSize: 12,
                                  color: AppColors.textSecondary)),
                          secondary: const Icon(Icons.qr_code_2_rounded,
                              color: AppColors.textMuted),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),
                    // Previsualización
                    _TicketPreview(
                      name: _nameCtrl.text,
                      ruc: _rucCtrl.text,
                      address: _addressCtrl.text,
                      city: _cityCtrl.text,
                      phone: _phoneCtrl.text,
                      footer1: _footer1Ctrl.text,
                      footer2: _footer2Ctrl.text,
                    ),
                    const SizedBox(height: 32),
                  ],
                ),
    );
  }
}

// ── Widgets auxiliares ────────────────────────────────────────────────────────

class _Section extends StatelessWidget {
  final String title;
  final IconData icon;
  final List<Widget> children;

  const _Section(
      {required this.title, required this.icon, required this.children});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 14, 16, 10),
            child: Row(children: [
              Icon(icon, size: 18, color: AppColors.accent),
              const SizedBox(width: 8),
              Text(title,
                  style: GoogleFonts.inter(
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                      color: AppColors.textPrimary)),
            ]),
          ),
          const Divider(height: 1),
          ...children,
        ],
      ),
    );
  }
}

class _Field extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final IconData icon;
  final TextInputType? keyboardType;

  const _Field({
    required this.controller,
    required this.label,
    required this.icon,
    this.keyboardType,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 10, 16, 4),
      child: TextField(
        controller: controller,
        keyboardType: keyboardType,
        style: GoogleFonts.inter(fontSize: 14),
        decoration: InputDecoration(
          labelText: label,
          prefixIcon: Icon(icon, size: 20, color: AppColors.textMuted),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
          isDense: true,
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        ),
      ),
    );
  }
}

class _TicketPreview extends StatelessWidget {
  final String name;
  final String ruc;
  final String address;
  final String city;
  final String phone;
  final String footer1;
  final String footer2;

  const _TicketPreview({
    required this.name,
    required this.ruc,
    required this.address,
    required this.city,
    required this.phone,
    required this.footer1,
    required this.footer2,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(children: [
          const Icon(Icons.receipt_outlined,
              size: 16, color: AppColors.textSecondary),
          const SizedBox(width: 6),
          Text('Vista previa del ticket',
              style: GoogleFonts.inter(
                  fontWeight: FontWeight.w700,
                  fontSize: 13,
                  color: AppColors.textSecondary)),
        ]),
        const SizedBox(height: 10),
        Center(
          child: Container(
            width: 240,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: AppColors.cardBorder),
              boxShadow: [
                BoxShadow(
                    color: Colors.black.withValues(alpha: 0.06),
                    blurRadius: 8,
                    offset: const Offset(0, 2))
              ],
            ),
            child: Column(
              children: [
                Text(
                  name.isNotEmpty ? name : 'NOMBRE DE EMPRESA',
                  textAlign: TextAlign.center,
                  style: GoogleFonts.robotoMono(
                      fontWeight: FontWeight.bold, fontSize: 13),
                ),
                const SizedBox(height: 2),
                if (ruc.isNotEmpty)
                  Text('RUC: $ruc',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.robotoMono(fontSize: 10)),
                if (address.isNotEmpty)
                  Text(address,
                      textAlign: TextAlign.center,
                      style: GoogleFonts.robotoMono(fontSize: 10)),
                if (city.isNotEmpty)
                  Text(city,
                      textAlign: TextAlign.center,
                      style: GoogleFonts.robotoMono(fontSize: 10)),
                if (phone.isNotEmpty)
                  Text('Tel: $phone',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.robotoMono(fontSize: 10)),
                const Padding(
                  padding: EdgeInsets.symmetric(vertical: 8),
                  child: Divider(height: 1),
                ),
                Text('BOLETA DE VENTA',
                    style: GoogleFonts.robotoMono(
                        fontSize: 11, fontWeight: FontWeight.bold)),
                const SizedBox(height: 4),
                Text('B001-00001', style: GoogleFonts.robotoMono(fontSize: 10)),
                const SizedBox(height: 4),
                const Divider(height: 1),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Producto ejemplo x1',
                        style: GoogleFonts.robotoMono(fontSize: 9)),
                    Text('S/ 10.00',
                        style: GoogleFonts.robotoMono(fontSize: 9)),
                  ],
                ),
                const SizedBox(height: 6),
                const Divider(height: 1),
                const SizedBox(height: 4),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('TOTAL',
                        style: GoogleFonts.robotoMono(
                            fontWeight: FontWeight.bold, fontSize: 12)),
                    Text('S/ 10.00',
                        style: GoogleFonts.robotoMono(
                            fontWeight: FontWeight.bold, fontSize: 12)),
                  ],
                ),
                const SizedBox(height: 8),
                const Divider(height: 1),
                const SizedBox(height: 6),
                if (footer1.isNotEmpty)
                  Text(footer1,
                      textAlign: TextAlign.center,
                      style: GoogleFonts.robotoMono(fontSize: 10)),
                if (footer2.isNotEmpty)
                  Text(footer2,
                      textAlign: TextAlign.center,
                      style: GoogleFonts.robotoMono(fontSize: 10)),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
