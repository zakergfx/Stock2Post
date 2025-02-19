import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const style = {
    position: "bottom-right",
    autoClose: 3000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
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
    }
}

export default Alert