import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../core/app_theme.dart';
import '../models/cart_item.dart';
import '../models/product.dart';
import '../providers/printer_provider.dart';
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
            p.name.toLowerCase().contains(q) || p.sku.toLowerCase().contains(q))
        .toList();
  }

  void _addToCart(Product product) {
    context.read<SaleProvider>().addToCart(CartItem(
          productId: product.id,
          productName: product.name,
          quantity: 1,
          unitPrice: product.price,
        ));
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${product.name} agregado al carrito'),
        duration: const Duration(seconds: 1),
        backgroundColor: AppColors.success,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
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
      showSuccess(context, '¡Venta registrada correctamente!');
      // Imprimir ticket automáticamente
      final printer = context.read<PrinterProvider>().defaultPrinter;
      final saleData = sale.lastSaleResult;
      if (printer != null && saleData != null) {
        // Los datos reales están en saleData['sale'] (anidado en la respuesta API)
        final ticketData = Map<String, dynamic>.from(
            (saleData['sale'] as Map<String, dynamic>?) ?? saleData);
        // Inyectar datos de pago del diálogo (no vienen en la respuesta de la BD)
        final paid = result['paid'] as double;
        final total = ticketData['total_amount'] != null
            ? double.tryParse(ticketData['total_amount'].toString()) ?? paid
            : paid;
        ticketData['payment_info'] = {
          'method': result['method'],
          'paid_amount': paid,
          'change_amount': paid - total > 0 ? paid - total : 0.0,
          'include_tax': result['include_tax'] ?? true,
        };
        final printed = await context.read<PrinterProvider>().printTicket(
              printer: printer,
              saleData: ticketData,
            );
        if (!printed && mounted) {
          final err = context.read<PrinterProvider>().lastPrintError ??
              'Error desconocido';
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('Venta OK pero error al imprimir: $err'),
            backgroundColor: Colors.orange,
            duration: const Duration(seconds: 6),
            behavior: SnackBarBehavior.floating,
          ));
        }
      } else if (printer == null && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text('Venta OK. Sin impresora configurada.'),
          duration: Duration(seconds: 3),
          behavior: SnackBarBehavior.floating,
        ));
      }
    } else {
      showError(context, sale.error ?? 'Error al procesar la venta');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: LayoutBuilder(builder: (context, constraints) {
        final isWide = constraints.maxWidth > 680;
        return isWide
            ? Row(children: [
                Expanded(flex: 3, child: _productPanel()),
                Container(
                  width: 1,
                  color: AppColors.divider,
                ),
                SizedBox(width: 320, child: _cartPanel()),
              ])
            : Column(children: [
                Expanded(child: _productPanel()),
                Container(height: 1, color: AppColors.divider),
                SizedBox(height: 280, child: _cartPanel()),
              ]);
      }),
    );
  }

  // â”€â”€ Panel de productos â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

  Widget _productPanel() {
    return Column(
      children: [
        // Header bÃºsqueda
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
                      vertical: 0,
                      horizontal: 16,
                    ),
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
            ],
          ),
        ),
        const Divider(height: 1),
        // Grid de productos
        Expanded(child: _productGrid()),
      ],
    );
  }

  Widget _productGrid() {
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
        return _ErrorState(
          message: pp.error!,
          onRetry: pp.loadProducts,
        );
      }
      final products =
          _filtered(pp.products.where((p) => p.status == 'active').toList());
      if (products.isEmpty) {
        return Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.search_off_rounded,
                  size: 56, color: AppColors.textMuted.withValues(alpha: 0.4)),
              const SizedBox(height: 12),
              Text(
                _searchQuery.isEmpty ? 'No hay productos' : 'Sin resultados',
                style: GoogleFonts.inter(
                  color: AppColors.textSecondary,
                  fontSize: 15,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        );
      }
      return GridView.builder(
        padding: const EdgeInsets.all(12),
        gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
          maxCrossAxisExtent: 170,
          mainAxisExtent: 130,
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
        ),
        itemCount: products.length,
        itemBuilder: (_, i) => _PosProductCard(
          product: products[i],
          currency: _currency,
          onTap: () => _addToCart(products[i]),
        ),
      );
    });
  }

  // â”€â”€ Panel del carrito â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

  Widget _cartPanel() {
    return Consumer<SaleProvider>(builder: (_, sale, __) {
      return Container(
        color: Colors.white,
        child: Column(
          children: [
            // Header carrito
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: const BoxDecoration(
                color: Colors.white,
                border: Border(bottom: BorderSide(color: AppColors.divider)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.shopping_cart_rounded,
                      size: 18, color: AppColors.primary),
                  const SizedBox(width: 8),
                  Text(
                    'Carrito',
                    style: GoogleFonts.inter(
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(width: 6),
                  if (sale.itemCount > 0)
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 7, vertical: 2),
                      decoration: BoxDecoration(
                        color: AppColors.accent,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Text(
                        '${sale.itemCount}',
                        style: GoogleFonts.inter(
                          color: Colors.white,
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  const Spacer(),
                  if (sale.cart.isNotEmpty)
                    TextButton.icon(
                      icon: const Icon(Icons.delete_outline, size: 15),
                      label: const Text('Limpiar'),
                      onPressed: sale.clearCart,
                      style: TextButton.styleFrom(
                        foregroundColor: AppColors.danger,
                        padding: EdgeInsets.zero,
                        minimumSize: const Size(0, 0),
                        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                        textStyle: GoogleFonts.inter(
                            fontSize: 12, fontWeight: FontWeight.w500),
                      ),
                    ),
                ],
              ),
            ),

            // Ãtems
            Expanded(
              child: sale.cart.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.shopping_cart_outlined,
                            size: 44,
                            color: AppColors.textMuted.withValues(alpha: 0.4),
                          ),
                          const SizedBox(height: 10),
                          Text(
                            'Agrega productos\npara comenzar',
                            textAlign: TextAlign.center,
                            style: GoogleFonts.inter(
                              color: AppColors.textSecondary,
                              fontSize: 13,
                            ),
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      itemCount: sale.cart.length,
                      itemBuilder: (_, i) {
                        final item = sale.cart[i];
                        return _CartItemTile(
                          item: item,
                          currency: _currency,
                          onRemove: () => sale.removeFromCart(item.productId),
                          onQtyChange: (q) =>
                              sale.updateQuantity(item.productId, q),
                        );
                      },
                    ),
            ),

            // Footer total + cobrar
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppColors.primary,
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(0),
                  bottomRight: Radius.circular(0),
                ),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.primary.withValues(alpha: 0.3),
                    blurRadius: 8,
                    offset: const Offset(0, -2),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        'TOTAL A COBRAR',
                        style: GoogleFonts.inter(
                          color: Colors.white54,
                          fontSize: 10,
                          fontWeight: FontWeight.w600,
                          letterSpacing: 0.8,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        _currency.format(sale.total),
                        style: GoogleFonts.inter(
                          color: Colors.white,
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
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
                        : const Icon(Icons.payments_outlined, size: 18),
                    label: Text(
                      'Cobrar',
                      style: GoogleFonts.inter(
                          fontWeight: FontWeight.w600, fontSize: 14),
                    ),
                    onPressed:
                        sale.loading || sale.cart.isEmpty ? null : _checkout,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.success,
                      foregroundColor: Colors.white,
                      disabledBackgroundColor:
                          Colors.white.withValues(alpha: 0.15),
                      disabledForegroundColor:
                          Colors.white.withValues(alpha: 0.4),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 20, vertical: 13),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      );
    });
  }
}

// â”€â”€ Tarjeta de producto para el POS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class _PosProductCard extends StatelessWidget {
  final Product product;
  final NumberFormat currency;
  final VoidCallback onTap;

  const _PosProductCard({
    required this.product,
    required this.currency,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final outOfStock = product.stockQuantity <= 0;
    final isLow = product.isLowStock && !outOfStock;

    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(12),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: outOfStock ? null : onTap,
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: outOfStock
                  ? AppColors.danger.withValues(alpha: 0.25)
                  : isLow
                      ? AppColors.warning.withValues(alpha: 0.35)
                      : AppColors.cardBorder,
            ),
          ),
          padding: const EdgeInsets.all(10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Ãcono + badge stock
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 32,
                    height: 32,
                    decoration: BoxDecoration(
                      color: outOfStock
                          ? AppColors.danger.withValues(alpha: 0.1)
                          : AppColors.accent.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(
                      Icons.inventory_2_rounded,
                      size: 16,
                      color: outOfStock ? AppColors.danger : AppColors.accent,
                    ),
                  ),
                  const Spacer(),
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 5, vertical: 2),
                    decoration: BoxDecoration(
                      color: outOfStock
                          ? AppColors.danger.withValues(alpha: 0.1)
                          : isLow
                              ? AppColors.warning.withValues(alpha: 0.1)
                              : AppColors.success.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      outOfStock
                          ? 'Agotado'
                          : product.stockQuantity.toStringAsFixed(0),
                      style: GoogleFonts.inter(
                        fontSize: 9,
                        fontWeight: FontWeight.bold,
                        color: outOfStock
                            ? AppColors.danger
                            : isLow
                                ? AppColors.warning
                                : AppColors.success,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              // Nombre
              Text(
                product.name,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: GoogleFonts.inter(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color:
                      outOfStock ? AppColors.textMuted : AppColors.textPrimary,
                  height: 1.2,
                ),
              ),
              const Spacer(),
              // Precio
              Text(
                currency.format(product.price),
                style: GoogleFonts.inter(
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                  color: outOfStock ? AppColors.textMuted : AppColors.accent,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// â”€â”€ Ãtem del carrito â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class _CartItemTile extends StatelessWidget {
  final CartItem item;
  final NumberFormat currency;
  final VoidCallback onRemove;
  final void Function(double) onQtyChange;

  const _CartItemTile({
    required this.item,
    required this.currency,
    required this.onRemove,
    required this.onQtyChange,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: AppColors.divider)),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      child: Row(
        children: [
          // remove
          IconButton(
            icon: const Icon(Icons.remove_circle_outline_rounded,
                color: AppColors.danger, size: 18),
            onPressed: onRemove,
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 24, minHeight: 24),
          ),
          const SizedBox(width: 6),
          // Nombre + subtotal
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item.productName,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: GoogleFonts.inter(
                    fontSize: 13,
                    fontWeight: FontWeight.w500,
                    color: AppColors.textPrimary,
                  ),
                ),
                Text(
                  currency.format(item.unitPrice),
                  style: GoogleFonts.inter(
                    fontSize: 11,
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
          // Cantidad +/-
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              _QtyButton(
                icon: Icons.remove_rounded,
                onTap: () => onQtyChange(item.quantity - 1),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8),
                child: Text(
                  item.quantity.toStringAsFixed(0),
                  style: GoogleFonts.inter(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textPrimary,
                  ),
                ),
              ),
              _QtyButton(
                icon: Icons.add_rounded,
                onTap: () => onQtyChange(item.quantity + 1),
              ),
            ],
          ),
          const SizedBox(width: 8),
          // Subtotal
          SizedBox(
            width: 68,
            child: Text(
              currency.format(item.subtotal),
              textAlign: TextAlign.right,
              style: GoogleFonts.inter(
                fontSize: 12,
                fontWeight: FontWeight.bold,
                color: AppColors.textPrimary,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _QtyButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;

  const _QtyButton({required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(6),
      child: Container(
        width: 26,
        height: 26,
        decoration: BoxDecoration(
          border: Border.all(color: AppColors.divider),
          borderRadius: BorderRadius.circular(6),
          color: AppColors.background,
        ),
        child: Icon(icon, size: 14, color: AppColors.textPrimary),
      ),
    );
  }
}

// â”€â”€ DiÃ¡logo de cobro â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class _PaymentDialog extends StatefulWidget {
  final double total;
  final NumberFormat currency;

  const _PaymentDialog({required this.total, required this.currency});

  @override
  State<_PaymentDialog> createState() => _PaymentDialogState();
}

class _PaymentDialogState extends State<_PaymentDialog> {
  final _paidCtrl = TextEditingController();
  String _method = 'cash';
  double _paid = 0;
  bool _hasError = false;

  @override
  void initState() {
    super.initState();
    _paidCtrl.text = widget.total.toStringAsFixed(2);
    _paid = widget.total;
    _paidCtrl.addListener(() {
      final v = double.tryParse(_paidCtrl.text) ?? 0;
      setState(() {
        _paid = v;
        _hasError = v < widget.total;
      });
    });
  }

  @override
  void dispose() {
    _paidCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final change = _paid - widget.total;

    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 380,
        padding: const EdgeInsets.all(0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: AppColors.primary,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(16),
                  topRight: Radius.circular(16),
                ),
              ),
              child: Row(
                children: [
                  const Icon(Icons.payments_outlined,
                      color: Colors.white, size: 22),
                  const SizedBox(width: 10),
                  Text(
                    'Cobro de venta',
                    style: GoogleFonts.inter(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                  ),
                  const Spacer(),
                  IconButton(
                    icon: const Icon(Icons.close,
                        color: Colors.white54, size: 20),
                    onPressed: () => Navigator.pop(context),
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                  ),
                ],
              ),
            ),

            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Total a cobrar
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: AppColors.primary.withValues(alpha: 0.05),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(
                          color: AppColors.primary.withValues(alpha: 0.1)),
                    ),
                    child: Column(
                      children: [
                        Text(
                          'Total a cobrar',
                          style: GoogleFonts.inter(
                            color: AppColors.textSecondary,
                            fontSize: 12,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          widget.currency.format(widget.total),
                          style: GoogleFonts.inter(
                            color: AppColors.primary,
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),

                  // MÃ©todo de pago
                  Text(
                    'MÃ©todo de pago',
                    style: GoogleFonts.inter(
                      fontWeight: FontWeight.w600,
                      fontSize: 13,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      _PayMethodChip(
                        icon: Icons.payments_outlined,
                        label: 'Efectivo',
                        value: 'cash',
                        selected: _method == 'cash',
                        onTap: () => setState(() => _method = 'cash'),
                      ),
                      const SizedBox(width: 8),
                      _PayMethodChip(
                        icon: Icons.credit_card_outlined,
                        label: 'Tarjeta',
                        value: 'card',
                        selected: _method == 'card',
                        onTap: () => setState(() => _method = 'card'),
                      ),
                      const SizedBox(width: 8),
                      _PayMethodChip(
                        icon: Icons.account_balance_outlined,
                        label: 'Transfer.',
                        value: 'transfer',
                        selected: _method == 'transfer',
                        onTap: () => setState(() => _method = 'transfer'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Monto recibido (solo efectivo)
                  if (_method == 'cash') ...[
                    Text(
                      'Monto recibido',
                      style: GoogleFonts.inter(
                        fontWeight: FontWeight.w600,
                        fontSize: 13,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 8),
                    TextField(
                      controller: _paidCtrl,
                      keyboardType:
                          const TextInputType.numberWithOptions(decimal: true),
                      decoration: InputDecoration(
                        prefixText: 'S/ ',
                        errorText: _hasError ? 'Monto insuficiente' : null,
                      ),
                    ),
                    const SizedBox(height: 12),
                    // Vuelto
                    AnimatedContainer(
                      duration: const Duration(milliseconds: 200),
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: change >= 0
                            ? AppColors.success.withValues(alpha: 0.08)
                            : AppColors.danger.withValues(alpha: 0.08),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: change >= 0
                              ? AppColors.success.withValues(alpha: 0.2)
                              : AppColors.danger.withValues(alpha: 0.2),
                        ),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Vuelto:',
                            style: GoogleFonts.inter(
                              fontWeight: FontWeight.w500,
                              color: change >= 0
                                  ? AppColors.success
                                  : AppColors.danger,
                            ),
                          ),
                          Text(
                            widget.currency.format(change >= 0 ? change : 0),
                            style: GoogleFonts.inter(
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                              color: change >= 0
                                  ? AppColors.success
                                  : AppColors.danger,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                  ] else
                    const SizedBox(height: 8),

                  // BotÃ³n confirmar
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: ElevatedButton.icon(
                      icon: const Icon(Icons.check_circle_outline, size: 18),
                      label: const Text('Confirmar pago'),
                      onPressed: (_method == 'cash' && _hasError)
                          ? null
                          : () => Navigator.pop(context, {
                                'method': _method,
                                'paid':
                                    _method == 'cash' ? _paid : widget.total,
                              }),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.success,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _PayMethodChip extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final bool selected;
  final VoidCallback onTap;

  const _PayMethodChip({
    required this.icon,
    required this.label,
    required this.value,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            color: selected
                ? AppColors.accent.withValues(alpha: 0.12)
                : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: selected ? AppColors.accent : AppColors.divider,
              width: selected ? 1.5 : 1,
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                color: selected ? AppColors.accent : AppColors.textSecondary,
                size: 20,
              ),
              const SizedBox(height: 4),
              Text(
                label,
                style: GoogleFonts.inter(
                  fontSize: 11,
                  fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
                  color: selected ? AppColors.accent : AppColors.textSecondary,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// â”€â”€ Estado de error reutilizable â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class _ErrorState extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;

  const _ErrorState({required this.message, required this.onRetry});

  @override
  Widget build(BuildContext context) {
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
            Text(
              'Error al cargar datos',
              style: GoogleFonts.inter(
                fontWeight: FontWeight.bold,
                color: AppColors.textPrimary,
                fontSize: 15,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              message,
              textAlign: TextAlign.center,
              maxLines: 3,
              overflow: TextOverflow.ellipsis,
              style: GoogleFonts.inter(
                color: AppColors.textSecondary,
                fontSize: 12,
              ),
            ),
            const SizedBox(height: 20),
            OutlinedButton.icon(
              icon: const Icon(Icons.refresh_rounded, size: 16),
              label: const Text('Reintentar'),
              onPressed: onRetry,
            ),
          ],
        ),
      ),
    );
  }
}
