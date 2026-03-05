/** @format */

// backend/models/ReadingSession.js
const mongoose = require("mongoose");

const readingSessionSchema = new mongoose.Schema({
 userId: {
  type: mongoose.Schema.Types.ObjectId,
  ref: "User",
  required: true,
 },
 passageId: {
  type: mongoose.Schema.Types.ObjectId,
  ref: "ReadingPassage",
  required: true,
 },
 answers: mongoose.Schema.Types.Mixed,
 correctCount: Number,
 totalQuestions: Number,
 score: Number,
 timeSpent: Number,
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

readingSessionSchema.index({ userId: 1, createdAt: -1 });

module.exports = mongoose.model("ReadingSession", readingSessionSchema);
