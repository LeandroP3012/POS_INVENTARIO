import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../core/api_client.dart';
import '../core/app_theme.dart';

// ── Screen ────────────────────────────────────────────────────────────────────

class RolesScreen extends StatefulWidget {
  const RolesScreen({super.key});

  @override
  State<RolesScreen> createState() => _RolesScreenState();
}

class _RolesScreenState extends State<RolesScreen> {
  List<Map<String, dynamic>> _roles = [];
  Map<String, List<Map<String, dynamic>>> _catalog = {};
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final results = await Future.wait([
        ApiClient.instance.get('/roles/'),
        ApiClient.instance.get('/roles/permissions-catalog'),
      ]);
      final rolesData = results[0].data;
      final catalogData = results[1].data;

      List<Map<String, dynamic>> roles = [];
      if (rolesData is Map && rolesData['data'] != null) {
        roles = List<Map<String, dynamic>>.from(rolesData['data'] as List);
      } else if (rolesData is List) {
        roles = List<Map<String, dynamic>>.from(rolesData);
      }

      Map<String, List<Map<String, dynamic>>> catalog = {};
      if (catalogData is Map && catalogData['data'] != null) {
        final raw = catalogData['data'] as Map;
        raw.forEach((key, value) {
          catalog[key as String] =
              List<Map<String, dynamic>>.from(value as List);
        });
      }

      setState(() {
        _roles = roles;
        _catalog = catalog;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _loading = false;
        _error =
            'No se pudieron cargar los roles.\n${e.toString().length > 100 ? e.toString().substring(0, 100) : e.toString()}';
      });
    }
  }

  void _showRoleDetail(Map<String, dynamic> role) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => _RoleDetailScreen(
          role: role,
          catalog: _catalog,
          onSaved: _load,
        ),
      ),
    );
  }

  void _showCreateRole() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => _RoleDetailScreen(
          role: null,
          catalog: _catalog,
          onSaved: _load,
        ),
      ),
    );
  }

  Future<void> _deleteRole(Map<String, dynamic> role) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: Text('Eliminar rol',
            style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
        content: Text(
          '¿Eliminar el rol "${role['name']}"? Esta acción no se puede deshacer.',
          style: GoogleFonts.inter(color: AppColors.textSecondary),
        ),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancelar')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.danger,
                foregroundColor: Colors.white),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
    if (confirmed != true || !mounted) return;
    try {
      await ApiClient.instance.delete('/roles/${role['id']}');
      _load();
      if (mounted) showSuccess(context, 'Rol eliminado');
    } catch (e) {
      if (mounted) showError(context, 'No se pudo eliminar: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Column(
        children: [
          // ── Header ─────────────────────────────────────────────────────
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [AppColors.primary, Color(0xFF34495E)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            padding: const EdgeInsets.fromLTRB(24, 28, 24, 28),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Roles y Permisos',
                          style: GoogleFonts.inter(
                              color: Colors.white,
                              fontSize: 22,
                              fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      Text('${_roles.length} roles configurados',
                          style: GoogleFonts.inter(
                              color: Colors.white54, fontSize: 12)),
                    ],
                  ),
                ),
                ElevatedButton.icon(
                  icon: const Icon(Icons.add_rounded, size: 18),
                  label: const Text('Nuevo rol'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.accent,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 14, vertical: 10),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10)),
                  ),
                  onPressed: _showCreateRole,
                ),
              ],
            ),
          ),

          // ── Content ────────────────────────────────────────────────────
          Expanded(
            child: _loading
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
                                icon:
                                    const Icon(Icons.refresh_rounded, size: 16),
                                label: const Text('Reintentar'),
                                onPressed: _load,
                              ),
                            ],
                          ),
                        ),
                      )
                    : RefreshIndicator(
                        onRefresh: _load,
                        color: AppColors.accent,
                        child: ListView.separated(
                          padding: const EdgeInsets.all(16),
                          itemCount: _roles.length,
                          separatorBuilder: (_, __) =>
                              const SizedBox(height: 10),
                          itemBuilder: (_, i) => _RoleCard(
                            role: _roles[i],
                            onTap: () => _showRoleDetail(_roles[i]),
                            onDelete: _roles[i]['can_delete'] == true
                                ? () => _deleteRole(_roles[i])
                                : null,
                          ),
                        ),
                      ),
          ),
        ],
      ),
    );
  }
}

// ── Role card ─────────────────────────────────────────────────────────────────

class _RoleCard extends StatelessWidget {
  final Map<String, dynamic> role;
  final VoidCallback onTap;
  final VoidCallback? onDelete;

  const _RoleCard({required this.role, required this.onTap, this.onDelete});

