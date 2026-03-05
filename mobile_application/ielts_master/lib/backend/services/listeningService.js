/** @format */

// backend/services/listeningService.js
const ListeningSession = require("../models/ListeningSession");
const ListeningAudio = require("../models/ListeningAudio");

class ListeningService {
 static async getAudios(accent = "british", difficulty = "medium") {
  const audios = await ListeningAudio.find({
   accent,
   difficulty,
   isActive: true,
  }).limit(10);

  return audios;
 }

 static async evaluateAnswers({ userId, audioId, answers }) {
  const audio = await ListeningAudio.findById(audioId);

  if (!audio) {
   throw new Error("Audio not found");
  }

  let correctCount = 0;
  const results = [];

  audio.questions.forEach((question, index) => {
   const userAnswer = answers[index];
   const isCorrect = this.compareAnswers(userAnswer, question.correctAnswer);

   if (isCorrect) correctCount++;

   results.push({
    questionId: index,
    userAnswer,
    correctAnswer: question.correctAnswer,
    isCorrect,
   });
  });

  const score = this.calculateBandScore(correctCount, audio.questions.length);

  // Save session
  const session = new ListeningSession({
   userId,
   audioId,
   answers,
   correctCount,
   totalQuestions: audio.questions.length,
   score,
   results,
  });
  await session.save();

  return {
   sessionId: session._id,
   score,
   correctCount,
   totalQuestions: audio.questions.length,
   results,
   bandScore: score,
  };
 }

 static compareAnswers(userAnswer, correctAnswer) {
  // Similar to reading service
  if (Array.isArray(correctAnswer)) {
   return correctAnswer.some(
    (ans) => ans.toLowerCase().trim() === userAnswer.toLowerCase().trim(),
   );
  }
  return correctAnswer.toLowerCase().trim() === userAnswer.toLowerCase().trim();
 }

 static calculateBandScore(correct, total) {
  // Same conversion as reading
  const percentage = (correct / total) * 100;

  if (percentage >= 90) return 9.0;
  if (percentage >= 85) return 8.5;
  if (percentage >= 80) return 8.0;
  if (percentage >= 75) return 7.5;
  if (percentage >= 70) return 7.0;
  if (percentage >= 60) return 6.5;
  if (percentage >= 50) return 6.0;
  if (percentage >= 40) return 5.5;
  if (percentage >= 30) return 5.0;
  return 4.5;
 }
}

module.exports = ListeningService;
