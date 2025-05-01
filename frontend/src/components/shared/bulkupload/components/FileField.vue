<template>
    <v-file-input class="Border-Remove File-Input" density="compact" variant="outlined" bg-color="white"
        hide-details="auto" prepend-icon="" prepend-inner-icon="mdi-paperclip" :class="class" :show-size="false"
        :counter="false" :label="label ? `${label}${isRequired ? ' *' : ''}` : ''" :rules="[
            ...addRequiredRule(),
            ...addMaxSizeRule(),
            ...addAcceptedFileExtensionsRule(),
            ...fieldRules,
        ]" v-bind="$attrs" v-model="files" :multiple="multiple" @click:clear="$emit('change', undefined)" @change="
            $emit('change', multiple ? $event.target.files : $event.target.files[0])
            "></v-file-input>
</template>

<script>
export default {
    props: {
        modelValue: {
            type: [File, Array, null],
            default: null,
        },
        class: {
            type: String,
        },
        label: {
            required: false,
        },
        isRequired: {
            default: false,
        },
        multiple: {
            default: false,
        },
        fieldRules: {
            default: () => [],
        },
        maxAllowedSize: {
            type: Number,
            default: null,
        },
        maxAllowedSizeErrorMessage: {
            type: String,
            default: "File exceeds allowed size",
        },
    },
    emits: ["change", "update:modelValue"],
    computed: {
        files: {
            get() {
                return this.multiple
                    ? this.modelValue
                    : this.modelValue
                        ? new Array(this.modelValue)
                        : new Array();
            },
            set(files) {
                if (files && files.length) {
                    const val = this.multiple ? files : files[0];
                    this.$emit("update:modelValue", val);
                }
            },
        },
    },
    methods: {
        /**
         * @description Return array of rule functions for required rule
         * @returns {Array<Function>} Array of rule functions
         */
        addRequiredRule() {
            return this.isRequired
                ? [
                    (files) =>
                        (files && files?.length > 0) ||
                        `${this.label ? this.label : "Field"} is Required`,
                ]
                : [];
        },

        /**
         * @description Return array of rule functions for max allowed size rule
         * @returns {Array<Function>} Array of rule functions
         */
        addMaxSizeRule() {
            return this.isRequired && this.maxAllowedSize
                ? [
                    (files) =>
                        (files && files[0]?.size < this.maxAllowedSize) ||
                        (files && files.length > 0 && this.maxAllowedSizeErrorMessage),
                ]
                : [];
        },

        /**
         * @description Return array of rule functions for accepted file extensions
         * @returns {Array<Function>} Array of rule functions
         */
        addAcceptedFileExtensionsRule() {
            return this.$attrs.accept && !this.multiple
                ? [
                    (files) => {
                        const file = files[0];
                        if (!file) return true;

                        // * Check if file extension is among valid extensions
                        const validExtensions = this.$attrs.accept
                            .split(",")
                            .map((ext) => ext.trim());
                        const fileExtension = file && `.${file?.name?.split(".").pop()}`;

                        return (
                            validExtensions.includes(fileExtension) ||
                            `Only ${this.$attrs.accept} are allowed`
                        );
                    },
                ]
                : [];
        },
    },
};
</script>
<style lang="scss">
.File-Input {

    // * To hide file details container if messages are empty and it is only child
    .v-input__details:has(> .v-messages:empty):has(:only-child) {
        display: none;
    }
}
</style>
