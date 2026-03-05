import React, { useState } from 'react';
import { toast } from 'react-toastify';

const HealthAnalysis = () => {
  const [formData, setFormData] = useState({
    pregnancy: '',
    glucose: '',
    bloodPressure: '',
    insulin: '',
    bmi: '',
    age: ''
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
    const { pregnancy, glucose, bloodPressure, insulin, bmi, age } = formData;
    
    if (!pregnancy || !glucose || !bloodPressure || !insulin || !bmi || !age) {
      toast.error('Please fill in all fields');
      return false;
    }

    if (isNaN(pregnancy) || isNaN(glucose) || isNaN(bloodPressure) || 
        isNaN(insulin) || isNaN(bmi) || isNaN(age)) {
      toast.error('All fields must be numbers');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:4000/api/health-analysis', {
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
      toast.error('Error analyzing health data');
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
            Health Analysis
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Enter your medical data for analysis
          </p>
        </div>

        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label htmlFor="pregnancy" className="block text-sm font-medium text-gray-700">
                  Number of Pregnancies
                </label>
                <input
                  type="number"
                  name="pregnancy"
                  id="pregnancy"
                  value={formData.pregnancy}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="glucose" className="block text-sm font-medium text-gray-700">
                  Glucose Level (mg/dL)
                </label>
                <input
                  type="number"
                  name="glucose"
                  id="glucose"
                  value={formData.glucose}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="bloodPressure" className="block text-sm font-medium text-gray-700">
                  Blood Pressure (mm Hg)
                </label>
                <input
                  type="number"
                  name="bloodPressure"
                  id="bloodPressure"
                  value={formData.bloodPressure}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="insulin" className="block text-sm font-medium text-gray-700">
                  Insulin Level (mu U/ml)
                </label>
                <input
                  type="number"
                  name="insulin"
                  id="insulin"
                  value={formData.insulin}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="bmi" className="block text-sm font-medium text-gray-700">
                  BMI (kg/m²)
                </label>
                <input
                  type="number"
                  name="bmi"
                  id="bmi"
                  value={formData.bmi}
                  onChange={handleChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
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
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : 'Analyze Health Data'}
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

export default HealthAnalysis; 