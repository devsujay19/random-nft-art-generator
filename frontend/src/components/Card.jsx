import React from "react";
import a0 from "../assets/art/art_art_0.png";
import a1 from "../assets/art/art_art_1.png";
import a2 from "../assets/art/art_art_2.png";
import a3 from "../assets/art/art_art_3.png";
import a4 from "../assets/art/art_art_4.png";
import a5 from "../assets/art/art_art_5.png";
import a6 from "../assets/art/art_art_6.png";
import a7 from "../assets/art/art_art_7.png";
import a8 from "../assets/art/art_art_8.png";
import a9 from "../assets/art/art_art_9.png";
import a10 from "../assets/art/art_art_10.png";
import a11 from "../assets/art/art_art_11.png";

const Card = () => {
    return (
        <div
            className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-3 lg:grid-cols-4 gap-4" // Responsive grid for small; medium and large screens
        >
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a0} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a1} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a2} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a3} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a4} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a5} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a6} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a7} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a8} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a9} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a10} alt="card-image" />
                </div>
            </div>
            <div class="shadow-sm rounded-lg">
                <div class="m-2.5 overflow-hidden text-white rounded-md">
                    <img src={a11} alt="card-image" />
                </div>
            </div>
        </div>
    );
};

export default Card;