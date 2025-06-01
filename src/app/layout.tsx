// These styles apply to every route in the application
import './globals.css'

export default function RootLayout({
    children,
  }: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className="p-2 bg-slate-700">
                <main className="p-2 flex flex-column flex-wrap justify-center">
                    {children}
                </main>
            </body>
        </html>
    )
}