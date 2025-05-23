import { createContext, useState, useEffect } from 'react'

export const MainContext = createContext()

export function MainProvider({ children }) {


    const [isMobile, setIsMobile] = useState(window.innerWidth <= 1280)
    const [isHeaderDisplayed, setIsHeaderDisplayed] = useState(false)


    useEffect(() => {
        const handleResize = () => {
          setIsMobile(window.innerWidth <= 1280);
        };
    
        window.addEventListener("resize", handleResize);
    
        return () => window.removeEventListener("resize", handleResize);
      }, []);
   
      let contextData = {
        isMobile: isMobile,
        isHeaderDisplayed: isHeaderDisplayed,
        setIsHeaderDisplayed: setIsHeaderDisplayed
    }

    return (
        <MainContext.Provider value={contextData}>
            {children}
        </MainContext.Provider>
    )
}
