// lib/presentation/providers/writing_provider.dart
import 'package:flutter/foundation.dart';

class WritingProvider with ChangeNotifier {
  bool _isLoading = false;
  dynamic _lastAssessmentResult;
  List<dynamic> _sessions = [];
  Map<String, dynamic>? _currentFeedback;

  bool get isLoading => _isLoading;
  dynamic get lastAssessmentResult => _lastAssessmentResult;
  List<dynamic> get sessions => _sessions;
  Map<String, dynamic>? get currentFeedback => _currentFeedback;

  void setLoading(bool isLoading) {
    _isLoading = isLoading;
    notifyListeners();
  }

  void setFeedback(Map<String, dynamic>? feedback) {
    _currentFeedback = feedback;
    notifyListeners();
  }

  void clearError() {
    notifyListeners();
  }
}
