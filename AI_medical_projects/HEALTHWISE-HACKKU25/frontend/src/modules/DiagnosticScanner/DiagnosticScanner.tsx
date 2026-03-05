import React, { useState } from 'react';
import { Button } from '../../components/ui/button';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/ui/tabs';
import { Badge } from '../../components/ui/badge';
import { ScannerInterface } from './components/ScannerInterface';
import { BodyVisualizer } from './components/BodyVisualizer';
import { AnalysisReport } from './components/AnalysisReport';
import { BrainCircuit, Eye, Activity, ScanFace, Droplets } from 'lucide-react';
import { toast } from 'sonner';

export const DiagnosticScanner = () => {
    const [activeTab, setActiveTab] = useState('scan');
    const [isScanning, setIsScanning] = useState(false);
    const [scanType, setScanType] = useState('eyes');
    const [scannedParts, setScannedParts] = useState<string[]>([]);
    const [results, setResults] = useState<any[]>([]);
    const [prescriptions, setPrescriptions] = useState<any[]>([]);

    // New Global Audio State
    const [isAudioPlaying, setIsAudioPlaying] = useState(false);

    const handleStartScan = () => {
        setIsScanning(true);
        setIsAudioPlaying(false); // Stop audio if new scan starts
    };

    const handleScanComplete = (type: string) => {
        setIsScanning(false);
        toast.success(`${type.toUpperCase()} Scan Completed Successfully`);

        // Add to scanned parts if not already there
        const partName = type.charAt(0).toUpperCase() + type.slice(1);
        if (!scannedParts.includes(partName)) {
            setScannedParts([...scannedParts, partName]);
        }

        // Simulate Result Generation
        generateMockResult(type);
    };

    const generateMockResult = (type: string) => {
        let newResult;
        let newRx;

        switch (type) {
            case 'eyes':
                newResult = {
                    part: 'Eyes',
                    condition: 'Mild Diabetic Retinopathy Signs',
                    risk: 'Medium',
                    confidence: 89,
                    details: 'Microaneurysms detected in peripheral retina. Vascular patterns indicate early stage stress.',
                    doctorAnalysis: 'Based on the fundus scan, I am observing distinct microaneurysms in the peripheral quadrants. While the macula appears relatively clear, these early vascular changes are classic indicators of diabetic stress on the retinal vessels. Immediate blood sugar control is paramount to prevent progression to proliferative retinopathy.',
                    preventiveMeasures: [
                        'Strict Glycemic Control (HbA1c < 7%)',
                        'Annual Dilated Eye Exams',
                        'Blood Pressure Monitoring',
                        'Consultation with Endocrinologist'
                    ]
                };
                newRx = {
                    name: 'Ranibizumab (Lucentis)',
                    dosage: '0.5 mg intravitreal injection',
                    reason: 'To reduce fluid leakage and localized retinal swelling.'
                };
                break;
            case 'skin':
                newResult = {
                    part: 'Skin',
                    condition: 'Benign Seborrheic Keratosis',
                    risk: 'Low',
                    confidence: 94,
                    details: 'Pigmented lesion with well-defined borders. Non-cancerous characteristics observed.',
                    doctorAnalysis: 'The lesion presents with a classic "stuck-on" appearance, well-circumscribed borders, and uniform pigmentation. These features are highly characteristic of a Seborrheic Keratosis, which is a common benign skin growth. There are no signs of asymmetry or irregular borders that would suggest Melanoma.',
                    preventiveMeasures: [
                        'Monitor for changes in size or color',
                        'Apply broad-spectrum sunscreen daily',
                        'No surgical removal required unless irritated'
                    ]
                };
                break;
            case 'throat':
                newResult = {
                    part: 'Throat',
                    condition: 'Viral Pharyngitis',
                    risk: 'Low',
                    confidence: 91,
                    details: 'Redness and inflammation of pharynx. No exudate present.',
                    doctorAnalysis: 'The pharyngeal wall shows mild to moderate erythema (redness) without the presence of purulent exudates or tonsillar hypertrophy. The uvula is midline and not swollen. This clinical picture strongly points towards a viral etiology rather than a bacterial infection like Strep Throat.',
                    preventiveMeasures: [
                        'Warm Salt Water Gargles (3x daily)',
                        'Hydration with warm fluids',
                        'Voice Rest',
                        'Monitor temperature'
                    ]
                };
                newRx = { name: 'Benzydamine Mouthwash', dosage: '15ml every 3 hours', reason: 'Analgesic/Anti-inflammatory for throat pain relief.' }
                break;
            case 'nails':
                newResult = {
                    part: 'Nails',
                    condition: 'Beau\'s Lines (Vitamin Deficiency)',
                    risk: 'Low',
                    confidence: 88,
                    details: 'Horizontal ridges observed on nail plate. Indicative of temporary growth arrest.',
                    doctorAnalysis: 'The horizontal depressions (Beau\'s Lines) running across the nail plate suggest a systemic insult that occurred weeks ago. This pattern is commonly associated with zinc deficiency or a recent febrile illness. The nail bed itself is healthy, ruling out fungal onychomycosis.',
                    preventiveMeasures: [
                        'Dietary Supplementation (Zinc & Biotin)',
                        'Improve protein intake',
                        'Hydrate nails with cuticle oil',
                        'Blood test for nutritional profile'
                    ]
                };
                newRx = { name: 'Multivitamin Complex (Zinc+)', dosage: '1 tablet daily with food', reason: 'To replenish micronutrient stores.' }
                break;
            default:
                newResult = { part: 'General', condition: 'Healthy', risk: 'Low', confidence: 99, details: 'No anomalies detected.' };
        }

        setResults(prev => [...prev.filter(r => r.part !== newResult.part), newResult]);
        if (newRx) setPrescriptions(prev => [...prev, newRx]);
    };

    return (
        <div className="h-full p-2 md:p-6 space-y-6 animate-in fade-in duration-700">

            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <div className="flex items-center gap-2">
                        <BrainCircuit className="h-8 w-8 text-cyan-500" />
                        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-cyan-500 to-blue-600 bg-clip-text text-transparent">
                            AI Diagnostic Scanner
                        </h1>
                    </div>
                    <p className="text-muted-foreground mt-1">
                        Deep-learning powered multi-organ disease detection system.
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-cyan-600 border-cyan-200 bg-cyan-50">
                        <Activity className="h-3 w-3 mr-1" /> System Ready
                    </Badge>
                    <Badge variant="outline" className="text-purple-600 border-purple-200 bg-purple-50">
                        v2.4.0 (Beta)
                    </Badge>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

                {/* Main Scanner Area */}
                <div className="lg:col-span-8 space-y-4">
                    {/* Organ Selector Tabs */}
                    <Tabs defaultValue="eyes" onValueChange={(val) => setScanType(val)} className="w-full">
                        <TabsList className="grid w-full grid-cols-4 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
                            <TabsTrigger value="eyes" disabled={isScanning} className="data-[state=active]:bg-cyan-500 data-[state=active]:text-white">
                                <Eye className="h-4 w-4 mr-2" /> Eyes
                            </TabsTrigger>
                            <TabsTrigger value="skin" disabled={isScanning} className="data-[state=active]:bg-cyan-500 data-[state=active]:text-white">
                                <ScanFace className="h-4 w-4 mr-2" /> Skin
                            </TabsTrigger>
                            <TabsTrigger value="throat" disabled={isScanning} className="data-[state=active]:bg-cyan-500 data-[state=active]:text-white">
                                <Activity className="h-4 w-4 mr-2" /> Tongue
                            </TabsTrigger>
                            <TabsTrigger value="nails" disabled={isScanning} className="data-[state=active]:bg-cyan-500 data-[state=active]:text-white">
                                <Droplets className="h-4 w-4 mr-2" /> Nails
                            </TabsTrigger>
                        </TabsList>
                    </Tabs>

                    {/* Camera View - Now Receives Audio State */}
                    <ScannerInterface
                        isScanning={isScanning}
                        scanType={scanType}
                        onScanComplete={handleScanComplete}
                        isAudioPlaying={isAudioPlaying}
                    />

                    {/* Controls */}
                    <div className="flex justify-center pt-4">
                        <Button
                            size="lg"
                            className={`w-48 h-14 text-lg font-bold shadow-lg shadow-cyan-500/20 rounded-full transition-all duration-300 ${isScanning ? 'bg-red-500 hover:bg-red-600' : 'bg-cyan-500 hover:bg-cyan-600 hover:scale-105'
                                }`}
                            onClick={() => setIsScanning(!isScanning)}
                        >
                            {isScanning ? 'STOP SCAN' : 'START SCAN'}
                        </Button>
                    </div>
                </div>

                {/* Sidebar: Viz & Results */}
                <div className="lg:col-span-4 space-y-6">
                    <div className="h-[300px]">
                        {/* Body Viz - Now Receives Audio State and Active Organ */}
                        <BodyVisualizer
                            scannedParts={scannedParts}
                            activePart={scanType}
                            isAnimating={isAudioPlaying}
                        />
                    </div>

                    {/* Report - Now Controls Parent Audio State */}
                    <AnalysisReport
                        results={results}
                        prescriptions={prescriptions}
                        onAudioToggle={(playing) => setIsAudioPlaying(playing)}
                        isExternalPlaying={isAudioPlaying}
                    />
                </div>

            </div>
        </div>
    );
};
