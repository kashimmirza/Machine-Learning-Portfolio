import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize the Gemini API
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

const analyzeHealthData = async (req, res) => {
  try {
    const { pregnancy, glucose, bloodPressure, insulin, bmi, age } = req.body;

    // Validate input data
    if (!pregnancy || !glucose || !bloodPressure || !insulin || !bmi || !age) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    // Create the prompt for few-shot learning
    const prompt = `
      Based on the following medical data, analyze the health condition and provide recommendations:
      
      Patient Data:
      - Number of Pregnancies: ${pregnancy}
      - Glucose Level: ${glucose} mg/dL
      - Blood Pressure: ${bloodPressure} mm Hg
      - Insulin Level: ${insulin} mu U/ml
      - BMI: ${bmi} kg/m²
      - Age: ${age} years

      Examples of analysis:
      1. For a patient with normal ranges:
         - Glucose: 90-100 mg/dL
         - Blood Pressure: 120/80 mm Hg
         - BMI: 18.5-24.9
         Analysis: Normal health indicators
         Recommendations: Maintain current lifestyle, regular checkups

      2. For a patient with elevated levels:
         - Glucose: >126 mg/dL
         - Blood Pressure: >140/90 mm Hg
         - BMI: >30
         Analysis: Potential risk factors present
         Recommendations: Consult healthcare provider, lifestyle modifications

      Please analyze the provided data and provide:
      1. A detailed health analysis
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
    console.error('Error in health analysis:', error);
    res.status(500).json({ error: 'Error analyzing health data' });
  }
};

export { analyzeHealthData }; 