import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const style = {
    position: "bottom-right",
    autoClose: 6000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: false,
    draggable: true,
    progress: undefined,
    theme: "dark",
}
const Alert = {
    error(msg) {
        toast.error(msg, {
            ...style

        });
    },
    success(msg) {
        toast.success(msg, {
            ...style
        });
    },
    info(msg) {
        toast.info(msg, {
            ...style
        });
    }
}

export default Alert