import { toast, type ToastType } from 'vue3-toastify';

export function useToastLocal(body: string, type: ToastType) {
  toast(body,
    {
      position: "bottom-left",
      hideProgressBar: false,
      theme: 'light',
      type: type,
      autoClose: 4000,
      closeOnClick: false,
      clearOnUrlChange: false // https://github.com/jerrywu001/vue3-toastify/issues/27
    }
  )
}
