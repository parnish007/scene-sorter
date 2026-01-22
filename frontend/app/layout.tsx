import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Scene Sorter",
  description:
    "AI-powered image scene classification and automatic folder organization.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen flex flex-col">
          {children}
        </div>
      </body>
    </html>
  );
}
