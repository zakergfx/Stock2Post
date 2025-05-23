import { useContext, useEffect, useState } from 'react'
import * as Tooltip from '@radix-ui/react-tooltip';
import { Info } from 'lucide-react';

function ToolTip(props) {

    return (<div className="ToolTip">
        <Tooltip.Provider>
            <Tooltip.Root>
                <Tooltip.Trigger asChild>
                    <span className="cursor-pointer">
                        <Info className="w-4 h-4 text-gray-500" />
                    </span>
                </Tooltip.Trigger>
                <Tooltip.Portal>
                    <Tooltip.Content
                        className="bg-gray-800 text-white text-sm p-2 rounded-md shadow-lg"
                        side="top"
                        align="center"
                    >
                        
                        <span className="Tip"> {props.msg}</span>
                        <Tooltip.Arrow className="fill-gray-800" />
                    </Tooltip.Content>
                </Tooltip.Portal>
            </Tooltip.Root>
        </Tooltip.Provider>
    </div>)

}

export default ToolTip