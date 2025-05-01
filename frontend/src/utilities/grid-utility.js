import { defineComponent, h } from "vue";
import { useRouter } from "vue-router";
import { VAvatar, VBtn, VChip, VIcon, VImg, VTooltip } from "vuetify/components";

export const gridUtility = {
    /**
     * Utility function to create a Vuetify cell renderer for Ag-Grid.
     * @returns {Object} A Vue component.
     */
    createWarningCell() {
        return defineComponent({
            props: {
                // Ag-Grid passes cell data through `params`
                params: {
                    type: Object,
                    required: true
                }
            },
            setup(props) {
                return () => {
                    // Only render the button if there's a value
                    if (!props.params?.value) return null;

                    return h(
                        "div",
                        { class: "d-flex justify-center align-center py-1" },
                        [
                            h(
                                VBtn,
                                { icon: true, size: "x-small", class: "elevation-3 border", color: "white" },
                                [
                                    h(VIcon, { size: "default", icon: "mdi-alert", color: "#ff0000" }),
                                    h(VTooltip, { activator: "parent" }, () => props.params.value),
                                ]
                            ),
                        ]
                    );
                };
            },
        });
    },


    /**
     * Utility function to create a Vuetify chip cell renderer for Ag-Grid.
     * @returns {Object} A Vue component.
     */
    createChipCell() {
        return defineComponent({
            props: {
                params: {
                    type: Object,
                    required: true
                }
            },
            setup(props) {
                return () => {
                    const statusValue = props.params.value;
                    const statusColor = props.params.color;

                    // If no status, return null (empty cell)
                    if (!statusValue) return null;

                    return h(
                        VChip,
                        { color: statusColor, class:"text-capitalize", size: "x-small", density: "default", variant: "flat", style: "font-size: 11px;" },
                        () => statusValue
                    );
                };
            },
        });
    },


    /**color
     * Utility function to create a Vuetify cell renderer for Ag-Grid that renders a clickable link.
     * @returns {Object} A Vue component.
     */
    createRedirectionCell() {
        return defineComponent({
            props: {
                params: {
                    type: Object,
                    required: true
                }
            },
            setup(props) {
                const router = useRouter();

                return () => {
                    const { value, routeName, routeParams, url } = props.params;

                    if (!value) return null; // Don't render if no value

                    if (url) {
                        // External Link
                        return h(
                            "a",
                            {
                                href: url,
                                target: "_blank",
                                rel: "noopener noreferrer",
                                class: "text-primary text-decoration-underline",
                            },
                            value
                        );
                    } else if (routeName) {
                        // Internal Router Link
                        return h(
                            "a",
                            {
                                href: "#",
                                class: "text-primary text-decoration-underline",
                                onClick: (event) => {
                                    event.preventDefault();
                                    router.push({ name: routeName, params: routeParams || {} });
                                }
                            },
                            value
                        );
                    }

                    return null;
                };
            },
        });
    },

    /**
     * Utility function to create a Vuetify avatar cell renderer for Ag-Grid.
     * Supports initials or image URL via mutually exclusive keys: `imageUrl` and `initials`.
     * @returns {Object} A Vue component.
     */
    createAvatarCell() {
        return defineComponent({
            props: {
                params: {
                    type: Object,
                    required: true
                }
            },
            setup(props) {
                return () => {
                    const { imageUrl, initials, bgColor } = props.params;
                    if (!imageUrl && !initials) return null;

                    return h(
                        VAvatar,
                        {
                            size: "32",
                            color: bgColor,
                        },
                        imageUrl
                            ? h(VImg, { src: imageUrl })
                            : h("span", { class: "text-capitalize" }, initials)
                    );
                };
            },
        });
    },

};
