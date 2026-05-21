import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'JSAAI',
  description: 'Bootstrap do projeto React',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
