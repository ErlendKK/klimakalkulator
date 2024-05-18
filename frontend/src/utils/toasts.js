import { useToast } from "vue-toastification";

const toast = useToast();

function displaySuccessToast(message="Suksess!") {
    toast.success(message);
}

function displayErrorToast(message="Error!") {
    toast.error(message);
}

function displayWarningToast(message="Obs!") {
    toast.warning(message);
}

export { displaySuccessToast, displayErrorToast, displayWarningToast }