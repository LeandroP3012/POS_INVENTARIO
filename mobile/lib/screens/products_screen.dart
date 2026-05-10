import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../core/api_client.dart';
import '../core/app_theme.dart';
import '../models/product.dart';
import '../providers/product_provider.dart';

class ProductsScreen extends StatefulWidget {
  const ProductsScreen({super.key});

  @override
  State<ProductsScreen> createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  final _searchController = TextEditingController();
  final _currency = NumberFormat.currency(locale: 'es_PE', symbol: 'S/ ');
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ProductProvider>().loadProducts();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  List<Product> _filtered(List<Product> products) {
    if (_searchQuery.isEmpty) return products;
    final q = _searchQuery.toLowerCase();
    return products
        .where((p) =>
            p.name.toLowerCase().contains(q) || p.sku.toLowerCase().contains(q))
        .toList();
  }

  void _showAddProduct() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => _AddProductSheet(
        onSave: (data) async {
          final ok = await context.read<ProductProvider>().createProduct(data);
          if (!mounted) return;
          if (ok) {
            showSuccess(context, 'Producto creado correctamente');
          } else {
            showError(
                context,
                context.read<ProductProvider>().error ??
                    'Error al crear el producto');
          }
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Column(
        children: [
          // Barra de búsqueda y acción
          Container(
            color: Colors.white,
            padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    decoration: InputDecoration(
                      hintText: 'Buscar producto o SKU...',
                      prefixIcon: const Icon(Icons.search_rounded, size: 20),
                      suffixIcon: _searchQuery.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.close_rounded, size: 18),
                              onPressed: () {
                                _searchController.clear();
                                setState(() => _searchQuery = '');
                              })
                          : null,
                      contentPadding: const EdgeInsets.symmetric(
                          vertical: 0, horizontal: 16),
                      filled: true,
                      fillColor: AppColors.background,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                        borderSide: const BorderSide(color: AppColors.divider),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                        borderSide: const BorderSide(color: AppColors.divider),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                        borderSide:
                            const BorderSide(color: AppColors.accent, width: 2),
                      ),
                    ),
                    onChanged: (v) => setState(() => _searchQuery = v),
                  ),
                ),
                const SizedBox(width: 10),
                ElevatedButton.icon(
                  icon: const Icon(Icons.add_rounded, size: 18),
                  label: Text('Nuevo',
                      style: GoogleFonts.inter(fontWeight: FontWeight.w600)),
                  onPressed: _showAddProduct,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.accent,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 13),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10)),
                  ),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          Expanded(child: _productList()),
        ],
      ),
    );
  }

  Widget _productList() {
    return Consumer<ProductProvider>(builder: (_, pp, __) {
      if (pp.loading) {
        return const Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              CircularProgressIndicator(color: AppColors.accent),
              SizedBox(height: 12),
              Text('Cargando productos...',
                  style: TextStyle(color: AppColors.textSecondary)),
            ],
          ),
        );
      }
      if (pp.error != null) {
        return Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 56,
                  height: 56,
                  decoration: BoxDecoration(
                    color: AppColors.danger.withValues(alpha: 0.1),
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.wifi_off_rounded,
                      color: AppColors.danger, size: 26),
                ),
                const SizedBox(height: 16),
                Text(pp.error!,
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: AppColors.textSecondary)),
                const SizedBox(height: 16),
                OutlinedButton.icon(
                  icon: const Icon(Icons.refresh_rounded, size: 16),
                  label: const Text('Reintentar'),
                  onPressed: pp.loadProducts,
                ),
              ],
            ),
          ),
        );
      }
      final products = _filtered(pp.products);
      if (products.isEmpty) {
        return Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.inventory_2_outlined,
                  size: 56, color: AppColors.textMuted.withValues(alpha: 0.4)),
              const SizedBox(height: 12),
              Text(
                _searchQuery.isEmpty
                    ? 'No hay productos registrados'
                    : 'Sin resultados para "$_searchQuery"',
                style: GoogleFonts.inter(
                  color: AppColors.textSecondary,
                  fontSize: 15,
                ),
              ),
              if (_searchQuery.isEmpty) ...[
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  icon: const Icon(Icons.add_rounded, size: 16),
                  label: const Text('Agregar producto'),
                  onPressed: _showAddProduct,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.accent,
                    foregroundColor: Colors.white,
                  ),
                ),
              ],
            ],
          ),
        );
      }
      return RefreshIndicator(
        onRefresh: pp.loadProducts,
        color: AppColors.accent,
        child: ListView.separated(
          padding: const EdgeInsets.fromLTRB(12, 12, 12, 80),
          itemCount: products.length,
          separatorBuilder: (_, __) => const SizedBox(height: 8),
          itemBuilder: (_, i) => _ProductCard(
            product: products[i],
            currency: _currency,
          ),
        ),
      );
    });
  }
}

