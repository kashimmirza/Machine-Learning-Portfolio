import React, { useState } from 'react';
import { usePrescriptions } from './usePrescriptions';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '../../components/ui/table';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Plus, Search, Pill } from 'lucide-react';
import { AddPrescriptionModal } from './AddPrescriptionModal';

export const Prescriptions = () => {
    const { prescriptions, addPrescription } = usePrescriptions();
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');

    const filteredPrescriptions = prescriptions.filter((p) =>
        p.medication.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Prescriptions</h2>
                    <p className="text-muted-foreground">
                        Manage active and past medications.
                    </p>
                </div>
                <Button onClick={() => setIsAddModalOpen(true)}>
                    <Plus className="mr-2 h-4 w-4" /> Add Prescription
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Medication List</CardTitle>
                    <div className="flex items-center space-x-2">
                        <Search className="h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search medications..."
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
                                <TableHead>Medication</TableHead>
                                <TableHead>Dosage</TableHead>
                                <TableHead>Frequency</TableHead>
                                <TableHead>Start Date</TableHead>
                                <TableHead>End Date</TableHead>
                                <TableHead>Prescribed By</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredPrescriptions.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={7} className="text-center py-8">
                                        No prescriptions found.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredPrescriptions.map((p) => (
                                    <TableRow key={p.id}>
                                        <TableCell className="font-medium flex items-center gap-2">
                                            <Pill className="h-4 w-4 text-primary" />
                                            {p.medication}
                                        </TableCell>
                                        <TableCell>{p.dosage}</TableCell>
                                        <TableCell>{p.frequency}</TableCell>
                                        <TableCell>{p.startDate}</TableCell>
                                        <TableCell>{p.endDate}</TableCell>
                                        <TableCell>{p.doctorName}</TableCell>
                                        <TableCell>
                                            <span
                                                className={`px-2 py-1 rounded-full text-xs font-medium ${p.status === 'Active'
                                                        ? 'bg-green-100 text-green-700'
                                                        : p.status === 'Completed'
                                                            ? 'bg-blue-100 text-blue-700'
                                                            : 'bg-gray-100 text-gray-700'
                                                    }`}
                                            >
                                                {p.status}
                                            </span>
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            <AddPrescriptionModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                onAdd={addPrescription}
            />
        </div>
    );
};
