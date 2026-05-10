import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

import '../core/api_client.dart';
import '../core/app_theme.dart';

// ── Screen ────────────────────────────────────────────────────────────────────

class CategoriesScreen extends StatefulWidget {
  const CategoriesScreen({super.key});

  @override
  State<CategoriesScreen> createState() => _CategoriesScreenState();
}

class _CategoriesScreenState extends State<CategoriesScreen> {
  List<Map<String, dynamic>> _categories = [];
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
      final res = await ApiClient.instance.get('/categories/');
      final data = res.data;
      if (data is List) {
        setState(() {
          _categories = List<Map<String, dynamic>>.from(data);
          _loading = false;
        });
      } else if (data is Map && data['data'] != null) {
        setState(() {
          _categories = List<Map<String, dynamic>>.from(data['data'] as List);
          _loading = false;
        });
      } else {
        setState(() {
          _categories = [];
          _loading = false;
        });
      }
    } catch (e) {
      setState(() {
        _loading = false;
        _error =
            'No se pudieron cargar las categorías.\n${e.toString().length > 100 ? e.toString().substring(0, 100) : e.toString()}';
      });
    }
  }

  void _showForm({Map<String, dynamic>? existing}) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => _CategoryForm(
        existing: existing,
        onSave: (name, desc) async {
          try {
            if (existing == null) {
              await ApiClient.instance.post('/categories/', data: {
                'name': name,
                'description': desc,
              });
            } else {
              await ApiClient.instance.put('/categories/${existing['id']}',
                  data: {'name': name, 'description': desc});
            }
            if (!mounted) return;
            _load();
            showSuccess(
                context,
                existing == null
                    ? 'Categoría creada'
                    : 'Categoría actualizada');
          } catch (e) {
            if (!mounted) return;
            showError(context, 'Error al guardar: $e');
          }
        },
      ),
    );
  }

  Future<void> _delete(Map<String, dynamic> cat) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: Text('Eliminar categoría',
            style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
        content: Text(
          '¿Seguro que deseas eliminar "${cat['name']}"? Esta acción no se puede deshacer.',
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
      await ApiClient.instance.delete('/categories/${cat['id']}');
      _load();
      if (mounted) showSuccess(context, 'Categoría eliminada');
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
                      Text('Categorías',
                          style: GoogleFonts.inter(
                              color: Colors.white,
                              fontSize: 22,
                              fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      Text('${_categories.length} categorías registradas',
                          style: GoogleFonts.inter(
                              color: Colors.white54, fontSize: 12)),
                    ],
                  ),
                ),
                ElevatedButton.icon(
                  icon: const Icon(Icons.add_rounded, size: 18),
                  label: const Text('Nueva'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.accent,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 10),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10)),
                  ),
                  onPressed: () => _showForm(),
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
                    : _categories.isEmpty
                        ? Center(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.category_outlined,
                                    size: 64,
                                    color: AppColors.textMuted
                                        .withValues(alpha: 0.4)),
                                const SizedBox(height: 16),
                                Text('Sin categorías',
                                    style: GoogleFonts.inter(
                                        fontSize: 16,
                                        fontWeight: FontWeight.w600,
                                        color: AppColors.textPrimary)),
                                const SizedBox(height: 8),
                                Text('Crea la primera categoría de productos',
                                    style: GoogleFonts.inter(
                                        color: AppColors.textSecondary,
                                        fontSize: 13)),
                              ],
                            ),
                          )
                        : RefreshIndicator(
                            onRefresh: _load,
                            color: AppColors.accent,
                            child: ListView.separated(
                              padding: const EdgeInsets.all(16),
                              itemCount: _categories.length,
                              separatorBuilder: (_, __) =>
                                  const SizedBox(height: 10),
                              itemBuilder: (_, i) => _CategoryCard(
                                category: _categories[i],
                                onEdit: () =>
                                    _showForm(existing: _categories[i]),
                                onDelete: () => _delete(_categories[i]),
                              ),
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}

// ── Category card ─────────────────────────────────────────────────────────────

class _CategoryCard extends StatelessWidget {
  final Map<String, dynamic> category;
  final VoidCallback onEdit;
  final VoidCallback onDelete;

  const _CategoryCard({
    required this.category,
    required this.onEdit,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    final isActive = (category['status'] ?? 'active') == 'active';
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
        leading: Container(
          width: 44,
          height: 44,
          decoration: BoxDecoration(
            color: AppColors.accent.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(10),
          ),
          child: const Icon(Icons.category_rounded,
              color: AppColors.accent, size: 22),
        ),
        title: Text(
          category['name'] ?? '',
          style: GoogleFonts.inter(
              fontWeight: FontWeight.w600,
              fontSize: 15,
              color: AppColors.textPrimary),
        ),
        subtitle: category['description'] != null &&
                (category['description'] as String).isNotEmpty
            ? Text(
                category['description'],
                style: GoogleFonts.inter(
                    fontSize: 12, color: AppColors.textSecondary),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              )
            : null,
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: isActive
                    ? AppColors.success.withValues(alpha: 0.12)
                    : AppColors.textMuted.withValues(alpha: 0.12),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                isActive ? 'Activa' : 'Inactiva',
                style: GoogleFonts.inter(
                  fontSize: 10,
                  fontWeight: FontWeight.w600,
                  color: isActive ? AppColors.success : AppColors.textMuted,
                ),
              ),
            ),
            const SizedBox(width: 4),
            PopupMenuButton<String>(
              icon: const Icon(Icons.more_vert_rounded,
                  color: AppColors.textSecondary, size: 20),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10)),
              onSelected: (v) {
                if (v == 'edit') onEdit();
                if (v == 'delete') onDelete();
              },
              itemBuilder: (_) => [
                PopupMenuItem(
                  value: 'edit',
                  child: Row(children: [
                    const Icon(Icons.edit_outlined,
                        size: 18, color: AppColors.accent),
                    const SizedBox(width: 10),
                    Text('Editar', style: GoogleFonts.inter()),
                  ]),
                ),
                PopupMenuItem(
                  value: 'delete',
                  child: Row(children: [
                    const Icon(Icons.delete_outline_rounded,
                        size: 18, color: AppColors.danger),
                    const SizedBox(width: 10),
                    Text('Eliminar',
                        style: GoogleFonts.inter(color: AppColors.danger)),
                  ]),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// ── Category form sheet ───────────────────────────────────────────────────────

class _CategoryForm extends StatefulWidget {
  final Map<String, dynamic>? existing;
  final void Function(String name, String desc) onSave;

  const _CategoryForm({this.existing, required this.onSave});

  @override
  State<_CategoryForm> createState() => _CategoryFormState();
}

class _CategoryFormState extends State<_CategoryForm> {
  late final TextEditingController _nameCtrl;
  late final TextEditingController _descCtrl;
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    _nameCtrl = TextEditingController(text: widget.existing?['name'] ?? '');
    _descCtrl =
        TextEditingController(text: widget.existing?['description'] ?? '');
  }

  @override
  void dispose() {
    _nameCtrl.dispose();
    _descCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (_nameCtrl.text.trim().isEmpty) {
      showError(context, 'El nombre es requerido');
      return;
    }
    setState(() => _saving = true);
    widget.onSave(_nameCtrl.text.trim(), _descCtrl.text.trim());
    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final isEdit = widget.existing != null;
    return Padding(
      padding:
          EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
      child: Container(
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        ),
        padding: const EdgeInsets.fromLTRB(24, 20, 24, 32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    isEdit ? 'Editar categoría' : 'Nueva categoría',
                    style: GoogleFonts.inter(
                        fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close_rounded),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _nameCtrl,
              autofocus: true,
              textCapitalization: TextCapitalization.words,
              decoration: InputDecoration(
                labelText: 'Nombre *',
                hintText: 'Ej: Bebidas, Electrónica...',
                prefixIcon: const Icon(Icons.label_outline_rounded),
                border:
                    OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 14),
            TextField(
              controller: _descCtrl,
              decoration: InputDecoration(
                labelText: 'Descripción (opcional)',
                hintText: 'Descripción breve de la categoría',
                prefixIcon: const Icon(Icons.notes_rounded),
                border:
                    OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _saving ? null : _submit,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.accent,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10)),
                ),
                child: _saving
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2))
                    : Text(isEdit ? 'Guardar cambios' : 'Crear categoría',
                        style: GoogleFonts.inter(
                            fontWeight: FontWeight.w600, fontSize: 15)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
