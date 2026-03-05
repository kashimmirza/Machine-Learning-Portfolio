import { useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, Brain, Heart, Apple, Send } from 'lucide-react';
import axios from 'axios';

const HealthWatch = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [vitalsData, setVitalsData] = useState({ heart_rate: 72, sys_bp: 120 });

    const API_URL = 'http://localhost:8000';

    const sendToAgent = async (agentType, data) => {
        try {
            setLoading(true);
            const response = await axios.post(`${API_URL}/api/agents/chat`, {
                agent_type: agentType,
                data: data
            });

            setMessages(prev => [...prev, {
                role: 'agent',
                content: response.data,
                timestamp: new Date().toLocaleTimeString()
            }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                role: 'error',
                content: `Error: ${error.response?.data?.detail || error.message}`,
                timestamp: new Date().toLocaleTimeString()
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleVitalsCheck = () => {
        sendToAgent('vitals', vitalsData);
    };

    const handleNutritionCheck = () => {
        const mealData = { meal_type: 'Lunch', calories: 650 };
        sendToAgent('nutrition', mealData);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-8"
                >
                    <div className="flex items-center justify-center gap-3 mb-4">
                        <Brain className="w-12 h-12 text-purple-600" />
                        <h1 className="text-4xl font-bold text-gray-800">AI Health Watch</h1>
                    </div>
                    <p className="text-gray-600">Multi-Agent Health Monitoring System</p>
                </motion.div>

                {/* Quick Actions */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleVitalsCheck}
                        className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all"
                    >
                        <Heart className="w-10 h-10 text-red-500 mb-3 mx-auto" />
                        <h3 className="font-semibold text-lg mb-2">Check Vitals</h3>
                        <p className="text-sm text-gray-600">Analyze heart rate & BP</p>
                    </motion.button>

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleNutritionCheck}
                        className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all"
                    >
                        <Apple className="w-10 h-10 text-green-500 mb-3 mx-auto" />
                        <h3 className="font-semibold text-lg mb-2">Nutrition AI</h3>
                        <p className="text-sm text-gray-600">Diet recommendations</p>
                    </motion.button>

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all"
                    >
                        <Activity className="w-10 h-10 text-blue-500 mb-3 mx-auto" />
                        <h3 className="font-semibold text-lg mb-2">AI Diagnosis</h3>
                        <p className="text-sm text-gray-600">Coming soon</p>
                    </motion.button>
                </div>

                {/* Agent Response Display */}
                <div className="bg-white rounded-xl shadow-lg p-6 max-h-96 overflow-y-auto">
                    <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                        <Brain className="w-6 h-6 text-purple-600" />
                        Agent Responses
                    </h2>

                    {messages.length === 0 ? (
                        <div className="text-center text-gray-400 py-8">
                            <p>No agent responses yet. Try checking your vitals or nutrition!</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {messages.map((msg, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    className={`p-4 rounded-lg ${msg.role === 'error'
                                            ? 'bg-red-50 border border-red-200'
                                            : 'bg-blue-50 border border-blue-200'
                                        }`}
                                >
                                    <div className="text-xs text-gray-500 mb-2">{msg.timestamp}</div>
                                    <pre className="text-sm whitespace-pre-wrap">
                                        {JSON.stringify(msg.content, null, 2)}
                                    </pre>
                                </motion.div>
                            ))}
                        </div>
                    )}

                    {loading && (
                        <div className="text-center py-4">
                            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-purple-500 border-t-transparent"></div>
                        </div>
                    )}
                </div>

                {/* Vitals Input (for testing) */}
                <div className="mt-6 bg-white rounded-xl shadow-lg p-6">
                    <h3 className="font-semibold mb-4">Test Vitals Input</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm text-gray-600 mb-1">Heart Rate (bpm)</label>
                            <input
                                type="number"
                                value={vitalsData.heart_rate}
                                onChange={(e) => setVitalsData({ ...vitalsData, heart_rate: parseInt(e.target.value) })}
                                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                            />
                        </div>
                        <div>
                            <label className="block text-sm text-gray-600 mb-1">Systolic BP</label>
                            <input
                                type="number"
                                value={vitalsData.sys_bp}
                                onChange={(e) => setVitalsData({ ...vitalsData, sys_bp: parseInt(e.target.value) })}
                                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HealthWatch;
