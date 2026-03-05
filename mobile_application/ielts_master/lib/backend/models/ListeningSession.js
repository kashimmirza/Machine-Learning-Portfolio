/** @format */

// backend/models/ListeningSession.js
const mongoose = require("mongoose");

const listeningSessionSchema = new mongoose.Schema({
 userId: {
  type: mongoose.Schema.Types.ObjectId,
  ref: "User",
  required: true,
 },
 audioId: {
  type: mongoose.Schema.Types.ObjectId,
  ref: "ListeningAudio",
  required: true,
 },
 answers: mongoose.Schema.Types.Mixed,
 correctCount: Number,
 totalQuestions: Number,
 score: Number,
 results: [
  {
   questionId: Number,
   userAnswer: String,
   correctAnswer: mongoose.Schema.Types.Mixed,
   isCorrect: Boolean,
  },
 ],
 createdAt: {
  type: Date,
  default: Date.now,
 },
});

listeningSessionSchema.index({ userId: 1, createdAt: -1 });

module.exports = mongoose.model("ListeningSession", listeningSessionSchema);
