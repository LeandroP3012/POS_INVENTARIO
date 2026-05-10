import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

import '../core/app_theme.dart';
import '../providers/auth_provider.dart';
import '../providers/printer_provider.dart';
import 'roles_screen.dart';
import 'ticket_config_screen.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: CustomScrollView(
        slivers: [
          // ── Encabezado ───────────────────────────────────────────────────
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
                          'Configuración',
                          style: GoogleFonts.inter(
                            color: Colors.white,
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Impresoras y preferencias del sistema',
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
                    child: const Icon(Icons.settings_rounded,
                        color: Colors.white, size: 26),
                  ),
                ],
              ),
            ),
          ),

          SliverPadding(
            padding: const EdgeInsets.all(16),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                // ── Sección impresoras ───────────────────────────────────
                _SectionHeader(
                  title: 'Impresoras de tickets',
                  action: TextButton.icon(
                    icon: const Icon(Icons.add_rounded, size: 16),
                    label: const Text('Agregar'),
                    onPressed: () => _showPrinterDialog(context, null),
                  ),
                ),
                const SizedBox(height: 10),
                const _PrinterList(),
                const SizedBox(height: 28),

                // ── Sección ajustes ───────────────────────────────────────
                const _SectionHeader(title: 'Ajustes del sistema'),
                const SizedBox(height: 10),
                _SettingsTile(
                  icon: Icons.receipt_long_outlined,
                  title: 'Configuración del ticket',
                  subtitle: 'Empresa, RUC, pie de página, opciones',
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (_) => const TicketConfigScreen()),
                  ),
                ),
                const SizedBox(height: 8),
                _SettingsTile(
                  icon: Icons.manage_accounts_rounded,
                  title: 'Roles y permisos',
                  subtitle: 'Gestionar roles de usuario y accesos',
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const RolesScreen()),
                  ),
                ),
                const SizedBox(height: 28),

                // ── Sección cuenta ────────────────────────────────────────
                const _SectionHeader(title: 'Cuenta'),
                const SizedBox(height: 10),
                const _AccountCard(),
                const SizedBox(height: 16),
              ]),
            ),
          ),
        ],
      ),
    );
  }

  static void _showPrinterDialog(
      BuildContext context, PrinterConfig? existing) {
    showDialog(
      context: context,
      builder: (_) => _PrinterDialog(existing: existing),
    );
  }
}

// ── Lista de impresoras ────────────────────────────────────────────────────────

class _PrinterList extends StatelessWidget {
  const _PrinterList();

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<PrinterProvider>();
    final printers = provider.printers;

    if (printers.isEmpty) {
      return Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.divider),
        ),
        child: Column(
          children: [
            Icon(Icons.print_disabled_rounded,
                size: 40, color: AppColors.textMuted.withValues(alpha: 0.5)),
            const SizedBox(height: 12),
            Text(
              'Sin impresoras configuradas',
              style: GoogleFonts.inter(
                color: AppColors.textSecondary,
                fontSize: 14,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              'Agrega una ticketera con su dirección IP',
              style: GoogleFonts.inter(
                color: AppColors.textMuted,
                fontSize: 12,
              ),
            ),
          ],
        ),
      );
    }

    return Column(
      children: printers
          .map((p) => Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: _PrinterCard(printer: p),
              ))
          .toList(),
    );
  }
}

// ── Tarjeta de impresora ──────────────────────────────────────────────────────

class _PrinterCard extends StatelessWidget {
  final PrinterConfig printer;

  const _PrinterCard({required this.printer});

