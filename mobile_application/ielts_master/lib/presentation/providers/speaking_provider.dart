// lib/presentation/providers/speaking_provider.dart
import 'package:flutter/foundation.dart';
import '../../data/models/speaking_assessment_model.dart';
import '../../core/services/api_service.dart';

class SpeakingProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();

  bool _isLoading = false;
  SpeakingAssessmentResult? _lastAssessmentResult;
  List<SpeakingSession> _sessions = [];

  bool get isLoading => _isLoading;
  SpeakingAssessmentResult? get lastAssessmentResult => _lastAssessmentResult;
  List<SpeakingSession> get sessions => _sessions;

  Future<void> submitSpeaking({
    required String part,
    required String question,
    required String audioPath,
    required int duration,
  }) async {
    _isLoading = true;
    notifyListeners();

    try {
      final result = await _apiService.uploadAudio<Map<String, dynamic>>(
        '/speaking/assess',
        audioPath,
        additionalData: {
          'part': part,
          'question': question,
          'duration': duration.toString(),
        },
      );

      _lastAssessmentResult = SpeakingAssessmentResult.fromJson(result);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      throw Exception('Speaking assessment failed: $e');
    }
  }

  Future<void> loadSessions() async {
    try {
      final response =
          await _apiService.get<List<dynamic>>('/speaking/sessions');
      _sessions = response.map((e) => SpeakingSession.fromJson(e)).toList();
      notifyListeners();
    } catch (e) {
      debugPrint('Failed to load sessions: $e');
    }
  }
}
