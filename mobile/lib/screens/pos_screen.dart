import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../models/cart_item.dart';
import '../models/product.dart';
import '../providers/product_provider.dart';
import '../providers/sale_provider.dart';

class PosScreen extends StatefulWidget {
  const PosScreen({super.key});

  @override
  State<PosScreen> createState() => _PosScreenState();
}

class _PosScreenState extends State<PosScreen> {
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

  void _addToCart(Product product) {
    context.read<SaleProvider>().addToCart(CartItem(
          productId: product.id,
          productName: product.name,
          quantity: 1,
          unitPrice: product.price,
        ));
  }

  Future<void> _checkout() async {
    final sale = context.read<SaleProvider>();
    if (sale.cart.isEmpty) return;

    final result = await showDialog<Map<String, dynamic>>(
      context: context,
      builder: (_) => _PaymentDialog(total: sale.total, currency: _currency),
    );

    if (result == null || !mounted) return;

    final ok = await sale.processSale(
      paymentMethod: result['method'] as String,
      paidAmount: result['paid'] as double,
    );

    if (!mounted) return;

    if (ok) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('¡Venta registrada correctamente!'),
          backgroundColor: Colors.green,
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(sale.error ?? 'Error al procesar la venta'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (context, constraints) {
      final isWide = constraints.maxWidth > 700;
      return isWide
          ? Row(children: [
              Expanded(flex: 3, child: _productPanel()),
              const VerticalDivider(width: 1),
              SizedBox(width: 320, child: _cartPanel()),
            ])
          : Column(children: [
              Expanded(child: _productPanel()),
              const Divider(height: 1),
              SizedBox(height: 260, child: _cartPanel()),
            ]);
    });
  }

  Widget _productPanel() {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(12),
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
        Expanded(child: _productGrid()),
      ],
    );
  }

  Widget _productGrid() {
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
      final products = _filtered(
          pp.products.where((p) => p.status == 'active').toList());
      if (products.isEmpty) {
        return const Center(child: Text('Sin productos'));
      }
      return GridView.builder(
        padding: const EdgeInsets.fromLTRB(12, 0, 12, 12),
        gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
          maxCrossAxisExtent: 180,
          mainAxisExtent: 110,
          crossAxisSpacing: 8,
          mainAxisSpacing: 8,
        ),
        itemCount: products.length,
        itemBuilder: (_, i) => _ProductCard(
          product: products[i],
          currency: _currency,
          onTap: () => _addToCart(products[i]),
        ),
      );
    });
  }

  Widget _cartPanel() {
    return Consumer<SaleProvider>(builder: (_, sale, __) {
      return Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(
              children: [
                const Icon(Icons.shopping_cart, size: 18),
                const SizedBox(width: 6),
                Text('Carrito (${sale.itemCount})',
                    style: const TextStyle(fontWeight: FontWeight.bold)),
                const Spacer(),
                if (sale.cart.isNotEmpty)
                  TextButton.icon(
                    icon: const Icon(Icons.delete_outline, size: 16),
                    label: const Text('Limpiar'),
                    onPressed: sale.clearCart,
                    style: TextButton.styleFrom(
                        foregroundColor: Colors.red,
                        padding: EdgeInsets.zero,
                        minimumSize: const Size(0, 0)),
                  ),
              ],
            ),
          ),
          Expanded(
            child: sale.cart.isEmpty
                ? const Center(
                    child: Text('Agrega productos\npara comenzar',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: Colors.grey)))
                : ListView.builder(
                    itemCount: sale.cart.length,
                    itemBuilder: (_, i) => _CartTile(
                      item: sale.cart[i],
                      currency: _currency,
                      onRemove: () =>
                          sale.removeFromCart(sale.cart[i].productId),
                      onQtyChange: (q) =>
                          sale.updateQuantity(sale.cart[i].productId, q),
                    ),
                  ),
          ),
          Container(
            color: const Color(0xFF2c3e50),
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text('TOTAL',
                        style:
                            TextStyle(color: Colors.white70, fontSize: 11)),
                    Text(_currency.format(sale.total),
                        style: const TextStyle(
                            color: Colors.white,
                            fontSize: 20,
                            fontWeight: FontWeight.bold)),
                  ],
                ),
                const Spacer(),
                ElevatedButton.icon(
                  icon: sale.loading
                      ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white))
                      : const Icon(Icons.payment),
                  label: const Text('Cobrar'),
                  onPressed: sale.loading ? null : _checkout,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF27ae60),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 20, vertical: 12),
                  ),
                ),
              ],
            ),
          ),
        ],
      );
    });
  }
}

// ── Tarjeta de producto ────────────────────────────────────────────────────────

class _ProductCard extends StatelessWidget {
  final Product product;
  final NumberFormat currency;
  final VoidCallback onTap;

