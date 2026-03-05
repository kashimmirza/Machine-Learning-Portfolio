// lib/data/models/assessment_model.dart
class AssessmentModel {
  final String id;
  final String userId;
  final String type; // reading, writing, listening, speaking
  final num score;
  final Map<String, dynamic> details;
  final DateTime completedAt;

  AssessmentModel({
    required this.id,
    required this.userId,
    required this.type,
    required this.score,
    required this.details,
    required this.completedAt,
  });

  factory AssessmentModel.fromJson(Map<String, dynamic> json) {
    return AssessmentModel(
      id: json['id'] as String? ?? '',
      userId: json['userId'] as String? ?? '',
      type: json['type'] as String? ?? '',
      score: json['score'] as num? ?? 0,
      details: json['details'] as Map<String, dynamic>? ?? {},
      completedAt: json['completedAt'] != null
          ? DateTime.parse(json['completedAt'] as String)
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'type': type,
      'score': score,
      'details': details,
      'completedAt': completedAt.toIso8601String(),
    };
  }
}
