import "./globals.css";
import {FC, ReactNode} from "react";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Providers from "@/components/Providers";
import {Toaster} from "@/components/ui/sonner";


// fonts

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// website metadata

export const metadata: Metadata = {
  title: "StoraSense"
};

// root layout

const RootLayout: FC<{ children: ReactNode }> = ({ children }) => {
    return (
        <html lang="en">
            <body className={`${geistSans.variable} ${geistMono.variable} antialiased box-border`}>
                <Providers>
                    <Toaster />
                    {children}
                </Providers>
            </body>
        </html>
    );
}

export default RootLayout;
