import 'package:flutter/foundation.dart';

import '../core/api_client.dart';
import '../models/product.dart';

class ProductProvider extends ChangeNotifier {
  List<Product> _products = [];
  bool _loading = false;
  String? _error;

  List<Product> get products => _products;
  bool get loading => _loading;
  String? get error => _error;

  List<Product> get lowStockProducts =>
      _products.where((p) => p.isLowStock).toList();

  Future<void> loadProducts() async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiClient.instance.get('/products/');
      final data = response.data;

      if (data is List) {
        _products = data
            .map((e) => Product.fromJson(e as Map<String, dynamic>))
            .toList();
      } else if (data is Map && data['products'] != null) {
        _products = (data['products'] as List)
            .map((e) => Product.fromJson(e as Map<String, dynamic>))
            .toList();
      }

      _loading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _loading = false;
      notifyListeners();
    }
  }

  Future<bool> createProduct(Map<String, dynamic> productData) async {
    try {
      await ApiClient.instance.post('/products/', data: productData);
      await loadProducts();
      return true;
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }
}
