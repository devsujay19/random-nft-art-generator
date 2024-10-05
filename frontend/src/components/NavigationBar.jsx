import React from "react";
import github from "../assets/image.png";

const NavigationBar = () => {

    return (

        <span>
            <a href="https://github.com/devsujay19/random-nft-art-generator/" target="_blank">
                <img src={github} className="rounded-full cursor-pointer w-16 h-16 fixed bottom-3 right-3 hover:w-20 hover:h-20 hover:bottom-5 hover:right-5 transition-all delay-200 duration-[1000] ease-in-out" alt="github" />
            </a>
        </span>

    );
};

export default NavigationBar;