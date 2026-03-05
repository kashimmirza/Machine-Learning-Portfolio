// lib/core/services/auth_service.dart
import '../../../data/models/user_model.dart';

class AuthService {
  Future<UserModel?> login(String email, String password) async {
    // TODO: Implement actual authentication
    return null;
  }

  Future<UserModel?> signup({
    required String name,
    required String email,
    required String password,
  }) async {
    // TODO: Implement actual registration
    return null;
  }

  Future<void> logout() async {
    // TODO: Implement actual logout
  }

  Future<UserModel?> getCurrentUser() async {
    // TODO: Check if user is logged in
    return null;
  }

  Future<bool> isLoggedIn() async {
    // TODO: Check if user is logged in
    return false;
  }
}
