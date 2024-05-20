"use client";
import Navbar from "@/components/Navbar";
import { useSession } from "next-auth/react";
import Image from "next/image";
import React, { useState } from "react";
import Link from "next/link";
import ThisCantBeReached from "@/components/thisSiteCanBeReached/site-reach";
import Startup from "@/components/startupLogo/startup-logo";
import { motion } from "framer-motion"

export default function Home() {

    const [showThisCantBeReached, setShowThisCantBeReached] = useState(true);
    setTimeout(() => {
        setShowThisCantBeReached(false);
    }, 5400);
    return (
        <>
            {showThisCantBeReached ? (
                <ThisCantBeReached />
            ) : (<main className="flex flex-col items-center min-h-screen ">
                <div className="relative flex justify-center w-full bg-blue-950">
                    <Image
                        className=""
                        width={500}
                        height={300}
                        src="/truck1.png"
                    ></Image>
                    <p className="absolute text-3xl bottom-12 ">
                        Your Delivery, Your Way.
                    </p>
                </div>
            </main>)}
        </>
    );
}
