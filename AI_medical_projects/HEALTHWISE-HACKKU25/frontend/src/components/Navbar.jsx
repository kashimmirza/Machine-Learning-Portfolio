import React, { useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { assets } from '../assets/assets'
import { Brain, Activity, Stethoscope, Calendar, FileText, Video, Heart, Pill } from 'lucide-react'

const Navbar = () => {
  const navigate = useNavigate()
  const [showMenu, setShowMenu] = useState(false)
  const [token, setToken] = useState(true)
  const [showAIMenu, setShowAIMenu] = useState(false)

  return (
    <div className='flex items-center justify-between text-sm py-4 mb-5 border-b border-b-gray-400'>
      <img onClick={() => navigate('/')} className='w-44 cursor-pointer' src={assets.logo} alt='' />
      <ul className='hidden md:flex items-start gap-5 font-medium'>
        <NavLink to='/'>
          <li className='py-1'>HOME</li>
          <hr className='border-none outline-none h-0.5 bg-primary w-3/5 m-auto hidden' />
        </NavLink>
        <NavLink to='/doctors'>
          <li className='py-1'>ALL DOCTORS</li>
          <hr className='border-none outline-none h-0.5 bg-primary w-3/5 m-auto hidden' />
        </NavLink>
        <NavLink to='/about'>
          <li className='py-1'>ABOUT</li>
          <hr className='border-none outline-none h-0.5 bg-primary w-3/5 m-auto hidden' />
        </NavLink>
        <NavLink to='/contact'>
          <li className='py-1'>CONTACT</li>
          <hr className='border-none outline-none h-0.5 bg-primary w-3/5 m-auto hidden' />
        </NavLink>

        {/* AI Health Watch Mega Menu */}
        <div
          className='relative'
          onMouseEnter={() => setShowAIMenu(true)}
          onMouseLeave={() => setShowAIMenu(false)}
        >
          <div className='py-1 cursor-pointer flex items-center gap-1 text-primary font-bold'>
            <Brain className='w-4 h-4' />
            AI HEALTH WATCH
          </div>
          {showAIMenu && (
            <div className='absolute top-full left-0 mt-2 w-72 bg-white border border-gray-200 rounded-lg shadow-xl z-50 p-4'>
              <div className='space-y-1'>
                <div onClick={() => navigate('/diagnostic-scanner')} className='flex items-center gap-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors'>
                  <Stethoscope className='w-5 h-5 text-cyan-600' />
                  <div>
                    <div className='font-semibold text-gray-900'>AI Diagnostic Scanner</div>
                    <div className='text-xs text-gray-500'>Multi-organ disease detection</div>
                  </div>
                </div>
                <div onClick={() => navigate('/symptom-checker')} className='flex items-center gap-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors'>
                  <Activity className='w-5 h-5 text-green-600' />
                  <div>
                    <div className='font-semibold text-gray-900'>Symptom Checker</div>
                    <div className='text-xs text-gray-500'>AI-powered triage</div>
                  </div>
                </div>
                <div onClick={() => navigate('/patient-management')} className='flex items-center gap-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors'>
                  <Heart className='w-5 h-5 text-red-600' />
                  <div>
                    <div className='font-semibold text-gray-900'>Patient Management</div>
                    <div className='text-xs text-gray-500'>Comprehensive records</div>
                  </div>
                </div>
                <div onClick={() => navigate('/telemedicine')} className='flex items-center gap-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors'>
                  <Video className='w-5 h-5 text-purple-600' />
                  <div>
                    <div className='font-semibold text-gray-900'>Telemedicine</div>
                    <div className='text-xs text-gray-500'>Virtual consultations</div>
                  </div>
                </div>
                <div onClick={() => navigate('/prescriptions')} className='flex items-center gap-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors'>
                  <Pill className='w-5 h-5 text-orange-600' />
                  <div>
                    <div className='font-semibold text-gray-900'>Prescriptions</div>
                    <div className='text-xs text-gray-500'>Digital Rx management</div>
                  </div>
                </div>
                <div onClick={() => navigate('/medical-records')} className='flex items-center gap-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors'>
                  <FileText className='w-5 h-5 text-blue-600' />
                  <div>
                    <div className='font-semibold text-gray-900'>Medical Records</div>
                    <div className='text-xs text-gray-500'>Patient history</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </ul>
      {/* Rest of navbar code... */}
      <div className='flex items-center gap-4'>
        {
          token
            ? <div className='flex items-center gap-2 cursor-pointer group relative'>
              <img className='w-8 rounded-full' src={assets.profile_pic} alt='' />
              <img className='w-2.5' src={assets.dropdown_icon} alt='' />
              <div className='absolute top-0 right-0 pt-14 text-base font-medium text-gray-600 z-20 hidden group-hover:block'>
                <div className='min-w-48 bg-stone-100 rounded flex flex-col gap-4 p-4'>
                  <p onClick={() => navigate('my-profile')} className='hover:text-black cursor-pointer'>My Profile</p>
                  <p onClick={() => navigate('my-appointments')} className='hover:text-black cursor-pointer'>My Appointments</p>
                  <p onClick={() => setToken(false)} className='hover:text-black cursor-pointer'>Logout</p>
                </div>
              </div>
            </div>
            : <button onClick={() => navigate('/login')} className='bg-primary text-white px-8 py-3 rounded-full font-light hidden md:block'>Create account</button>
        }
        <img onClick={() => setShowMenu(true)} className='w-6 md:hidden' src={assets.menu_icon} alt='' />

        {/* Mobile Menu */}
        <div className={` ${showMenu ? 'fixed w-full' : 'h-0 w-0'} md:hidden right-0 top-0 bottom-0 z-20 overflow-hidden bg-white transition-all`}>
          <div className='flex items-center justify-between px-5 py-6'>
            <img className='w-36' src={assets.logo} alt='' />
            <img className='w-7' onClick={() => setShowMenu(false)} src={assets.cross_icon} alt='' />
          </div>
          <ul className='flex flex-col items-center gap-2 mt-5 px-5 text-lg font-medium'>
            <NavLink onClick={() => setShowMenu(false)} to='/'><p className='px-4 py-2 rounded inline-block'>HOME</p></NavLink>
            <NavLink onClick={() => setShowMenu(false)} to='/doctors' ><p className='px-4 py-2 rounded inline-block'>ALL DOCTORS</p></NavLink>
            <NavLink onClick={() => setShowMenu(false)} to='/about' ><p className='px-4 py-2 rounded inline-block'>ABOUT</p></NavLink>
            <NavLink onClick={() => setShowMenu(false)} to='/contact' ><p className='px-4 py-2 rounded inline-block'>CONTACT</p></NavLink>
            <NavLink onClick={() => setShowMenu(false)} to='/diagnostic-scanner' ><p className='px-4 py-2 rounded inline-block text-primary'>AI SCANNER</p></NavLink>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Navbar