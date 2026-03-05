/** @format */

// backend/routes/speaking.js
const express = require("express");
const router = express.Router();
const multer = require("multer");
const path = require("path");
const authMiddleware = require("../middleware/auth");
const SpeakingService = require("../services/speakingService");
const AIService = require("../services/aiService");

// Configure multer for audio upload
const storage = multer.diskStorage({
 destination: (req, file, cb) => {
  cb(null, "uploads/audio/");
 },
 filename: (req, file, cb) => {
  const uniqueName = `${Date.now()}-${Math.random().toString(36).substring(7)}${path.extname(file.originalname)}`;
  cb(null, uniqueName);
 },
});

const upload = multer({
 storage,
 limits: { fileSize: 50 * 1024 * 1024 }, // 50MB
 fileFilter: (req, file, cb) => {
  const allowedTypes = /aac|m4a|mp3|wav/;
  const extname = allowedTypes.test(
   path.extname(file.originalname).toLowerCase(),
  );
  const mimetype = allowedTypes.test(file.mimetype);

  if (mimetype && extname) {
   return cb(null, true);
  }
  cb(new Error("Only audio files are allowed!"));
 },
});

// Submit speaking for assessment
router.post(
 "/assess",
 authMiddleware,
 upload.single("audio"),
 async (req, res) => {
  try {
   const { part, question, duration } = req.body;
   const userId = req.user.id;
   const audioPath = req.file.path;

   // Call AI service for assessment
   const assessment = await AIService.assessSpeaking({
    audioPath,
    part,
    question,
   });

   // Save to database
   const session = await SpeakingService.saveSession({
    userId,
    part,
    question,
    audioPath,
    duration: parseInt(duration),
    score: assessment.score,
    feedback: assessment.feedback,
    transcript: assessment.transcript,
    pronunciationIssues: assessment.pronunciationIssues,
    fluencyMetrics: assessment.fluencyMetrics,
   });

   res.json({
    id: session._id,
    score: assessment.score,
    feedback: assessment.feedback,
    transcript: assessment.transcript,
    pronunciationIssues: assessment.pronunciationIssues,
    fluencyMetrics: assessment.fluencyMetrics,
    createdAt: session.createdAt,
   });
  } catch (error) {
   res.status(500).json({ error: error.message });
  }
 },
);

// Get speaking questions
router.get("/questions", authMiddleware, async (req, res) => {
 try {
  const { part } = req.query;
  const questions = await SpeakingService.getQuestions(part);
  res.json(questions);
 } catch (error) {
  res.status(500).json({ error: error.message });
 }
});

module.exports = router;
