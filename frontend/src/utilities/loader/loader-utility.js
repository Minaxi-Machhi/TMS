import { defineComponent, h, ref } from "vue";
import loaderGif from "./loader-4.gif";

// Loading state
const isLoading = ref(false);
let delay;

// Methods to control the loader
const show = () => {
    isLoading.value = true;
};

const hide = () => {
    clearTimeout(delay);
    delay = setTimeout(() => { isLoading.value = false; }, 500);
};

// Loader Component
const LoaderComponent = defineComponent({
    setup() {
        return () =>
            isLoading.value
                ? h(
                    "div",
                    { class: "loader-overlay" },
                    h("img", { src: loaderGif, alt: "Loading...", class: "loader-gif" }),
                    h("h6", null, "Loading....")
                )
                : null;
    },
});

// IIFE to inject loader styles dynamically
(() => {
    const style = document.createElement("style");
    style.textContent = `
      .loader-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.1); /* Optional background overlay */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 99999;
      }
      .loader-gif {
        width: auto; /* Automatically adjusts to the size of the GIF */
        height: auto;
        max-width: 100px; /* Prevent oversizing */
        max-height: 100px; /* Prevent oversizing */
      }
    `;
    document.head.appendChild(style);
})();

export default {
    LoaderComponent,
    isLoading,
    show,
    hide,
};
