<template>
  <v-file-input
    v-model:file="files"
    class="Border-Remove File-Input"
    density="compact"
    variant="outlined"
    bg-color="white"
    hide-details="auto"
    prepend-icon=""
    prepend-inner-icon="mdi-paperclip"
    :class="fileClass"
    rows="1"
    :show-size="false"
    :counter="false"
    :label="computedLabel"
    :rules="rules"
    v-bind="$attrs"
    :multiple="multiple"
    @click:clear="$emit('change', undefined)"
    @change="handleFileChange"
  ></v-file-input>
</template>

<script setup>
import { computed, toRefs } from "vue";

const props = defineProps({
  modelValue: {
    type: [File, Array, null],
    default: null,
  },
  fileClass: {
    type: String,
    default: "",
  },
  label: {
    type: String,
    default: "",
    required: false,
  },
  isRequired: {
    type: Boolean,
    default: false,
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  fieldRules: {
    type: Array,
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
});

const emit = defineEmits(["change", "update:modelValue"]);

const {
  modelValue,
  label,
  isRequired,
  multiple,
  fieldRules,
  maxAllowedSize,
  maxAllowedSizeErrorMessage,
} = toRefs(props);

const files = computed({
  get() {
    return multiple.value
      ? modelValue.value
      : modelValue.value
      ? [modelValue.value]
      : [];
  },
  set(files) {
    if (files && files.length) {
      const val = multiple.value ? files : files[0];
      emit("update:modelValue", val);
    }
  },
});

const computedLabel = computed(() => {
  return label.value ? `${label.value}${isRequired.value ? " *" : ""}` : "";
});

const addRequiredRule = () => {
  return isRequired.value
    ? [
        (files) =>
          (files && files.length > 0) ||
          `${label.value ? label.value : "Field"} is Required`,
      ]
    : [];
};

const addMaxSizeRule = () => {
  return isRequired.value && maxAllowedSize.value
    ? [
        (files) =>
          (files && files[0]?.size < maxAllowedSize.value) ||
          (files && files.length > 0 && maxAllowedSizeErrorMessage.value),
      ]
    : [];
};

const addAcceptedFileExtensionsRule = () => {
  return props.accept && !multiple.value
    ? [
        (files) => {
          const file = files[0];
          if (!file) return true;

          const validExtensions = props.accept
            .split(",")
            .map((ext) => ext.trim());
          const fileExtension = file && `.${file.name.split(".").pop()}`;

          return (
            validExtensions.includes(fileExtension) ||
            `Only ${props.accept} are allowed`
          );
        },
      ]
    : [];
};

const rules = computed(() => [
  ...addRequiredRule(),
  ...addMaxSizeRule(),
  ...addAcceptedFileExtensionsRule(),
  ...fieldRules.value,
]);

const handleFileChange = (event) => {
  emit("change", multiple.value ? event.target.files : event.target.files[0]);
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
