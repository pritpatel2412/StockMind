'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Shield, LayoutDashboard, Users, History, Settings, ExternalLink } from 'lucide-react';

const navItems = [
  { name: 'WAR ROOM', href: '/simulation', icon: LayoutDashboard },
  { name: 'AGENTS', href: '/agents', icon: Users },
  { name: 'HISTORY', href: '/history', icon: History },
  { name: 'SETTINGS', href: '/settings', icon: Settings },
];

export const Navbar = () => {
  const pathname = usePathname();
  
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black/95 border-b-2 border-[#CBF900] backdrop-blur-md px-6 py-3">
      <div className="max-w-[1400px] mx-auto flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 bg-[#CBF900] rounded-sm flex items-center justify-center rotate-45 group-hover:rotate-90 transition-transform duration-300">
              <Shield className="w-5 h-5 text-black -rotate-45 group-hover:-rotate-90 transition-transform duration-300" />
            </div>
            <span className="font-silkscreen text-xl tracking-tighter text-[#CBF900]">STOCKMIND</span>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Link 
                  key={item.name} 
                  href={item.href}
                  className="relative px-4 py-2 group"
                >
                  <div className="flex items-center gap-2 relative z-10 text-xs font-bold tracking-widest transition-colors duration-200">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-black' : 'text-[#CBF900]'}`} />
                    <span className={isActive ? 'text-black' : 'text-white group-hover:text-[#CBF900]'}>
                      {item.name}
                    </span>
                  </div>
                  {isActive && (
                    <motion.div 
                      layoutId="nav-active"
                      className="absolute inset-0 bg-[#CBF900] rounded-sm"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                </Link>
              );
            })}
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-1 bg-[#CBF900]/10 border border-[#CBF900]/30 rounded-full">
            <div className="w-2 h-2 bg-[#CBF900] rounded-full animate-pulse shadow-[0_0_8px_#CBF900]" />
            <span className="text-[10px] font-bold text-[#CBF900] tracking-tighter">SERVER LIVE</span>
          </div>
          
          <button className="flex items-center gap-2 px-4 py-2 bg-white text-black text-xs font-black tracking-widest hover:bg-[#CBF900] transition-colors uppercase italic rounded-sm">
            Launch War Room
            <ExternalLink className="w-3 h-3" />
          </button>
        </div>
      </div>
    </nav>
  );
};
