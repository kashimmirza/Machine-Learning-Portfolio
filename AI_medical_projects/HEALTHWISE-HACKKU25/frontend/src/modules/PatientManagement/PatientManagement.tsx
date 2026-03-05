import React, { useState } from 'react';
import { usePatients } from './usePatients';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '../../components/ui/table';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Plus, Search, User } from 'lucide-react';
import { AddPatientModal } from './AddPatientModal';
import { useNavigate } from 'react-router-dom';

export const PatientManagement = () => {
    const { patients, searchQuery, setSearchQuery, addPatient } = usePatients();
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const navigate = useNavigate();

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Patient Management</h2>
                    <p className="text-muted-foreground">
                        Manage patient records and profiles.
                    </p>
                </div>
                <Button onClick={() => setIsAddModalOpen(true)}>
                    <Plus className="mr-2 h-4 w-4" /> Add Patient
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Patients Directory</CardTitle>
                    <div className="flex items-center space-x-2">
                        <Search className="h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search patients..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="max-w-sm"
                        />
                    </div>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Age</TableHead>
                                <TableHead>Gender</TableHead>
                                <TableHead>Contact</TableHead>
                                <TableHead>Last Visit</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {patients.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={7} className="text-center py-8">
                                        No patients found.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                patients.map((patient) => (
                                    <TableRow
                                        key={patient.id}
                                        className="cursor-pointer hover:bg-muted/50"
                                        onClick={() => navigate(`/patients/${patient.id}`)}
                                    >
                                        <TableCell className="font-medium">
                                            <div className="flex items-center space-x-2">
                                                <User className="h-8 w-8 p-1.5 bg-primary/10 rounded-full text-primary" />
                                                <span>{patient.name}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>{patient.age}</TableCell>
                                        <TableCell>{patient.gender}</TableCell>
                                        <TableCell>{patient.contact}</TableCell>
                                        <TableCell>{patient.lastVisit}</TableCell>
                                        <TableCell>
                                            <span
                                                className={`px-2 py-1 rounded-full text-xs font-medium ${patient.status === 'Stable'
                                                        ? 'bg-green-100 text-green-700'
                                                        : patient.status === 'Critical'
                                                            ? 'bg-red-100 text-red-700'
                                                            : 'bg-yellow-100 text-yellow-700'
                                                    }`}
                                            >
                                                {patient.status}
                                            </span>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Button variant="ghost" size="sm">
                                                View
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            <AddPatientModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                onAdd={addPatient}
            />
        </div>
    );
};
