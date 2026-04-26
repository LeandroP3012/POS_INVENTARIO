import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

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
            p.name.toLowerCase().contains(q) ||
            p.sku.toLowerCase().contains(q))
        .toList();
  }

  void _showAddProduct() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(16))),
      builder: (_) => _AddProductSheet(
        onSave: (data) async {
          final ok = await context.read<ProductProvider>().createProduct(data);
          if (!mounted) return;
          if (ok) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Producto creado correctamente'),
                backgroundColor: Colors.green,
              ),
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(context.read<ProductProvider>().error ??
                    'Error al crear el producto'),
                backgroundColor: Colors.red,
              ),
            );
          }
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    decoration: InputDecoration(
                      hintText: 'Buscar producto o SKU...',
                      prefixIcon: const Icon(Icons.search),
                      border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(10)),
                      contentPadding:
                          const EdgeInsets.symmetric(vertical: 0, horizontal: 12),
                      suffixIcon: _searchQuery.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.clear),
                              onPressed: () {
                                _searchController.clear();
                                setState(() => _searchQuery = '');
                              })
                          : null,
                    ),
                    onChanged: (v) => setState(() => _searchQuery = v),
                  ),
                ),
                const SizedBox(width: 8),
                FilledButton.icon(
                  icon: const Icon(Icons.add),
                  label: const Text('Nuevo'),
                  onPressed: _showAddProduct,
                ),
              ],
            ),
          ),
          Expanded(child: _productList()),
        ],
      ),
    );
  }

  Widget _productList() {
    return Consumer<ProductProvider>(builder: (_, pp, __) {
      if (pp.loading) {
        return const Center(child: CircularProgressIndicator());
      }
      if (pp.error != null) {
        return Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(pp.error!, style: const TextStyle(color: Colors.red)),
              const SizedBox(height: 8),
              ElevatedButton(
                  onPressed: pp.loadProducts, child: const Text('Reintentar')),
            ],
          ),
        );
      }
      final products = _filtered(pp.products);
      if (products.isEmpty) {
        return const Center(child: Text('No hay productos registrados'));
      }
      return RefreshIndicator(
        onRefresh: pp.loadProducts,
        child: ListView.separated(
          padding: const EdgeInsets.fromLTRB(12, 0, 12, 80),
          itemCount: products.length,
          separatorBuilder: (_, __) => const Divider(height: 1),
          itemBuilder: (_, i) => _ProductTile(
            product: products[i],
            currency: _currency,
          ),
        ),
      );
    });
  }
}

// ── Tile de producto ──────────────────────────────────────────────────────────

class _ProductTile extends StatelessWidget {
  final Product product;
  final NumberFormat currency;

  const _ProductTile({required this.product, required this.currency});

  @override
  Widget build(BuildContext context) {
    final isLow = product.isLowStock && product.stockQuantity > 0;
    final isOut = product.stockQuantity <= 0;

    return ListTile(
      contentPadding: const EdgeInsets.symmetric(horizontal: 4, vertical: 4),
      leading: CircleAvatar(
        backgroundColor: isOut
            ? Colors.red.shade100
            : isLow
                ? Colors.orange.shade100
                : Colors.green.shade100,
        child: Icon(
          Icons.inventory_2_outlined,
          color: isOut
              ? Colors.red
              : isLow
                  ? Colors.orange
                  : Colors.green,
          size: 20,
        ),
      ),
      title: Text(product.name,
          style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
      subtitle: Text('SKU: ${product.sku}  •  Stock: ${product.stockQuantity.toStringAsFixed(0)}',
          style: const TextStyle(fontSize: 12)),
      trailing: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(currency.format(product.price),
              style: const TextStyle(
                  fontWeight: FontWeight.bold, fontSize: 14)),
          if (isOut)
            const Text('Sin stock',
                style: TextStyle(color: Colors.red, fontSize: 10))
          else if (isLow)
            const Text('Stock bajo',
                style: TextStyle(color: Colors.orange, fontSize: 10))
          else
            Text(product.status,
                style:
                    const TextStyle(color: Colors.green, fontSize: 10)),
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
    });

    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final bottom = MediaQuery.of(context).viewInsets.bottom;
    return Padding(
      padding: EdgeInsets.fromLTRB(16, 16, 16, bottom + 16),
      child: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Text('Nuevo producto',
                      style:
                          TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const Spacer(),
                  IconButton(
                      icon: const Icon(Icons.close),
                      onPressed: () => Navigator.pop(context)),
                ],
              ),
              const SizedBox(height: 12),
              _field(_nameCtrl, 'Nombre del producto', required: true),
              const SizedBox(height: 10),
              _field(_skuCtrl, 'SKU / Código', required: true),
              const SizedBox(height: 10),
              Row(children: [
                Expanded(
                    child: _field(_priceCtrl, 'Precio de venta',
                        required: true, isNumber: true, prefix: 'S/ ')),
                const SizedBox(width: 10),
                Expanded(
                    child: _field(_costCtrl, 'Costo',
                        isNumber: true, prefix: 'S/ ')),
              ]),
              const SizedBox(height: 10),
              Row(children: [
                Expanded(
                    child: _field(_stockCtrl, 'Stock inicial',
                        isNumber: true)),
                const SizedBox(width: 10),
                Expanded(
                    child: _field(_minStockCtrl, 'Stock mínimo',
                        isNumber: true)),
              ]),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: FilledButton(
                  onPressed: _saving ? null : _save,
                  child: _saving
                      ? const SizedBox(
                          height: 18,
                          width: 18,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white))
                      : const Text('Guardar producto'),
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
    bool required = false,
    bool isNumber = false,
    String? prefix,
  }) {
    return TextFormField(
      controller: ctrl,
      decoration: InputDecoration(
        labelText: label,
        prefixText: prefix,
        border: const OutlineInputBorder(),
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
      ),
      keyboardType: isNumber
          ? const TextInputType.numberWithOptions(decimal: true)
          : TextInputType.text,
      validator: required
          ? (v) => (v == null || v.trim().isEmpty) ? 'Campo requerido' : null
          : isNumber
              ? (v) {
                  if (v != null && v.isNotEmpty) {
                    if (double.tryParse(v) == null) return 'Número inválido';
                  }
                  return null;
                }
              : null,
    );
  }
}
