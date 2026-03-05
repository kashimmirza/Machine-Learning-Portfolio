// lib/presentation/providers/module_provider.dart
import 'package:flutter/foundation.dart';

class ModuleProvider with ChangeNotifier {
  String? _selectedModule;
  bool _isLoading = false;
  String? _errorMessage;

  String? get selectedModule => _selectedModule;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  void selectModule(String moduleId) {
    _selectedModule = moduleId;
    notifyListeners();
  }

  void setLoading(bool isLoading) {
    _isLoading = isLoading;
    notifyListeners();
  }

  void setError(String? error) {
    _errorMessage = error;
    notifyListeners();
  }

  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }
}
