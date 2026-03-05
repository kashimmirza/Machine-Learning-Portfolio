// lib/presentation/providers/listening_provider.dart
import 'package:flutter/foundation.dart';

class ListeningProvider with ChangeNotifier {
  bool _isLoading = false;
  String? _errorMessage;
  Map<int, String> _answers = {};
  bool _isPlaying = false;

  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  Map<int, String> get answers => _answers;
  bool get isPlaying => _isPlaying;

  void setLoading(bool isLoading) {
    _isLoading = isLoading;
    notifyListeners();
  }

  void setError(String? error) {
    _errorMessage = error;
    notifyListeners();
  }

  void setAnswer(int questionId, String answer) {
    _answers[questionId] = answer;
    notifyListeners();
  }

  void setPlaying(bool isPlaying) {
    _isPlaying = isPlaying;
    notifyListeners();
  }

  void clearAnswers() {
    _answers.clear();
    notifyListeners();
  }
}
