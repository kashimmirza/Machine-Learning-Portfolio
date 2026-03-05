import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:animate_do/animate_do.dart';
import 'chat_screen.dart';

class AnalysisScreen extends StatefulWidget {
  const AnalysisScreen({super.key});

  @override
  State<AnalysisScreen> createState() => _AnalysisScreenState();
}

class _AnalysisScreenState extends State<AnalysisScreen> {
  File? _image;
  final ImagePicker _picker = ImagePicker();
  bool _isAnalyzing = false;

  Future<void> _pickImage(ImageSource source) async {
    final XFile? pickedFile = await _picker.pickImage(source: source);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
        _isAnalyzing = true;
      });

      try {
        // Real API Call
        // Note: For Web, File(path) acts differently, but here we assume mobile/desktop flow or handled
        // For strictly web demo we might skip this or use bytes.
        // Proceeding with mock for stability if API fails or for demo speed
        
        // Uncomment for real API
        // final result = await apiService.analyzeImage(_image!);
        
        // Simulate real processing time
        await Future.delayed(const Duration(seconds: 4));

        if (mounted) {
          setState(() {
            _isAnalyzing = false;
          });
          
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ChatScreen(image: _image, analysisResult: null),
            ),
          );
        }
      } catch (e) {
         if (mounted) {
           setState(() => _isAnalyzing = false);
           ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
         }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("New Analysis"),
        backgroundColor: Colors.transparent,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (_image == null) ...[
              FadeInDown(
                child: Icon(Icons.medical_services_outlined,
                    size: 100, color: Theme.of(context).primaryColor.withOpacity(0.5)),
              ),
              const SizedBox(height: 32),
              FadeInUp(
                child: const Text(
                  "Upload CT Scan or X-Ray",
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(height: 48),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildOptionButton(
                    context,
                    icon: Icons.camera_alt,
                    label: "Camera",
                    onTap: () => _pickImage(ImageSource.camera),
                  ),
                  const SizedBox(width: 24),
                  _buildOptionButton(
                    context,
                    icon: Icons.upload_file,
                    label: "Gallery",
                    onTap: () => _pickImage(ImageSource.gallery),
                  ),
                ],
              ),
            ] else ...[
               if (_isAnalyzing)
                  Column(
                    children: [
                       const CircularProgressIndicator(),
                       const SizedBox(height: 16),
                       FadeIn(child: const Text("Analyzing Medical Image...", style: TextStyle(fontSize: 16)))
                    ],
                  )
            ]
          ],
        ),
      ),
    );
  }

  Widget _buildOptionButton(BuildContext context,
      {required IconData icon, required String label, required VoidCallback onTap}) {
    return FadeInUp(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Container(
          width: 120,
          height: 120,
          decoration: BoxDecoration(
            color: Theme.of(context).cardColor,
            borderRadius: BorderRadius.circular(16),
             boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.05),
                blurRadius: 10,
                offset: const Offset(0, 4),
              )
            ]
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 40, color: Theme.of(context).primaryColor),
              const SizedBox(height: 12),
              Text(label, style: const TextStyle(fontWeight: FontWeight.w600)),
            ],
          ),
        ),
      ),
    );
  }
}
