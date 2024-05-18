import { useToast } from "vue-toastification";

const toast = useToast();

const toastOptions = {
    transition: "Vue-Toastification__fade",
    maxToasts: 8,
    newestOnTop: true,
    position: "top-right",
    timeout: 2500,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: true,
    closeButton: "button",
    icon: true,
    rtl: false
  };

function displaySuccessToast(message="Suksess!") {
    toast.success(message);
}

function displayErrorToast(message="Error!") {
    toast.error(message);
}

function displayWarningToast(message="Obs!") {
    toast.warning(message);
}

export { toastOptions, displaySuccessToast, displayErrorToast, displayWarningToast }