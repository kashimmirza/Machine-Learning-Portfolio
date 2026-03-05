import { useState, useCallback } from 'react';

export interface MedicalRecord {
    id: string;
    date: string;
    type: 'Diagnosis' | 'Lab Result' | 'Procedure' | 'Vaccination';
    title: string;
    description: string;
    doctorName: string;
    attachments?: string[];
}

const MOCK_RECORDS: MedicalRecord[] = [
    {
        id: '1',
        date: '2024-03-10',
        type: 'Diagnosis',
        title: 'Acute Bronchitis',
        description: 'Patient presented with cough and fever. Prescribed antibiotics.',
        doctorName: 'Dr. Sarah Chen',
    },
    {
        id: '2',
        date: '2024-02-15',
        type: 'Lab Result',
        title: 'Blood Panel',
        description: 'Cholesterol levels slightly elevated. Recommended dietary changes.',
        doctorName: 'Dr. Michael Ross',
    },
    {
        id: '3',
        date: '2023-11-20',
        type: 'Vaccination',
        title: 'Influenza Vaccine',
        description: 'Annual flu shot administered.',
        doctorName: 'Nurse Jackie',
    },
];

export function useMedicalRecords() {
    const [records, setRecords] = useState<MedicalRecord[]>(MOCK_RECORDS);

    const addRecord = useCallback((record: Omit<MedicalRecord, 'id'>) => {
        const newRecord = {
            ...record,
            id: Math.random().toString(36).substr(2, 9),
        };
        setRecords((prev) => [newRecord, ...prev]);
    }, []);

    return {
        records,
        addRecord,
    };
}