// ── Tarjeta de producto ───────────────────────────────────────────────────────

class _ProductCard extends StatelessWidget {
  final Product product;
  final NumberFormat currency;

  const _ProductCard({required this.product, required this.currency});

  @override
  Widget build(BuildContext context) {
    final isOut = product.stockQuantity <= 0;
    final isLow = product.isLowStock && !isOut;
    final status = isOut
        ? (AppColors.danger, 'Sin stock', Icons.remove_circle_outline)
        : isLow
            ? (AppColors.warning, 'Stock bajo', Icons.warning_amber_rounded)
            : (AppColors.success, 'Disponible', Icons.check_circle_outline);

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isOut
              ? AppColors.danger.withValues(alpha: 0.2)
              : isLow
                  ? AppColors.warning.withValues(alpha: 0.2)
                  : AppColors.cardBorder,
        ),
      ),
      padding: const EdgeInsets.all(14),
      child: Row(
        children: [
          // Ícono de categoría
          Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
              color: status.$1.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Center(
              child: Text(
                product.name.isNotEmpty ? product.name[0].toUpperCase() : '?',
                style: GoogleFonts.inter(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: status.$1,
                ),
              ),
            ),
          ),
          const SizedBox(width: 12),
          // Info principal
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  product.name,
                  style: GoogleFonts.inter(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 3),
                Text(
                  'SKU: ${product.sku}',
                  style: GoogleFonts.inter(
                    fontSize: 12,
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
          // Stock badge
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                currency.format(product.price),
                style: GoogleFonts.inter(
                  fontSize: 15,
                  fontWeight: FontWeight.bold,
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: 5),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: status.$1.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(status.$3, size: 11, color: status.$1),
                    const SizedBox(width: 3),
                    Text(
                      isOut
                          ? 'Sin stock'
                          : '${product.stockQuantity.toStringAsFixed(0)} uds',
                      style: GoogleFonts.inter(
                        fontSize: 10,
                        fontWeight: FontWeight.w600,
                        color: status.$1,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

// ── Modal: nuevo producto ─────────────────────────────────────────────────────

class _AddProductSheet extends StatefulWidget {
  final Future<void> Function(Map<String, dynamic>) onSave;

  const _AddProductSheet({required this.onSave});

  @override
  State<_AddProductSheet> createState() => _AddProductSheetState();
}

class _AddProductSheetState extends State<_AddProductSheet> {
  final _formKey = GlobalKey<FormState>();
  final _nameCtrl = TextEditingController();
  final _skuCtrl = TextEditingController();
  final _priceCtrl = TextEditingController();
  final _costCtrl = TextEditingController();
  final _stockCtrl = TextEditingController(text: '0');
  final _minStockCtrl = TextEditingController(text: '5');
  bool _saving = false;

  // Categorías cargadas desde la API
  List<Map<String, dynamic>> _categories = [];
  int? _selectedCategoryId;
  bool _loadingCategories = true;

  @override
  void initState() {
    super.initState();
    _loadCategories();
  }

  Future<void> _loadCategories() async {
    try {
      final res = await ApiClient.instance.get('/categories/');
      final data = res.data;
      List<Map<String, dynamic>> cats = [];
      if (data is List) {
        cats = List<Map<String, dynamic>>.from(data);
      } else if (data is Map && data['data'] != null) {
        cats = List<Map<String, dynamic>>.from(data['data'] as List);
      }
      if (mounted)
        setState(() {
          _categories = cats;
          _loadingCategories = false;
        });
    } catch (_) {
      if (mounted) setState(() => _loadingCategories = false);
    }
  }

  @override
  void dispose() {
    _nameCtrl.dispose();
    _skuCtrl.dispose();
    _priceCtrl.dispose();
    _costCtrl.dispose();
    _stockCtrl.dispose();
    _minStockCtrl.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _saving = true);

    await widget.onSave({
      'name': _nameCtrl.text.trim(),
      'sku': _skuCtrl.text.trim(),
      'price': double.parse(_priceCtrl.text),
      'cost': double.tryParse(_costCtrl.text) ?? 0,
      'stock_quantity': double.tryParse(_stockCtrl.text) ?? 0,
      'min_stock': double.tryParse(_minStockCtrl.text) ?? 5,
      'status': 'active',
      if (_selectedCategoryId != null) 'category_id': _selectedCategoryId,
    });

    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final bottom = MediaQuery.of(context).viewInsets.bottom;
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      padding: EdgeInsets.fromLTRB(20, 0, 20, bottom + 20),
      child: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Handle bar
              Center(
                child: Container(
                  margin: const EdgeInsets.only(top: 12, bottom: 8),
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: AppColors.divider,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              // Header
              Row(children: [
                Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    color: AppColors.accent.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.add_box_outlined,
                      color: AppColors.accent, size: 20),
                ),
                const SizedBox(width: 10),
                Text('Nuevo producto',
                    style: GoogleFonts.inter(
                        fontSize: 17,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary)),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.close_rounded),
                  onPressed: () => Navigator.pop(context),
                  color: AppColors.textSecondary,
                ),
              ]),
              const SizedBox(height: 16),
              _field(_nameCtrl, 'Nombre del producto',
                  hint: 'Ej. Coca Cola 500ml', required: true),
              const SizedBox(height: 12),
              _field(_skuCtrl, 'SKU / Código',
                  hint: 'Ej. CC-500', required: true),
              const SizedBox(height: 12),
              // ── Categoría ───────────────────────────────────
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Categoría',
                    style: GoogleFonts.inter(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: AppColors.textSecondary,
                    ),
                  ),
                  const SizedBox(height: 5),
                  _loadingCategories
                      ? const SizedBox(
                          height: 48,
                          child: Center(
                              child: SizedBox(
                                  height: 18,
                                  width: 18,
                                  child: CircularProgressIndicator(
                                      strokeWidth: 2))))
                      : DropdownButtonFormField<int?>(
                          value: _selectedCategoryId,
                          decoration: const InputDecoration(
                            contentPadding: EdgeInsets.symmetric(
                                horizontal: 12, vertical: 13),
                          ),
                          hint: const Text('Sin categoría'),
                          items: [
                            const DropdownMenuItem<int?>(
                              value: null,
                              child: Text('Sin categoría'),
                            ),
                            ..._categories.map((cat) {
                              final id = cat['category_id'] as int? ??
                                  cat['id'] as int?;
                              final name =
                                  cat['name']?.toString() ?? 'Sin nombre';
                              return DropdownMenuItem<int?>(
                                value: id,
                                child: Text(name),
                              );
                            }),
                          ],
                          onChanged: (v) =>
                              setState(() => _selectedCategoryId = v),
                        ),
                ],
              ),
              const SizedBox(height: 12),
              Row(children: [
                Expanded(
                    child: _field(_priceCtrl, 'Precio de venta',
                        hint: '0.00',
                        required: true,
                        isNumber: true,
                        prefix: 'S/ ')),
                const SizedBox(width: 12),
                Expanded(
                    child: _field(_costCtrl, 'Costo (opcional)',
                        hint: '0.00', isNumber: true, prefix: 'S/ ')),
              ]),
              const SizedBox(height: 12),
              Row(children: [
                Expanded(
                    child: _field(_stockCtrl, 'Stock inicial',
                        hint: '0', isNumber: true)),
                const SizedBox(width: 12),
                Expanded(
                    child: _field(_minStockCtrl, 'Stock mínimo',
                        hint: '5', isNumber: true)),
              ]),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton.icon(
                  icon: _saving
                      ? const SizedBox(
                          height: 16,
                          width: 16,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white))
                      : const Icon(Icons.save_outlined, size: 18),
                  label: Text(_saving ? 'Guardando...' : 'Guardar producto',
                      style: GoogleFonts.inter(fontWeight: FontWeight.w600)),
                  onPressed: _saving ? null : _save,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.accent,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10)),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _field(
    TextEditingController ctrl,
    String label, {
    String? hint,
    bool required = false,
    bool isNumber = false,
    String? prefix,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          label,
          style: GoogleFonts.inter(
            fontSize: 12,
            fontWeight: FontWeight.w600,
            color: AppColors.textSecondary,
          ),
        ),
        const SizedBox(height: 5),
        TextFormField(
          controller: ctrl,
          decoration: InputDecoration(
            hintText: hint,
            prefixText: prefix,
            contentPadding:
                const EdgeInsets.symmetric(horizontal: 12, vertical: 13),
          ),
          keyboardType: isNumber
              ? const TextInputType.numberWithOptions(decimal: true)
              : TextInputType.text,
          validator: required
              ? (v) =>
                  (v == null || v.trim().isEmpty) ? 'Campo requerido' : null
              : isNumber
                  ? (v) {
                      if (v != null && v.isNotEmpty) {
                        if (double.tryParse(v) == null) {
                          return 'Número inválido';
                        }
                      }
                      return null;
                    }
                  : null,
        ),
      ],
    );
  }
}
