import type { Metadata } from 'next'
import { Space_Grotesk, Silkscreen } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import { AuthProvider } from '@/lib/use-auth'
import './globals.css'

const spaceGrotesk = Space_Grotesk({ 
  subsets: ["latin"],
  weight: ['400', '500', '700']
});

const silkscreen = Silkscreen({ 
  subsets: ["latin"],
  weight: ['400', '700'],
  variable: '--font-silkscreen'
});

export const metadata: Metadata = {
  title: 'StockMind War Room',
  description: 'AI-Powered Market Sentiment Dashboard with Agent Swarm Analytics',
}

import { Navbar } from '@/components/Navbar'

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${spaceGrotesk.className} ${silkscreen.variable} font-sans antialiased text-black bg-black grid-bg pt-16`}>
        <AuthProvider>
          <Navbar />
          {children}
        </AuthProvider>
        <Analytics />
      </body>
    </html>
  )
}
