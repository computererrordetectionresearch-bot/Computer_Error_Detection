// FILE: app/layout.tsx
import '../styles/globals.css';

export const metadata = {
  title: 'Installation Error Fixer',
  description: 'Fix installation errors and get installation guides',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

