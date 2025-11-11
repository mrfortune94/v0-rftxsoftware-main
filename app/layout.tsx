import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'RFTX Tuning - BMW ECU Flasher',
  description: 'Multi-platform BMW ECU flashing and tuning software',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
