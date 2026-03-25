'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/use-auth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Shield, Lock, User, ArrowRight } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const { login, isLoading, error, clearError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    setLocalError('');

    if (!email || !password) {
      setLocalError('PLEASE PROVIDE CREDENTIALS');
      return;
    }

    try {
      await login(email, password);
      router.push('/simulation');
    } catch (err) {
      setLocalError('AUTHENTICATION FAILED');
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
            <div className="w-16 h-16 bg-[#CBF900] mx-auto rounded-sm flex items-center justify-center rotate-45 mb-8 shadow-[0_0_30px_-5px_#CBF900] italic">
               <Shield className="w-8 h-8 text-black -rotate-45" />
            </div>
            <h1 className="text-4xl font-silkscreen text-white tracking-tighter uppercase italic">WAR ROOM ACCESS</h1>
            <p className="text-zinc-500 text-[10px] font-black tracking-widest uppercase italic mt-2 italic">Level 4 Clearance Required</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6 italic">
            <div className="space-y-2 italic">
               <label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase italic italic italic">OPERATOR ID (EMAIL)</label>
               <div className="relative italic">
                  <User className="absolute left-4 top-4 w-4 h-4 text-zinc-600" />
                  <input
                    type="email"
                    placeholder="operator@stockmind.ai"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full bg-black border border-zinc-800 p-4 pl-12 text-sm font-bold tracking-widest uppercase italic rounded-sm focus:border-[#CBF900] outline-none transition-colors"
                  />
               </div>
            </div>

            <div className="space-y-2 italic">
               <label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase italic italic italic">ACCESS KEY (PASSWORD)</label>
               <div className="relative italic">
                  <Lock className="absolute left-4 top-4 w-4 h-4 text-zinc-600" />
                  <input
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-black border border-zinc-800 p-4 pl-12 text-sm font-bold tracking-widest uppercase italic rounded-sm focus:border-[#CBF900] outline-none transition-colors"
                  />
               </div>
            </div>

            {(localError || error) && (
              <motion.div 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="p-4 bg-red-950/20 border border-red-900 text-red-500 text-[10px] font-black tracking-widest uppercase italic italic"
              >
                {localError || error}
              </motion.div>
            )}

            <button
               type="submit"
               disabled={isLoading}
               className="w-full py-5 bg-[#CBF900] text-black font-black tracking-widest uppercase italic flex items-center justify-center gap-3 hover:scale-[1.02] active:scale-95 transition-all rounded-sm shadow-[0_0_40px_-10px_#CBF900]"
            >
               {isLoading ? 'VERIFYING...' : 'INITIALIZE ACCESS'}
               <ArrowRight className="w-5 h-5" />
            </button>
          </form>

          <div className="mt-10 pt-10 border-t border-zinc-800 text-center italic">
             <div className="text-[10px] font-black text-zinc-600 tracking-widest uppercase italic italic">
                First Time Operator?{' '}
                <Link href="/register" className="text-[#CBF900] hover:underline underline-offset-4 ml-2">
                   Request Credentials
                </Link>
             </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
