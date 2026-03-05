import React, { useState } from 'react';
import { toast } from 'react-toastify';

const MentalHealthAnalysis = () => {
  const [formData, setFormData] = useState({
    suicidalThoughts: '',
    age: '',
    academicPressure: '',
    financialStress: '',
    jobSatisfaction: '',
    dietHabits: '',
    workStudyHours: '',
    sleepDuration: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    const { suicidalThoughts, age, academicPressure, financialStress, 
            jobSatisfaction, dietHabits, workStudyHours, sleepDuration } = formData;
    
    if (!suicidalThoughts || !age || !academicPressure || !financialStress || 
        !jobSatisfaction || !dietHabits || !workStudyHours || !sleepDuration) {
      toast.error('Please fill in all fields');
      return false;
    }

    if (isNaN(age) || isNaN(academicPressure) || isNaN(financialStress) || 
        isNaN(jobSatisfaction) || isNaN(workStudyHours) || isNaN(sleepDuration)) {
      toast.error('Age, Academic Pressure, Financial Stress, Job Satisfaction, Work/Study Hours, and Sleep Duration must be numbers');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:4000/api/mental-health-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      toast.success('Analysis completed successfully');
    } catch (error) {
      toast.error('Error analyzing mental health data');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold text-gray-900">
            Mental Health Analysis
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Enter your mental health data for analysis
          </p>
        </div>

        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label htmlFor="suicidalThoughts" className="block text-sm font-medium text-gray-700">
                  Have you had suicidal thoughts? (Yes/No)
                </label>
                <select
                  name="suicidalThoughts"
                  id="suicidalThoughts"
                  value={formData.suicidalThoughts}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                >
                  <option value="">Select an option</option>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>

              <div>
                <label htmlFor="age" className="block text-sm font-medium text-gray-700">
                  Age (years)
                </label>
                <input
                  type="number"
                  name="age"
                  id="age"
                  value={formData.age}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="academicPressure" className="block text-sm font-medium text-gray-700">
                  Academic Pressure (1-10)
                </label>
                <input
                  type="number"
                  name="academicPressure"
                  id="academicPressure"
                  min="1"
                  max="10"
                  value={formData.academicPressure}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="financialStress" className="block text-sm font-medium text-gray-700">
                  Financial Stress (1-10)
                </label>
                <input
                  type="number"
                  name="financialStress"
                  id="financialStress"
                  min="1"
                  max="10"
                  value={formData.financialStress}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="jobSatisfaction" className="block text-sm font-medium text-gray-700">
                  Job Satisfaction (1-10)
                </label>
                <input
                  type="number"
                  name="jobSatisfaction"
                  id="jobSatisfaction"
                  min="1"
                  max="10"
                  value={formData.jobSatisfaction}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="dietHabits" className="block text-sm font-medium text-gray-700">
                  Diet Habits
                </label>
                <select
                  name="dietHabits"
                  id="dietHabits"
                  value={formData.dietHabits}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                >
                  <option value="">Select an option</option>
                  <option value="healthy">Healthy</option>
                  <option value="moderate">Moderate</option>
                  <option value="unhealthy">Unhealthy</option>
                </select>
              </div>

              <div>
                <label htmlFor="workStudyHours" className="block text-sm font-medium text-gray-700">
                  Work/Study Hours per day
                </label>
                <input
                  type="number"
                  name="workStudyHours"
                  id="workStudyHours"
                  min="0"
                  max="24"
                  value={formData.workStudyHours}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="sleepDuration" className="block text-sm font-medium text-gray-700">
                  Sleep Duration (hours)
                </label>
                <input
                  type="number"
                  name="sleepDuration"
                  id="sleepDuration"
                  min="0"
                  max="24"
                  value={formData.sleepDuration}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : 'Analyze Mental Health Data'}
              </button>
            </div>
          </form>

          {result && (
            <div className="mt-8 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Analysis Results</h3>
              <div className="prose max-w-none">
                <p className="text-gray-700">{result.analysis}</p>
                {result.recommendations && (
                  <div className="mt-4">
                    <h4 className="text-md font-medium text-gray-900">Recommendations</h4>
                    <ul className="list-disc pl-5 mt-2">
                      {result.recommendations.map((rec, index) => (
                        <li key={index} className="text-gray-700">{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MentalHealthAnalysis; 