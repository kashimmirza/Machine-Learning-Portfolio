import { useState, useCallback } from 'react';

export interface Prescription {
    id: string;
    medication: string;
    dosage: string;
    frequency: string;
    startDate: string;
    endDate: string;
    status: 'Active' | 'Completed' | 'Discontinued';
    doctorName: string;
}

const MOCK_PRESCRIPTIONS: Prescription[] = [
    {
        id: '1',
        medication: 'Lisinopril',
        dosage: '10mg',
        frequency: 'Once daily',
        startDate: '2024-01-01',
        endDate: '2024-12-31',
        status: 'Active',
        doctorName: 'Dr. Sarah Chen',
    },
    {
        id: '2',
        medication: 'Amoxicillin',
        dosage: '500mg',
        frequency: 'Three times daily',
        startDate: '2024-02-15',
        endDate: '2024-02-25',
        status: 'Completed',
        doctorName: 'Dr. Michael Ross',
    },
];

export function usePrescriptions() {
    const [prescriptions, setPrescriptions] = useState<Prescription[]>(MOCK_PRESCRIPTIONS);

    const addPrescription = useCallback((prescription: Omit<Prescription, 'id'>) => {
        const newPrescription = {
            ...prescription,
            id: Math.random().toString(36).substr(2, 9),
        };
        setPrescriptions((prev) => [newPrescription, ...prev]);
    }, []);

    return {
        prescriptions,
        addPrescription,
    };
}
