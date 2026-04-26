class Product {
  final int id;
  final String sku;
  final String name;
  final String? description;
  final int? categoryId;
  final double price;
  final double cost;
  final double stockQuantity;
  final double minStock;
  final String status;

  Product({
    required this.id,
    required this.sku,
    required this.name,
    this.description,
    this.categoryId,
    required this.price,
    required this.cost,
    required this.stockQuantity,
    required this.minStock,
    required this.status,
  });

  factory Product.fromJson(Map<String, dynamic> json) => Product(
        id: json['id'],
        sku: json['sku'] ?? '',
        name: json['name'],
        description: json['description'],
        categoryId: json['category_id'],
        price: (json['price'] as num).toDouble(),
        cost: (json['cost'] as num?)?.toDouble() ?? 0,
        stockQuantity: (json['stock_quantity'] ?? json['quantity'] as num?)?.toDouble() ?? 0,
        minStock: (json['min_stock'] as num?)?.toDouble() ?? 0,
        status: json['status'] ?? 'active',
      );

  bool get isLowStock => stockQuantity <= minStock;
}
