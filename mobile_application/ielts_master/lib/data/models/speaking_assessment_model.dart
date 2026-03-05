// lib/data/models/speaking_assessment_model.dart
class SpeakingAssessmentResult {
  final String id;
  final num score;
  final String feedback;
  final Map<String, dynamic> details;

  SpeakingAssessmentResult({
    required this.id,
    required this.score,
    required this.feedback,
    required this.details,
  });

  factory SpeakingAssessmentResult.fromJson(Map<String, dynamic> json) {
    return SpeakingAssessmentResult(
      id: json['id'] as String? ?? '',
      score: json['score'] as num? ?? 0,
      feedback: json['feedback'] as String? ?? '',
      details: json['details'] as Map<String, dynamic>? ?? {},
    );
  }
}

class SpeakingSession {
  final String id;
  final String part;
  final String question;
  final String? recordingPath;
  final DateTime createdAt;

  SpeakingSession({
    required this.id,
    required this.part,
    required this.question,
    this.recordingPath,
    required this.createdAt,
  });

  factory SpeakingSession.fromJson(Map<String, dynamic> json) {
    return SpeakingSession(
      id: json['id'] as String? ?? '',
      part: json['part'] as String? ?? '',
      question: json['question'] as String? ?? '',
      recordingPath: json['recordingPath'] as String?,
      createdAt: json['createdAt'] != null
          ? DateTime.parse(json['createdAt'] as String)
          : DateTime.now(),
    );
  }
}
