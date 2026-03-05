import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize the Gemini API
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

const analyzeMentalHealthData = async (req, res) => {
  try {
    const { 
      suicidalThoughts, 
      age, 
      academicPressure, 
      financialStress, 
      jobSatisfaction, 
      dietHabits, 
      workStudyHours, 
      sleepDuration 
    } = req.body;

    // Validate input data
    if (!suicidalThoughts || !age || !academicPressure || !financialStress || 
        !jobSatisfaction || !dietHabits || !workStudyHours || !sleepDuration) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    // Create the prompt for few-shot learning
    const prompt = `
      Based on the following mental health data, analyze the condition and provide recommendations:
      
      Patient Data:
      - Suicidal Thoughts: ${suicidalThoughts}
      - Age: ${age} years
      - Academic Pressure: ${academicPressure}/10
      - Financial Stress: ${financialStress}/10
      - Job Satisfaction: ${jobSatisfaction}/10
      - Diet Habits: ${dietHabits}
      - Work/Study Hours: ${workStudyHours} hours per day
      - Sleep Duration: ${sleepDuration} hours

      Examples of analysis:
      1. For a patient with concerning indicators:
         - Suicidal Thoughts: Yes
         - Academic Pressure: 9/10
         - Financial Stress: 8/10
         - Job Satisfaction: 2/10
         - Sleep Duration: 4 hours
         Analysis: High risk factors present
         Recommendations: Immediate professional help needed, crisis intervention

      2. For a patient with moderate indicators:
         - Academic Pressure: 7/10
         - Financial Stress: 5/10
         - Job Satisfaction: 6/10
         - Sleep Duration: 6 hours
         Analysis: Moderate stress levels
         Recommendations: Stress management techniques, better sleep hygiene

      3. For a patient with good indicators:
         - Academic Pressure: 4/10
         - Financial Stress: 3/10
         - Job Satisfaction: 8/10
         - Sleep Duration: 8 hours
         Analysis: Good mental health indicators
         Recommendations: Maintain current practices, regular self-care

      Please analyze the provided data and provide:
      1. A detailed mental health analysis
      2. Specific recommendations based on the data
    `;

    // Get the generative model
    const model = genAI.getGenerativeModel({ 
      model: "gemini-2.0-flash"
    });

    // Generate content
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    // Parse the response to extract analysis and recommendations
    const analysis = text.split('Recommendations:')[0].trim();
    const recommendations = text.split('Recommendations:')[1]
      ? text.split('Recommendations:')[1]
          .split('\n')
          .filter(line => line.trim())
          .map(line => line.replace(/^\d+\.\s*/, '').trim())
      : [];

    res.json({
      analysis,
      recommendations
    });
  } catch (error) {
    console.error('Error in mental health analysis:', error);
    res.status(500).json({ error: 'Error analyzing mental health data' });
  }
};

export { analyzeMentalHealthData }; 