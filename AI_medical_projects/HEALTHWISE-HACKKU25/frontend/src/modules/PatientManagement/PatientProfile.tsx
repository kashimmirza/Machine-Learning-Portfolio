import React from 'react';
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { User } from 'lucide-react';

export const PatientProfile = () => {
    const { id } = useParams();

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <h2 className="text-3xl font-bold tracking-tight">Patient Profile</h2>
            <Card>
                <CardHeader>
                    <CardTitle>Patient Details</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center space-x-4">
                        <div className="h-20 w-20 bg-primary/10 rounded-full flex items-center justify-center">
                            <User className="h-10 w-10 text-primary" />
                        </div>
                        <div>
                            <h3 className="text-xl font-semibold">Patient ID: {id}</h3>
                            <p className="text-muted-foreground">Detailed profile view coming soon.</p>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};
