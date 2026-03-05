import React, { useState } from 'react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { RadioGroup, RadioGroupItem } from '../../components/ui/radio-group';
import { Checkbox } from '../../components/ui/checkbox';
import { Loader2, AlertTriangle, CheckCircle, Activity, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const SymptomChecker = () => {
    const navigate = useNavigate();
    const [step, setStep] = useState(1);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [result, setResult] = useState<any>(null);

    const [formData, setFormData] = useState({
        primarySymptom: '',
        duration: '',
        severity: 'mild',
        hasFever: false,
        hasPain: false,
        age: '',
    });

    const handleAnalyze = () => {
        setIsAnalyzing(true);
        // Simulate AI Analysis
        setTimeout(() => {
            setIsAnalyzing(false);
            generateResult();
            setStep(3);
        }, 2000);
    };

    const generateResult = () => {
        const severityScore =
            (formData.severity === 'severe' ? 3 : formData.severity === 'moderate' ? 2 : 1) +
            (formData.hasFever ? 2 : 0) +
            (formData.hasPain ? 1 : 0);

        let diagnosis = '';
        let advice = '';
        let urgency = 'low';

        if (severityScore >= 5) {
            diagnosis = 'Potential Acute Infection or Inflammatory Condition';
            advice = 'Your reported symptoms indicate a potentially serious condition. Immediate medical attention is recommended.';
            urgency = 'high';
        } else if (severityScore >= 3) {
            diagnosis = 'Possible Viral Infection or Moderate Strain';
            advice = 'Monitor your symptoms closely. If they persist for more than 24 hours, schedule a consultation.';
            urgency = 'medium';
        } else {
            diagnosis = 'Likely Minor Irritation or Fatigue';
            advice = 'Rest and hydration are severeal. Use over-the-counter remedies if needed.';
            urgency = 'low';
        }

        setResult({ diagnosis, advice, urgency });
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 max-w-2xl mx-auto">
            <div className="text-center space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">AI Symptom Checker</h2>
                <p className="text-muted-foreground">
                    Answer a few questions to get a preliminary health assessment.
                </p>
            </div>

            <Card>
                {step === 1 && (
                    <>
                        <CardHeader>
                            <CardTitle>Describe your symptoms</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label>What is your primary symptom?</Label>
                                <Input
                                    placeholder="e.g., Headache, Nausea, Back pain"
                                    value={formData.primarySymptom}
                                    onChange={(e) => setFormData({ ...formData, primarySymptom: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>How long have you had this?</Label>
                                <Input
                                    placeholder="e.g., 2 days, 1 week"
                                    value={formData.duration}
                                    onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Age</Label>
                                <Input
                                    type="number"
                                    placeholder="Your age"
                                    value={formData.age}
                                    onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                                />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button
                                className="w-full"
                                disabled={!formData.primarySymptom || !formData.duration}
                                onClick={() => setStep(2)}
                            >
                                Next <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                        </CardFooter>
                    </>
                )}

                {step === 2 && !isAnalyzing && (
                    <>
                        <CardHeader>
                            <CardTitle>Additional Details</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="space-y-3">
                                <Label>Severity Level</Label>
                                <RadioGroup
                                    value={formData.severity}
                                    onValueChange={(val) => setFormData({ ...formData, severity: val })}
                                >
                                    <div className="flex items-center space-x-2">
                                        <RadioGroupItem value="mild" id="mild" />
                                        <Label htmlFor="mild">Mild - Noticeable but not disturbing</Label>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <RadioGroupItem value="moderate" id="moderate" />
                                        <Label htmlFor="moderate">Moderate - Affects daily activities</Label>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <RadioGroupItem value="severe" id="severe" />
                                        <Label htmlFor="severe">Severe - Unbearable or incapacitating</Label>
                                    </div>
                                </RadioGroup>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="fever"
                                    checked={formData.hasFever}
                                    onCheckedChange={(checked) => setFormData({ ...formData, hasFever: checked as boolean })}
                                />
                                <Label htmlFor="fever">Do you have a fever?</Label>
                            </div>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="pain"
                                    checked={formData.hasPain}
                                    onCheckedChange={(checked) => setFormData({ ...formData, hasPain: checked as boolean })}
                                />
                                <Label htmlFor="pain">Are you experiencing significant pain?</Label>
                            </div>
                        </CardContent>
                        <CardFooter className="flex gap-3">
                            <Button variant="outline" onClick={() => setStep(1)} className="flex-1">
                                Back
                            </Button>
                            <Button onClick={handleAnalyze} className="flex-1">
                                Analyze Symptoms
                            </Button>
                        </CardFooter>
                    </>
                )}

                {isAnalyzing && (
                    <CardContent className="py-12 flex flex-col items-center justify-center space-y-4">
                        <Loader2 className="h-12 w-12 text-primary animate-spin" />
                        <div className="text-center">
                            <h3 className="text-lg font-semibold">Analyzing Symptoms...</h3>
                            <p className="text-muted-foreground">Our AI is comparing your inputs with medical databases.</p>
                        </div>
                    </CardContent>
                )}

                {step === 3 && result && (
                    <>
                        <CardHeader className={`${result.urgency === 'high' ? 'bg-red-50 text-red-900' :
                                result.urgency === 'medium' ? 'bg-yellow-50 text-yellow-900' :
                                    'bg-green-50 text-green-900'
                            } rounded-t-lg`}>
                            <div className="flex items-center gap-2">
                                {result.urgency === 'high' ? <AlertTriangle className="h-6 w-6" /> :
                                    result.urgency === 'medium' ? <Activity className="h-6 w-6" /> :
                                        <CheckCircle className="h-6 w-6" />}
                                <CardTitle>Analysis Result</CardTitle>
                            </div>
                        </CardHeader>
                        <CardContent className="space-y-4 pt-6">
                            <div>
                                <h4 className="font-semibold text-lg mb-1">{result.diagnosis}</h4>
                                <p className="text-muted-foreground">{result.advice}</p>
                            </div>

                            <div className="bg-muted p-4 rounded-lg">
                                <p className="text-xs text-muted-foreground">
                                    <strong>Disclaimer:</strong> This is an AI-generated assessment and does not replace professional medical advice. Always consult a doctor for a proper diagnosis.
                                </p>
                            </div>
                        </CardContent>
                        <CardFooter className="flex flex-col gap-3 sm:flex-row">
                            <Button variant="outline" onClick={() => { setStep(1); setResult(null); }} className="w-full sm:w-auto">
                                Check Another Symptom
                            </Button>
                            {result.urgency !== 'low' && (
                                <Button onClick={() => navigate('/appointments')} className="w-full sm:w-1 bg-primary">
                                    Book a Consultation
                                </Button>
                            )}
                        </CardFooter>
                    </>
                )}
            </Card>
        </div>
    );
};
