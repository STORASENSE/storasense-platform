"use client"

import {FC} from "react";
import HomePageComponent from "@/components/HomePageComponent";

const HomePage: FC = () => {
    return (
        <div className="w-full max-w-[1200px] mx-auto p-5">
            <header className="text-center mb-10">
                <h1 className="font-bold text-3xl">
                    StoraSense
                </h1>
                <p className="text-gray-500">Welcome to our system!</p>
            </header>

            <section>
                {}
                <HomePageComponent />
            </section>
        </div>
    );
}

export default HomePage;
