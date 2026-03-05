// lib/core/services/api_service.dart
class ApiService {
  Future<T> get<T>(String endpoint) async {
    // TODO: Implement GET request
    throw UnimplementedError();
  }

  Future<T> post<T>(String endpoint,
      {required Map<String, dynamic> data}) async {
    // TODO: Implement POST request
    throw UnimplementedError();
  }

  Future<T> uploadAudio<T>(String endpoint, String audioPath,
      {Map<String, dynamic>? additionalData}) async {
    // TODO: Implement audio upload
    throw UnimplementedError();
  }

  Future<T> put<T>(String endpoint,
      {required Map<String, dynamic> data}) async {
    // TODO: Implement PUT request
    throw UnimplementedError();
  }

  Future<void> delete(String endpoint) async {
    // TODO: Implement DELETE request
  }
}
