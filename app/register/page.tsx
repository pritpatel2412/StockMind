'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/use-auth';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Shield, Mail, Lock, User, ArrowRight } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const { register, isLoading, error, clearError } = useAuth();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [localError, setLocalError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    setLocalError('');

    if (!fullName || !email || !password || !confirmPassword) {
      setLocalError('ALL SECTORS MUST BE COMPLETED');
      return;
    }

    if (password.length < 8) {
      setLocalError('MINIMUM ENTROPY: 8 CHARACTERS');
      return;
    }

    if (password !== confirmPassword) {
      setLocalError('KEY MISMATCH DETECTED');
      return;
    }

    try {
      await register(email, password, fullName);
      router.push('/simulation');
    } catch (err) {
      setLocalError('REGISTRATION REJECTED');
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4 relative overflow-hidden italic">
      <div className="grid-bg opacity-20 absolute inset-0 pointer-events-none" />
      
      <motion.div 
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md relative z-10"
      >
        <div className="bg-zinc-900/50 border-2 border-zinc-800 backdrop-blur-xl p-10 rounded-sm shadow-2xl shadow-black italic">
          <div className="mb-10 text-center italic">
            <h1 className="text-4xl font-silkscreen text-white tracking-tighter uppercase italic">NEW OPERATOR</h1>
            <p className="text-zinc-500 text-[10px] font-black tracking-widest uppercase italic mt-2 italic">Initiating Enlistment Protocol</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4 italic">
            <div className="space-y-1 italic">
               <label className="text-[9px] font-black text-zinc-500 tracking-widest uppercase italic italic">LEGAL ENTITY NAME</label>
               <input
                  type="text"
                  placeholder="JOHN DOE"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-black border border-zinc-800 p-3 text-xs font-bold tracking-widest uppercase italic rounded-sm focus:border-[#CBF900] outline-none"
               />
            </div>

            <div className="space-y-1 italic">
               <label className="text-[9px] font-black text-zinc-500 tracking-widest uppercase italic italic">COMMS ADDRESS (EMAIL)</label>
               <input
                  type="email"
                  placeholder="OPERATOR@STOCKMIND.AI"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-black border border-zinc-800 p-3 text-xs font-bold tracking-widest uppercase italic rounded-sm focus:border-[#CBF900] outline-none"
               />
            </div>

            <div className="grid grid-cols-2 gap-4 italic italic">
               <div className="space-y-1 italic italic">
                  <label className="text-[9px] font-black text-zinc-500 tracking-widest uppercase italic italic italic">ACCESS KEY</label>
                  <input
                     type="password"
                     placeholder="••••••••"
                     value={password}
                     onChange={(e) => setPassword(e.target.value)}
                     className="w-full bg-black border border-zinc-800 p-3 text-xs font-bold tracking-widest uppercase italic rounded-sm focus:border-[#CBF900] outline-none"
                  />
               </div>
               <div className="space-y-1 italic italic">
                  <label className="text-[9px] font-black text-zinc-500 tracking-widest uppercase italic italic italic">CONFIRM KEY</label>
                  <input
                     type="password"
                     placeholder="••••••••"
                     value={confirmPassword}
                     onChange={(e) => setConfirmPassword(e.target.value)}
                     className="w-full bg-black border border-zinc-800 p-3 text-xs font-bold tracking-widest uppercase italic rounded-sm focus:border-[#CBF900] outline-none"
                  />
               </div>
            </div>

            {(localError || error) && (
              <div className="p-3 bg-red-950/20 border border-red-900 text-red-500 text-[10px] font-black tracking-widest uppercase italic italic italic">
                {localError || error}
              </div>
            )}

            <button
               type="submit"
               disabled={isLoading}
               className="w-full py-4 bg-[#CBF900] text-black font-black tracking-widest uppercase italic flex items-center justify-center gap-3 hover:bg-white transition-all rounded-sm italic"
            >
               {isLoading ? 'ENLISTING...' : 'FINALIZE ENLISTMENT'}
               <ArrowRight className="w-5 h-5" />
            </button>
          </form>

          <div className="mt-8 pt-6 border-t border-zinc-800 text-center italic">
             <div className="text-[10px] font-black text-zinc-600 tracking-widest uppercase italic italic">
                Already an Operator?{' '}
                <Link href="/login" className="text-[#CBF900] hover:underline underline-offset-4 ml-2">
                   Return to Terminal
                </Link>
             </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