  @override
  Widget build(BuildContext context) {
    final provider = context.read<PrinterProvider>();

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: printer.isDefault
              ? AppColors.accent.withValues(alpha: 0.5)
              : AppColors.divider,
          width: printer.isDefault ? 1.5 : 1,
        ),
      ),
      child: Column(
        children: [
          ListTile(
            contentPadding:
                const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            leading: Container(
              width: 44,
              height: 44,
              decoration: BoxDecoration(
                color: printer.isDefault
                    ? AppColors.accent.withValues(alpha: 0.1)
                    : AppColors.background,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(
                  color: printer.isDefault
                      ? AppColors.accent.withValues(alpha: 0.3)
                      : AppColors.divider,
                ),
              ),
              child: Icon(
                Icons.print_rounded,
                color:
                    printer.isDefault ? AppColors.accent : AppColors.textMuted,
                size: 22,
              ),
            ),
            title: Row(
              children: [
                Expanded(
                  child: Text(
                    printer.name,
                    style: GoogleFonts.inter(
                      fontWeight: FontWeight.w600,
                      fontSize: 14,
                      color: AppColors.textPrimary,
                    ),
                  ),
                ),
                if (printer.isDefault)
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: AppColors.accent.withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      'Predeterminada',
                      style: GoogleFonts.inter(
                        color: AppColors.accent,
                        fontSize: 10,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
              ],
            ),
            subtitle: Text(
              '${printer.ip}:${printer.port}',
              style: GoogleFonts.robotoMono(
                color: AppColors.textSecondary,
                fontSize: 12,
              ),
            ),
            trailing: PopupMenuButton<String>(
              icon: const Icon(Icons.more_vert_rounded,
                  color: AppColors.textMuted, size: 20),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10)),
              onSelected: (value) => _onMenuAction(context, value, provider),
              itemBuilder: (_) => [
                if (!printer.isDefault)
                  const PopupMenuItem(
                    value: 'default',
                    child: Row(children: [
                      Icon(Icons.star_rounded,
                          size: 18, color: AppColors.accent),
                      SizedBox(width: 10),
                      Text('Marcar como predeterminada'),
                    ]),
                  ),
                const PopupMenuItem(
                  value: 'test',
                  child: Row(children: [
                    Icon(Icons.print_rounded, size: 18, color: AppColors.info),
                    SizedBox(width: 10),
                    Text('Prueba de impresión'),
                  ]),
                ),
                const PopupMenuItem(
                  value: 'edit',
                  child: Row(children: [
                    Icon(Icons.edit_rounded,
                        size: 18, color: AppColors.textSecondary),
                    SizedBox(width: 10),
                    Text('Editar'),
                  ]),
                ),
                const PopupMenuItem(
                  value: 'delete',
                  child: Row(children: [
                    Icon(Icons.delete_outline_rounded,
                        size: 18, color: AppColors.danger),
                    SizedBox(width: 10),
                    Text('Eliminar', style: TextStyle(color: AppColors.danger)),
                  ]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _onMenuAction(
      BuildContext context, String action, PrinterProvider provider) async {
    switch (action) {
      case 'default':
        await provider.setDefault(printer.id);
        break;

      case 'test':
        _showTestDialog(context, provider);
        break;

      case 'edit':
        if (context.mounted) {
          showDialog(
            context: context,
            builder: (_) => _PrinterDialog(existing: printer),
          );
        }
        break;

      case 'delete':
        if (context.mounted) _confirmDelete(context, provider);
        break;
    }
  }

  void _showTestDialog(BuildContext context, PrinterProvider provider) async {
    final messenger = ScaffoldMessenger.of(context);
    final ok = await provider.testPrinter(printer);
    if (!context.mounted) return;
    messenger.showSnackBar(SnackBar(
      content: Text(ok
          ? '✓ Impresora respondió correctamente'
          : 'Error: ${provider.lastPrintError}'),
      backgroundColor: ok ? AppColors.success : AppColors.danger,
    ));
  }

  void _confirmDelete(BuildContext context, PrinterProvider provider) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        title: const Text('Eliminar impresora'),
        content: Text('¿Eliminar "${printer.name}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: AppColors.danger),
            onPressed: () async {
              await provider.deletePrinter(printer.id);
              if (ctx.mounted) Navigator.pop(ctx);
            },
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
  }
}

// ── Diálogo agregar/editar impresora ─────────────────────────────────────────

class _PrinterDialog extends StatefulWidget {
  final PrinterConfig? existing;

  const _PrinterDialog({this.existing});

  @override
  State<_PrinterDialog> createState() => _PrinterDialogState();
}

class _PrinterDialogState extends State<_PrinterDialog> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _nameCtrl;
  late final TextEditingController _ipCtrl;
  late final TextEditingController _portCtrl;
  bool _isDefault = false;

  @override
  void initState() {
    super.initState();
    _nameCtrl = TextEditingController(text: widget.existing?.name ?? '');
    _ipCtrl = TextEditingController(text: widget.existing?.ip ?? '');
    _portCtrl = TextEditingController(text: '${widget.existing?.port ?? 9100}');
    _isDefault = widget.existing?.isDefault ?? false;
  }

  @override
  void dispose() {
    _nameCtrl.dispose();
    _ipCtrl.dispose();
    _portCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isEdit = widget.existing != null;
    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      title: Text(isEdit ? 'Editar impresora' : 'Nueva impresora'),
      content: Form(
        key: _formKey,
        child: SizedBox(
          width: 360,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Nombre
              TextFormField(
                controller: _nameCtrl,
                decoration: const InputDecoration(
                  labelText: 'Nombre',
                  hintText: 'Ej: Ticketera Caja 1',
                  prefixIcon: Icon(Icons.label_outline_rounded),
                ),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? 'Requerido' : null,
              ),
              const SizedBox(height: 14),

              // IP
              TextFormField(
                controller: _ipCtrl,
                decoration: const InputDecoration(
                  labelText: 'Dirección IP',
                  hintText: '192.168.1.100',
                  prefixIcon: Icon(Icons.lan_outlined),
                ),
                keyboardType:
                    const TextInputType.numberWithOptions(decimal: true),
                validator: (v) {
                  if (v == null || v.trim().isEmpty) return 'Requerido';
                  final ipRegex =
                      RegExp(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$');
                  if (!ipRegex.hasMatch(v.trim())) return 'IP inválida';
                  return null;
                },
              ),
              const SizedBox(height: 14),

              // Puerto
              TextFormField(
                controller: _portCtrl,
                decoration: const InputDecoration(
                  labelText: 'Puerto',
                  hintText: '9100',
                  prefixIcon: Icon(Icons.settings_ethernet_rounded),
                ),
                keyboardType: TextInputType.number,
                inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                validator: (v) {
                  if (v == null || v.isEmpty) return 'Requerido';
                  final port = int.tryParse(v);
                  if (port == null || port < 1 || port > 65535) {
                    return 'Puerto inválido (1-65535)';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 10),

              // Default switch
              SwitchListTile(
                value: _isDefault,
                onChanged: (v) => setState(() => _isDefault = v),
                title: Text(
                  'Impresora predeterminada',
                  style: GoogleFonts.inter(fontSize: 13),
                ),
                contentPadding: EdgeInsets.zero,
                dense: true,
                activeColor: AppColors.accent,
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancelar'),
        ),
        FilledButton(
          onPressed: _submit,
          child: Text(isEdit ? 'Guardar' : 'Agregar'),
        ),
      ],
    );
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    final provider = context.read<PrinterProvider>();
    final config = PrinterConfig(
      id: widget.existing?.id ??
          DateTime.now().millisecondsSinceEpoch.toString(),
      name: _nameCtrl.text.trim(),
      ip: _ipCtrl.text.trim(),
      port: int.parse(_portCtrl.text.trim()),
      isDefault: _isDefault,
    );

    if (widget.existing != null) {
      await provider.updatePrinter(config);
    } else {
      await provider.addPrinter(config);
    }

    if (mounted) Navigator.pop(context);
  }
}

// ── Tarjeta de cuenta ─────────────────────────────────────────────────────────

class _AccountCard extends StatelessWidget {
  const _AccountCard();

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthProvider>().currentUser;

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.divider),
      ),
      child: Column(
        children: [
          ListTile(
            leading: CircleAvatar(
              radius: 22,
              backgroundColor: AppColors.accent,
              child: Text(
                (user?.fullName.isNotEmpty == true ? user!.fullName[0] : 'U')
                    .toUpperCase(),
                style: GoogleFonts.inter(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 17,
                ),
              ),
            ),
            title: Text(
              user?.fullName ?? 'Usuario',
              style:
                  GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 14),
            ),
            subtitle: Text(
              '@${user?.username ?? ''}  •  ${user?.userType ?? ''}',
              style: GoogleFonts.inter(
                  color: AppColors.textSecondary, fontSize: 12),
            ),
          ),
          const Divider(height: 1),
          ListTile(
            leading: const Icon(Icons.logout_rounded, color: AppColors.danger),
            title: const Text('Cerrar sesión',
                style: TextStyle(color: AppColors.danger)),
            onTap: () => _confirmLogout(context),
          ),
        ],
      ),
    );
  }

  void _confirmLogout(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        title: const Text('Cerrar sesión'),
        content: const Text('¿Seguro que deseas cerrar la sesión actual?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: AppColors.danger),
            onPressed: () async {
              await context.read<AuthProvider>().logout();
              if (ctx.mounted) {
                Navigator.pop(ctx);
                Navigator.pushReplacementNamed(ctx, '/login');
              }
            },
            child: const Text('Cerrar sesión'),
          ),
        ],
      ),
    );
  }
}

// ── Widgets auxiliares ────────────────────────────────────────────────────────

class _SettingsTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _SettingsTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.cardBorder),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        child: Row(
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: AppColors.accent.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(icon, color: AppColors.accent, size: 22),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title,
                      style: GoogleFonts.inter(
                          fontWeight: FontWeight.w600,
                          fontSize: 14,
                          color: AppColors.textPrimary)),
                  const SizedBox(height: 2),
                  Text(subtitle,
                      style: GoogleFonts.inter(
                          fontSize: 12, color: AppColors.textSecondary)),
                ],
              ),
            ),
            const Icon(Icons.chevron_right_rounded, color: AppColors.textMuted),
          ],
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  final Widget? action;

  const _SectionHeader({required this.title, this.action});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(
          title,
          style: GoogleFonts.inter(
            fontSize: 13,
            fontWeight: FontWeight.w700,
            color: AppColors.textSecondary,
            letterSpacing: 0.4,
          ),
        ),
        const Spacer(),
        if (action != null) action!,
      ],
    );
  }
}
