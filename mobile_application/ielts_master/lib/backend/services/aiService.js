/** @format */

// backend/services/aiService.js (Extended with speaking assessment)
class AIService {
 /**
  * Assess IELTS speaking using Whisper (transcription) + GPT-4 (evaluation)
  */
 static async assessSpeaking({ audioPath, part, question }) {
  try {
   // Step 1: Transcribe audio using Whisper
   const transcript = await this.transcribeAudio(audioPath);

   // Step 2: Assess speaking using GPT-4
   const systemPrompt = this.buildSpeakingPrompt(part);

   const completion = await openai.chat.completions.create({
    model: "gpt-4-turbo-preview",
    messages: [
     { role: "system", content: systemPrompt },
     {
      role: "user",
      content: `Question: ${question}\n\nTranscript: ${transcript}`,
     },
    ],
    response_format: { type: "json_object" },
    temperature: 0.3,
   });

   const result = JSON.parse(completion.choices[0].message.content);

   return {
    score: {
     overall: result.overall_score,
     fluencyCoherence: result.fluency_coherence,
     lexicalResource: result.lexical_resource,
     grammaticalAccuracy: result.grammatical_accuracy,
     pronunciation: result.pronunciation,
    },
    feedback: result.feedback,
    transcript,
    pronunciationIssues: result.pronunciation_issues || [],
    fluencyMetrics: {
     wordsPerMinute: result.words_per_minute || 0,
     pauseCount: result.pause_count || 0,
     fillerWords: result.filler_words || [],
    },
   };
  } catch (error) {
   console.error("Speaking Assessment Error:", error);
   throw new Error("Failed to assess speaking");
  }
 }

 /**
  * Transcribe audio using OpenAI Whisper
  */
 static async transcribeAudio(audioPath) {
  try {
   const fs = require("fs");
   const audioFile = fs.createReadStream(audioPath);

   const transcription = await openai.audio.transcriptions.create({
    file: audioFile,
    model: "whisper-1",
    language: "en",
    response_format: "verbose_json",
    timestamp_granularities: ["word"],
   });

   return transcription.text;
  } catch (error) {
   console.error("Transcription Error:", error);
   throw new Error("Failed to transcribe audio");
  }
 }

 /**
  * Build speaking assessment prompt
  */
 static buildSpeakingPrompt(part) {
  const criteria =
   part === "part1"
    ? "Part 1 criteria (personal questions, everyday topics)"
    : part === "part2"
      ? "Part 2 criteria (long turn, describing experience/topic)"
      : "Part 3 criteria (discussion, abstract ideas)";

  return `You are an expert IELTS speaking examiner. Assess this ${part.toUpperCase()} speaking response according to official IELTS ${criteria}.

Provide scores (0.0-9.0, in 0.5 increments) for:
1. Fluency & Coherence (flow, linking, discourse markers)
2. Lexical Resource (vocabulary range, precision, collocations)
3. Grammatical Range & Accuracy (sentence structures, grammar)
4. Pronunciation (clarity, intonation, stress patterns)

Analyze the transcript for:
- Fluency metrics (speaking speed, pauses, hesitations)
- Pronunciation issues (specific words/sounds)
- Grammar and vocabulary usage
- Coherence and organization

Return ONLY valid JSON in this format:
{
  "overall_score": 7.0,
  "fluency_coherence": 7.0,
  "lexical_resource": 7.5,
  "grammatical_accuracy": 7.0,
  "pronunciation": 6.5,
  "feedback": "Detailed assessment paragraph",
  "pronunciation_issues": [
    {"word": "thought", "issue": "th sound", "suggestion": "Practice voiceless th"}
  ],
  "words_per_minute": 140,
  "pause_count": 8,
  "filler_words": ["um", "like", "you know"]
}`;
 }
}