  @override
  Widget build(BuildContext context) {
    final isSystem = role['system_role'] == true;
    final permCount = (role['permissions'] as List?)?.length ?? 0;
    final userCount = role['users_count'] ?? 0;

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSystem
                ? AppColors.accent.withValues(alpha: 0.3)
                : AppColors.cardBorder,
            width: isSystem ? 1.5 : 1,
          ),
        ),
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: isSystem
                    ? AppColors.accent.withValues(alpha: 0.1)
                    : AppColors.background,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                isSystem ? Icons.shield_rounded : Icons.manage_accounts_rounded,
                color: isSystem ? AppColors.accent : AppColors.textSecondary,
                size: 24,
              ),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(children: [
                    Text(role['name'] ?? '',
                        style: GoogleFonts.inter(
                            fontWeight: FontWeight.w600,
                            fontSize: 15,
                            color: AppColors.textPrimary)),
                    if (isSystem) ...[
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: AppColors.accent.withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text('Sistema',
                            style: GoogleFonts.inter(
                                fontSize: 10,
                                color: AppColors.accent,
                                fontWeight: FontWeight.w600)),
                      ),
                    ],
                  ]),
                  const SizedBox(height: 4),
                  Text(
                    role['description'] ?? '',
                    style: GoogleFonts.inter(
                        fontSize: 12, color: AppColors.textSecondary),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 8),
                  Row(children: [
                    _RoleStat(
                        icon: Icons.lock_outline_rounded,
                        label: '$permCount permisos'),
                    const SizedBox(width: 16),
                    _RoleStat(
                        icon: Icons.people_outline_rounded,
                        label: '$userCount usuarios'),
                  ]),
                ],
              ),
            ),
            Column(
              children: [
                const Icon(Icons.chevron_right_rounded,
                    color: AppColors.textMuted),
                if (onDelete != null)
                  IconButton(
                    icon: const Icon(Icons.delete_outline_rounded,
                        color: AppColors.danger, size: 20),
                    tooltip: 'Eliminar rol',
                    onPressed: onDelete,
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _RoleStat extends StatelessWidget {
  final IconData icon;
  final String label;

  const _RoleStat({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Row(children: [
      Icon(icon, size: 13, color: AppColors.textMuted),
      const SizedBox(width: 4),
      Text(label,
          style: GoogleFonts.inter(fontSize: 11, color: AppColors.textMuted)),
    ]);
  }
}

// ── Role detail / editor ──────────────────────────────────────────────────────

class _RoleDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? role;
  final Map<String, List<Map<String, dynamic>>> catalog;
  final VoidCallback onSaved;

  const _RoleDetailScreen({
    this.role,
    required this.catalog,
    required this.onSaved,
  });

  @override
  State<_RoleDetailScreen> createState() => _RoleDetailScreenState();
}

class _RoleDetailScreenState extends State<_RoleDetailScreen> {
  late final TextEditingController _nameCtrl;
  late final TextEditingController _codeCtrl;
  late final TextEditingController _descCtrl;
  late Set<String> _selectedPerms;
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    final role = widget.role;
    _nameCtrl = TextEditingController(text: role?['name'] ?? '');
    _codeCtrl = TextEditingController(text: role?['code'] ?? '');
    _descCtrl = TextEditingController(text: role?['description'] ?? '');

    final rawPerms = role?['permissions'];
    if (rawPerms is List) {
      _selectedPerms = rawPerms
          .map((p) => p is Map ? (p['code'] ?? p.toString()) : p.toString())
          .toSet()
          .cast<String>();
    } else {
      _selectedPerms = {};
    }
  }

  @override
  void dispose() {
    _nameCtrl.dispose();
    _codeCtrl.dispose();
    _descCtrl.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (_nameCtrl.text.trim().isEmpty) {
      showError(context, 'El nombre del rol es requerido');
      return;
    }
    setState(() => _saving = true);
    try {
      final payload = {
        'name': _nameCtrl.text.trim(),
        'code': _codeCtrl.text.trim().toLowerCase().replaceAll(' ', '_'),
        'description': _descCtrl.text.trim(),
        'permissions': _selectedPerms.toList(),
      };

      if (widget.role == null) {
        await ApiClient.instance.post('/roles/', data: payload);
      } else {
        payload.remove('code');
        await ApiClient.instance
            .put('/roles/${widget.role!['id']}', data: payload);
      }

      widget.onSaved();
      if (mounted) {
        Navigator.pop(context);
        showSuccess(
            context, widget.role == null ? 'Rol creado' : 'Rol actualizado');
      }
    } catch (e) {
      setState(() => _saving = false);
      if (mounted) showError(context, 'Error al guardar: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    final isEdit = widget.role != null;
    final isSystem = widget.role?['system_role'] == true;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.primary,
        iconTheme: const IconThemeData(color: Colors.white),
        title: Text(
          isEdit ? 'Editar rol' : 'Nuevo rol',
          style: GoogleFonts.inter(
              color: Colors.white, fontWeight: FontWeight.w600),
        ),
        actions: [
          if (!isSystem)
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
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Datos básicos
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.cardBorder),
            ),
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Información del rol',
                    style: GoogleFonts.inter(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                        color: AppColors.textPrimary)),
                const SizedBox(height: 14),
                TextField(
                  controller: _nameCtrl,
                  enabled: !isSystem,
                  decoration: InputDecoration(
                    labelText: 'Nombre *',
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8)),
                    isDense: true,
                  ),
                ),
                const SizedBox(height: 10),
                if (!isEdit)
                  TextField(
                    controller: _codeCtrl,
                    decoration: InputDecoration(
                      labelText: 'Código (único, sin espacios)',
                      hintText: 'Ej: vendedor_junior',
                      border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8)),
                      isDense: true,
                    ),
                  ),
                if (!isEdit) const SizedBox(height: 10),
                TextField(
                  controller: _descCtrl,
                  enabled: !isSystem,
                  maxLines: 2,
                  decoration: InputDecoration(
                    labelText: 'Descripción',
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8)),
                    isDense: true,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // Permisos por módulo
          Text('Permisos',
              style: GoogleFonts.inter(
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                  color: AppColors.textPrimary)),
          const SizedBox(height: 10),

          ...widget.catalog.entries.map((entry) => _PermissionGroup(
                module: entry.key,
                permissions: entry.value,
                selected: _selectedPerms,
                readOnly: isSystem,
                onChanged: (code, val) {
                  setState(() {
                    if (val) {
                      _selectedPerms.add(code);
                    } else {
                      _selectedPerms.remove(code);
                    }
                  });
                },
              )),
        ],
      ),
    );
  }
}

