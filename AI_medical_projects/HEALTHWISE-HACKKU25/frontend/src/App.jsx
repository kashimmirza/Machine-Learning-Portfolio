import React from 'react'
import Navbar from './components/Navbar'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Doctors from './pages/Doctors'
import Login from './pages/Login'
import About from './pages/About'
import Contact from './pages/Contact'
import Appointment from './pages/Appointment'
import MyAppointments from './pages/MyAppointments'
import MyProfile from './pages/MyProfile'
import Footer from './components/Footer'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Verify from './pages/Verify'
import Chat from './pages/Chat'
import HealthAnalysis from './pages/HealthAnalysis'
import MentalHealthAnalysis from './pages/MentalHealthAnalysis'
import HealthWatch from './pages/HealthWatch'
import DiagnosticScanner from './modules/DiagnosticScanner/DiagnosticScanner'
import PatientManagement from './modules/PatientManagement/PatientManagement'
import SymptomChecker from './modules/SymptomChecker/SymptomChecker'
import Appointments from './modules/Appointments/Appointments'
import Prescriptions from './modules/Prescriptions/Prescriptions'
import MedicalRecords from './modules/MedicalRecords/MedicalRecords'
import Telemedicine from './modules/Telemedicine/Telemedicine'

const App = () => {
  return (
    <div className='mx-4 sm:mx-[10%]'>
      <ToastContainer />
      <Navbar />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/doctors' element={<Doctors />} />
        <Route path='/doctors/:speciality' element={<Doctors />} />
        <Route path='/login' element={<Login />} />
        <Route path='/about' element={<About />} />
        <Route path='/contact' element={<Contact />} />
        <Route path='/appointment/:docId' element={<Appointment />} />
        <Route path='/my-appointments' element={<MyAppointments />} />
        <Route path='/my-profile' element={<MyProfile />} />
        <Route path='/verify' element={<Verify />} />
        <Route path='/chat' element={<Chat />} />
        <Route path='/health-analysis' element={<HealthAnalysis />} />
        <Route path='/mental-health-analysis' element={<MentalHealthAnalysis />} />
        <Route path='/health-watch' element={<HealthWatch />} />
        <Route path='/diagnostic-scanner' element={<DiagnosticScanner />} />
        <Route path='/patient-management' element={<PatientManagement />} />
        <Route path='/symptom-checker' element={<SymptomChecker />} />
        <Route path='/appointments' element={<Appointments />} />
        <Route path='/prescriptions' element={<Prescriptions />} />
        <Route path='/medical-records' element={<MedicalRecords />} />
        <Route path='/telemedicine' element={<Telemedicine />} />
      </Routes>
      <Footer />
    </div>
  )
}

export default App