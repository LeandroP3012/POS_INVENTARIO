import 'package:flutter/foundation.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dart:convert';

import '../core/api_client.dart';
import '../core/constants.dart';
import '../models/user.dart';

class AuthProvider extends ChangeNotifier {
  User? _currentUser;
  bool _loading = false;
  String? _error;

  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  User? get currentUser => _currentUser;
  bool get loading => _loading;
  String? get error => _error;
  bool get isLoggedIn => _currentUser != null;

  /// Intenta recargar sesión desde almacenamiento seguro
  Future<bool> tryAutoLogin() async {
    final token = await _storage.read(key: kTokenKey);
    final userData = await _storage.read(key: kUserKey);
    if (token == null || userData == null) return false;

    try {
      final json = jsonDecode(userData) as Map<String, dynamic>;
      json['access_token'] = token;
      _currentUser = User.fromJson(json);
      notifyListeners();
      return true;
    } catch (_) {
      return false;
    }
  }

  Future<bool> login(String username, String password) async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiClient.instance.post(
        '/auth/login',
        data: {'username': username, 'password': password},
      );

      final user = User.fromJson(response.data as Map<String, dynamic>);
      _currentUser = user;

      // Guardar token y datos de usuario de forma segura
      await _storage.write(key: kTokenKey, value: user.accessToken);
      await _storage.write(
        key: kUserKey,
        value: jsonEncode({
          'user_id': user.id,
          'username': user.username,
          'full_name': user.fullName,
          'user_type': user.userType,
          'role_id': user.roleId,
        }),
      );

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

  Future<void> logout() async {
    await _storage.deleteAll();
    _currentUser = null;
    notifyListeners();
  }

  String _parseError(dynamic e) {
    try {
      final data = (e as dynamic).response?.data;
      if (data is Map) return data['detail']?.toString() ?? 'Error desconocido';
    } catch (_) {}
    return 'Error de conexión';
  }
}
