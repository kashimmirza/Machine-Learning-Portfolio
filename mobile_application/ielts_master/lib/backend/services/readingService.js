/** @format */

// backend/services/readingService.js
const ReadingSession = require("../models/ReadingSession");
const ReadingPassage = require("../models/ReadingPassage");

class ReadingService {
 static async getPassages(difficulty = "medium") {
  const passages = await ReadingPassage.find({
   difficulty,
   isActive: true,
  }).limit(10);

  return passages;
 }

 static async evaluateAnswers({ userId, passageId, answers, timeSpent }) {
  const passage = await ReadingPassage.findById(passageId);

  if (!passage) {
   throw new Error("Passage not found");
  }

  let correctCount = 0;
  const results = [];

  passage.questions.forEach((question, index) => {
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

  const score = this.calculateBandScore(correctCount, passage.questions.length);

  // Save session
  const session = new ReadingSession({
   userId,
   passageId,
   answers,
   correctCount,
   totalQuestions: passage.questions.length,
   score,
   timeSpent,
   results,
  });
  await session.save();

  return {
   sessionId: session._id,
   score,
   correctCount,
   totalQuestions: passage.questions.length,
   results,
   bandScore: score,
  };
 }

 static compareAnswers(userAnswer, correctAnswer) {
  if (Array.isArray(correctAnswer)) {
   // Multiple acceptable answers
   return correctAnswer.some(
    (ans) => ans.toLowerCase().trim() === userAnswer.toLowerCase().trim(),
   );
  }
  return correctAnswer.toLowerCase().trim() === userAnswer.toLowerCase().trim();
 }

 static calculateBandScore(correct, total) {
  const percentage = (correct / total) * 100;

  // IELTS Reading band score conversion (approximate)
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

module.exports = ReadingService;