class _PermissionGroup extends StatefulWidget {
  final String module;
  final List<Map<String, dynamic>> permissions;
  final Set<String> selected;
  final bool readOnly;
  final void Function(String code, bool val) onChanged;

  const _PermissionGroup({
    required this.module,
    required this.permissions,
    required this.selected,
    required this.readOnly,
    required this.onChanged,
  });

  @override
  State<_PermissionGroup> createState() => _PermissionGroupState();
}

class _PermissionGroupState extends State<_PermissionGroup> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    final allSelected =
        widget.permissions.every((p) => widget.selected.contains(p['code']));
    final someSelected =
        widget.permissions.any((p) => widget.selected.contains(p['code']));

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: Column(
        children: [
          // Header del módulo
          InkWell(
            onTap: () => setState(() => _expanded = !_expanded),
            borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Row(
                children: [
                  if (!widget.readOnly)
                    Checkbox(
                      value: allSelected
                          ? true
                          : someSelected
                              ? null
                              : false,
                      tristate: true,
                      activeColor: AppColors.accent,
                      onChanged: (val) {
                        for (final p in widget.permissions) {
                          widget.onChanged(p['code'] as String, val == true);
                        }
                      },
                    ),
                  Expanded(
                    child: Text(
                      widget.module,
                      style: GoogleFonts.inter(
                          fontWeight: FontWeight.w600,
                          fontSize: 14,
                          color: AppColors.textPrimary),
                    ),
                  ),
                  Text(
                    '${widget.permissions.where((p) => widget.selected.contains(p['code'])).length}/${widget.permissions.length}',
                    style: GoogleFonts.inter(
                        fontSize: 12, color: AppColors.textSecondary),
                  ),
                  const SizedBox(width: 8),
                  Icon(
                    _expanded
                        ? Icons.keyboard_arrow_up_rounded
                        : Icons.keyboard_arrow_down_rounded,
                    color: AppColors.textMuted,
                  ),
                ],
              ),
            ),
          ),
          if (_expanded)
            ...widget.permissions.map((perm) {
              final code = perm['code'] as String;
              final selected = widget.selected.contains(code);
              return CheckboxListTile(
                value: selected,
                activeColor: AppColors.accent,
                dense: true,
                controlAffinity: ListTileControlAffinity.leading,
                title: Text(perm['label'] ?? code,
                    style: GoogleFonts.inter(
                        fontSize: 13, color: AppColors.textPrimary)),
                subtitle: perm['description'] != null
                    ? Text(perm['description'] as String,
                        style: GoogleFonts.inter(
                            fontSize: 11, color: AppColors.textSecondary))
                    : null,
                onChanged: widget.readOnly
                    ? null
                    : (val) => widget.onChanged(code, val ?? false),
              );
            }),
        ],
      ),
    );
  }
}
