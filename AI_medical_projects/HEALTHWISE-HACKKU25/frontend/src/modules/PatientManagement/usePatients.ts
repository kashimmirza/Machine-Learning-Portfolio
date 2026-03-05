import { useState, useCallback } from 'react';

export interface Patient {
    id: string;
    name: string;
    age: number;
    gender: string;
    contact: string;
    lastVisit: string;
    status: 'Stable' | 'Critical' | 'Recovering';
}

const MOCK_PATIENTS: Patient[] = [
    {
        id: '1',
        name: 'John Doe',
        age: 45,
        gender: 'Male',
        contact: '+1 234 567 8900',
        lastVisit: '2024-03-15',
        status: 'Stable',
    },
    {
        id: '2',
        name: 'Jane Smith',
        age: 32,
        gender: 'Female',
        contact: '+1 234 567 8901',
        lastVisit: '2024-03-18',
        status: 'Recovering',
    },
    {
        id: '3',
        name: 'Robert Johnson',
        age: 68,
        gender: 'Male',
        contact: '+1 234 567 8902',
        lastVisit: '2024-03-10',
        status: 'Critical',
    },
];

export function usePatients() {
    const [patients, setPatients] = useState<Patient[]>(MOCK_PATIENTS);
    const [searchQuery, setSearchQuery] = useState('');

    const addPatient = useCallback((patient: Omit<Patient, 'id'>) => {
        const newPatient = {
            ...patient,
            id: Math.random().toString(36).substr(2, 9),
        };
        setPatients((prev) => [...prev, newPatient]);
    }, []);

    const updatePatient = useCallback((id: string, updates: Partial<Patient>) => {
        setPatients((prev) =>
            prev.map((p) => (p.id === id ? { ...p, ...updates } : p))
        );
    }, []);

    const deletePatient = useCallback((id: string) => {
        setPatients((prev) => prev.filter((p) => p.id !== id));
    }, []);

    const filteredPatients = patients.filter((patient) =>
        patient.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return {
        patients: filteredPatients,
        searchQuery,
        setSearchQuery,
        addPatient,
        updatePatient,
        deletePatient,
    };
}
