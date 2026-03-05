import React, { useState } from 'react';
import { useMedicalRecords } from './useMedicalRecords';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Plus, Search, FileText, Activity, Stethoscope, Syringe } from 'lucide-react';
import { AddRecordModal } from './AddRecordModal';
import { ScrollArea } from '../../components/ui/scroll-area';

export const MedicalRecords = () => {
    const { records, addRecord } = useMedicalRecords();
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');

    const filteredRecords = records.filter((r) =>
        r.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const getIcon = (type: string) => {
        switch (type) {
            case 'Diagnosis':
                return <Stethoscope className="h-4 w-4" />;
            case 'Lab Result':
                return <Activity className="h-4 w-4" />;
            case 'Vaccination':
                return <Syringe className="h-4 w-4" />;
            default:
                return <FileText className="h-4 w-4" />;
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Medical Records</h2>
                    <p className="text-muted-foreground">
                        Patient history and documentation.
                    </p>
                </div>
                <Button onClick={() => setIsAddModalOpen(true)}>
                    <Plus className="mr-2 h-4 w-4" /> Add Record
                </Button>
            </div>

            <div className="flex items-center space-x-2">
                <Search className="h-4 w-4 text-muted-foreground" />
                <Input
                    placeholder="Search records..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="max-w-sm"
                />
            </div>

            <ScrollArea className="h-[600px] pr-4">
                <div className="relative space-y-6 pl-6 before:absolute before:inset-0 before:ml-2.5 before:h-full before:w-0.5 before:bg-border">
                    {filteredRecords.map((record) => (
                        <div key={record.id} className="relative">
                            <span className="absolute left-[-2.15rem] top-3 flex h-6 w-6 items-center justify-center rounded-full bg-background border-2 border-primary ring-4 ring-background">
                                {getIcon(record.type)}
                            </span>
                            <Card>
                                <CardHeader>
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <CardTitle className="text-lg">{record.title}</CardTitle>
                                            <CardDescription>{record.date}</CardDescription>
                                        </div>
                                        <span className="text-xs font-medium px-2 py-1 bg-secondary rounded-full">
                                            {record.type}
                                        </span>
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm text-gray-600 mb-2">{record.description}</p>
                                    <div className="text-xs text-muted-foreground">
                                        Recorded by: {record.doctorName}
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    ))}
                </div>
            </ScrollArea>

            <AddRecordModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                onAdd={addRecord}
            />
        </div>
    );
};
