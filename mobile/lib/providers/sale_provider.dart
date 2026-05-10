import 'package:flutter/foundation.dart';

import '../core/api_client.dart';
import '../models/cart_item.dart';

class SaleProvider extends ChangeNotifier {
  final List<CartItem> _cart = [];
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _lastSaleResult;

  List<CartItem> get cart => _cart;
  bool get loading => _loading;
  String? get error => _error;
  Map<String, dynamic>? get lastSaleResult => _lastSaleResult;

  double get subtotal => _cart.fold(0, (sum, item) => sum + item.subtotal);
  double get tax => subtotal * 0.18;
  double get total => subtotal; // Los precios ya incluyen IGV

  int get itemCount => _cart.length;

  void addToCart(CartItem item) {
    final existing = _cart.indexWhere((e) => e.productId == item.productId);
    if (existing >= 0) {
      _cart[existing].quantity += item.quantity;
    } else {
      _cart.add(item);
    }
    notifyListeners();
  }

  void removeFromCart(int productId) {
    _cart.removeWhere((e) => e.productId == productId);
    notifyListeners();
  }

  void updateQuantity(int productId, double quantity) {
    final index = _cart.indexWhere((e) => e.productId == productId);
    if (index >= 0) {
      if (quantity <= 0) {
        _cart.removeAt(index);
      } else {
        _cart[index].quantity = quantity;
      }
      notifyListeners();
    }
  }

  void clearCart() {
    _cart.clear();
    _lastSaleResult = null;
    notifyListeners();
  }

  Future<bool> processSale({
    int? customerId,
    required String paymentMethod,
    required double paidAmount,
    bool includeTax = true,
  }) async {
    if (_cart.isEmpty) return false;

    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final changeAmount = paidAmount - total;

      final payload = {
        'cart_items': _cart.map((e) => e.toJson()).toList(),
        'customer_id': customerId,
        'payment_info': {
          'method': paymentMethod,
          'paid_amount': paidAmount,
          'change_amount': changeAmount < 0 ? 0.0 : changeAmount,
          'discount_amount': 0.0,
          'include_tax': includeTax,
        },
        'notes': '',
      };

      final response = await ApiClient.instance.post('/sales/', data: payload);
      _lastSaleResult = response.data as Map<String, dynamic>;
      _cart.clear(); // No usar clearCart() — ese resetea _lastSaleResult
      _loading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = _parseError(e);
      _loading = false;
      notifyListeners();
      return false;
    }
  }

  String _parseError(dynamic e) {
    try {
      final data = (e as dynamic).response?.data;
      if (data is Map) return data['detail']?.toString() ?? 'Error';
    } catch (_) {}
    return 'Error de conexión';
  }
}
