import 'dart:io';
import 'package:dio/dio.dart';
import 'package:http_parser/http_parser.dart';

class ApiService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'http://localhost:8000/api/v1',
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  // Placeholder token - in real app, get from storage
  String? _token;

  void setToken(String token) {
    _token = token;
  }

  Future<Map<String, dynamic>> analyzeImage(File image) async {
    try {
      String fileName = image.path.split('/').last;
      FormData formData = FormData.fromMap({
        // For web support we might need bytes, but for mobile/desktop File is fine
        "file": await MultipartFile.fromFile(
          image.path, 
          filename: fileName,
          contentType: MediaType('image', 'jpeg') // Adjust if png
        ),
      });

      // Simple anonymous auth for demo, or require login
      // For now assuming public or simple header if needed
      final response = await _dio.post(
        '/analysis/analyze', 
        data: formData,
        options: Options(headers: {
           if(_token != null) "Authorization": "Bearer $_token"
        })
      );
      
      return response.data;
    } catch (e) {
      print("Analysis Error: $e");
      rethrow;
    }
  }
}

final apiService = ApiService();
