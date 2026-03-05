/** @format */

// backend/models/SpeakingSession.js
const mongoose = require("mongoose");

const speakingSessionSchema = new mongoose.Schema({
 userId: {
  type: mongoose.Schema.Types.ObjectId,
  ref: "User",
  required: true,
 },
 part: {
  type: String,
  enum: ["part1", "part2", "part3"],
  required: true,
 },
 question: {
  type: String,
  required: true,
 },
 audioPath: {
  type: String,
  required: true,
 },
 duration: {
  type: Number,
  required: true,
 },
 transcript: String,
 score: {
  overall: Number,
  fluencyCoherence: Number,
  lexicalResource: Number,
  grammaticalAccuracy: Number,
  pronunciation: Number,
 },
 feedback: String,
 pronunciationIssues: [
  {
   word: String,
   issue: String,
   suggestion: String,
  },
 ],
 fluencyMetrics: {
  wordsPerMinute: Number,
  pauseCount: Number,
  fillerWords: [String],
 },
 createdAt: {
  type: Date,
  default: Date.now,
 },
});

speakingSessionSchema.index({ userId: 1, createdAt: -1 });

module.exports = mongoose.model("SpeakingSession", speakingSessionSchema);