  const _ProductCard(
      {required this.product, required this.currency, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final outOfStock = product.stockQuantity <= 0;
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: InkWell(
        borderRadius: BorderRadius.circular(10),
        onTap: outOfStock ? null : onTap,
        child: Padding(
          padding: const EdgeInsets.all(10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(product.name,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: outOfStock ? Colors.grey : null)),
              const Spacer(),
              Text(currency.format(product.price),
                  style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF2c3e50))),
              Text(
                outOfStock
                    ? 'Sin stock'
                    : 'Stock: ${product.stockQuantity.toStringAsFixed(0)}',
                style: TextStyle(
                    fontSize: 10,
                    color: outOfStock ? Colors.red : Colors.grey[600]),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// ── Ítem del carrito ──────────────────────────────────────────────────────────

class _CartTile extends StatelessWidget {
  final CartItem item;
  final NumberFormat currency;
  final VoidCallback onRemove;
  final ValueChanged<double> onQtyChange;

  const _CartTile(
      {required this.item,
      required this.currency,
      required this.onRemove,
      required this.onQtyChange});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      dense: true,
      title: Text(item.productName,
          style: const TextStyle(fontSize: 13),
          maxLines: 1,
          overflow: TextOverflow.ellipsis),
      subtitle: Text(currency.format(item.unitPrice),
          style: const TextStyle(fontSize: 11)),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          IconButton(
            icon: const Icon(Icons.remove_circle_outline, size: 18),
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(),
            onPressed: () => onQtyChange(item.quantity - 1),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: Text(item.quantity.toStringAsFixed(0),
                style: const TextStyle(fontSize: 13)),
          ),
          IconButton(
            icon: const Icon(Icons.add_circle_outline, size: 18),
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(),
            onPressed: () => onQtyChange(item.quantity + 1),
          ),
          const SizedBox(width: 4),
          Text(currency.format(item.subtotal),
              style: const TextStyle(
                  fontSize: 12, fontWeight: FontWeight.bold)),
          IconButton(
            icon: const Icon(Icons.close, size: 16, color: Colors.red),
            padding: const EdgeInsets.only(left: 4),
            constraints: const BoxConstraints(),
            onPressed: onRemove,
          ),
        ],
      ),
    );
  }
}

// ── Diálogo de pago ───────────────────────────────────────────────────────────

class _PaymentDialog extends StatefulWidget {
  final double total;
  final NumberFormat currency;

  const _PaymentDialog({required this.total, required this.currency});

  @override
  State<_PaymentDialog> createState() => _PaymentDialogState();
}

class _PaymentDialogState extends State<_PaymentDialog> {
  String _method = 'cash';
  final _paidController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();
    _paidController.text = widget.total.toStringAsFixed(2);
  }

  @override
  void dispose() {
    _paidController.dispose();
    super.dispose();
  }

  double get _paid => double.tryParse(_paidController.text) ?? 0;
  double get _change => _paid - widget.total;

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Registrar pago'),
      content: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Total: ${widget.currency.format(widget.total)}',
                style: const TextStyle(
                    fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              initialValue: _method,
              decoration: const InputDecoration(
                labelText: 'Método de pago',
                border: OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(value: 'cash', child: Text('Efectivo')),
                DropdownMenuItem(value: 'card', child: Text('Tarjeta')),
                DropdownMenuItem(
                    value: 'transfer', child: Text('Transferencia')),
              ],
              onChanged: (v) => setState(() => _method = v!),
            ),
            const SizedBox(height: 12),
            if (_method == 'cash') ...[
              TextFormField(
                controller: _paidController,
                decoration: const InputDecoration(
                  labelText: 'Monto recibido',
                  prefixText: 'S/ ',
                  border: OutlineInputBorder(),
                ),
                keyboardType:
                    const TextInputType.numberWithOptions(decimal: true),
                onChanged: (_) => setState(() {}),
                validator: (v) {
                  final n = double.tryParse(v ?? '');
                  if (n == null) return 'Ingresa un monto válido';
                  if (n < widget.total) return 'Monto insuficiente';
                  return null;
                },
              ),
              const SizedBox(height: 8),
              if (_paid >= widget.total)
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.green.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.green.shade200),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.change_history, color: Colors.green),
                      const SizedBox(width: 8),
                      Text('Vuelto: ${widget.currency.format(_change)}',
                          style: const TextStyle(color: Colors.green)),
                    ],
                  ),
                ),
            ],
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancelar'),
        ),
        ElevatedButton(
          onPressed: () {
            if (_formKey.currentState!.validate()) {
              Navigator.pop(context, {
                'method': _method,
                'paid': _method == 'cash' ? _paid : widget.total,
              });
            }
          },
          style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF27ae60),
              foregroundColor: Colors.white),
          child: const Text('Confirmar'),
        ),
      ],
    );
  }
}
