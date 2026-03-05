/** @format */

// backend/services/speakingService.js
const SpeakingSession = require("../models/SpeakingSession");
const SpeakingQuestion = require("../models/SpeakingQuestion");

class SpeakingService {
 static async getQuestions(part = "part1") {
  const questions = await SpeakingQuestion.find({
   part,
   isActive: true,
  }).limit(20);

  return questions;
 }

 static async saveSession(sessionData) {
  const session = new SpeakingSession(sessionData);
  await session.save();
  return session;
 }

 static async getUserSessions(userId, limit = 20) {
  const sessions = await SpeakingSession.find({ userId })
   .sort({ createdAt: -1 })
   .limit(limit);

  return sessions;
 }
}

module.exports = SpeakingService;
