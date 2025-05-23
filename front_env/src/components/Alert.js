import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


const Alert = {
    error(msg) {
        toast.error(msg);
    },
    success(msg) {
        toast.success(msg);
    },
    info(msg) {
        toast.info(msg);
    },

    promise(fct) {
        toast.promise(fct, {
            pending: "Post en cours de création",
            success: "Post créé avec succès !",
            error: "Impossible de créer le post"
        })
    }


}

export default Alert