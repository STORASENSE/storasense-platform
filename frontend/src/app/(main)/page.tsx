"use client"

import {FC} from "react";
import HomePageComponent from "@/components/HomePageComponent";
import Image from "next/image";

const HomePage: FC = () => {
    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="flex items-center gap-16">
                <div className="flex items-center gap-8">
                    <Image
                        src="/logo-animated.gif"
                        alt="StoraSense Logo Animation"
                        width={80}
                        height={80}
                        unoptimized={true}
                        className="object-contain"
                    />
                    <div className="text-left">
                        <h1 className="font-bold text-3xl mb-2">
                            StoraSense
                        </h1>
                        <p className="text-gray-500">Welcome to your storage guardian!</p>
                    </div>
                </div>
                <div className="h-32 w-px bg-gray-300"></div>
                <div>
                    <HomePageComponent />
                </div>
            </div>
        </div>
    );
}

export default HomePage;
