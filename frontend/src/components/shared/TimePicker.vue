<template>
  <VueDatePicker
    :id="id"
    :model-value="modelValue"
    :teleport="true"
    :auto-apply="true"
    :time-picker="true"
    :is-24="false"
    :clearable="false"
    model-type="HH:mm"
    class="Date_Picker"
    v-bind="$attrs"
    :min-date="min"
    :max-date="max"
    :config="{
      allowStopPropagation: false,
      allowPreventDefault: true,
    }"
    @update:model-value="handleDate"
  >
    <template #dp-input>
      <InputField
        :id="`${id}-input`"
        :model-value="displayTime"
        :name="name"
        :label="label"
        append-inner-icon="mdi-clock-time-three"
        :error-messages="errorMessages"
        :field-rules="rules"
        :is-disabled="isDisabled"
        :bg-color="bgColor"
        :required="isRequired"
        density="compact"
      />
    </template>
  </VueDatePicker>
</template>

<script setup>
import { computed } from "vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

const props = defineProps({
  isRequired: Boolean,
  id: {
    type: String,
    default: "",
  },
  name: {
    type: String,
    default: "",
  },
  min: {
    type: [Number, String],
    default: null,
  },
  max: {
    type: [Number, String],
    default: null,
  },
  bgColor: {
    type: String,
    default: "white",
  },
  modelValue: {
    type: [String, Date, Number],
    default: null,
  },
  isDisabled: {
    type: Boolean,
    default: false,
  },
  rules: {
    type: Array,
    default: () => [],
  },
  errorMessages: {
    type: Array,
    default: () => [],
  },
  label: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue"]);

const formatDate = (value, withTime) => {
  if (value) {
    const _date = new Date(value);
    let date = _date.getDate();
    let month = _date.getMonth() + 1;
    let year = _date.getFullYear();
    date = date < 10 ? `0${date}` : `${date}`;
    month = month < 10 ? `0${month}` : `${month}`;
    let fullDate = [date, month, year].join("/");
    if (withTime) {
      let hour = _date.getHours();
      let minute = _date.getMinutes();
      hour = hour < 10 ? `0${hour}` : `${hour}`;
      minute = minute < 10 ? `0${minute}` : `${minute}`;
      let time = [hour, minute].join(":");
      fullDate = [fullDate, time].join(" ");
    }
    return fullDate;
  }
  return "";
};

const formatViewDate = (value, withTime) => {
  if (value) {
    const _date = new Date(value);
    let date = _date.getDate();
    let month = _date.getMonth() + 1;
    let year = _date.getFullYear();
    date = date < 10 ? `0${date}` : `${date}`;
    month = month < 10 ? `0${month}` : `${month}`;
    let fullDate = [year, month, date].join("-");
    if (withTime) {
      let hour = _date.getHours();
      let minute = _date.getMinutes();
      hour = hour < 10 ? `0${hour}` : `${hour}`;
      minute = minute < 10 ? `0${minute}` : `${minute}`;
      let time = [hour, minute].join(":");
      fullDate = [fullDate, time].join("T");
    }
    return fullDate;
  }
  return "";
};

const displayTime = computed(() => {
  return props.modelValue;
});

const handleDate = (selectedTime) => {
  if (selectedTime) {
    emit("update:modelValue", selectedTime);
  } else {
    emit("update:modelValue", null);
  }
};
</script>

<style lang="scss">
.Date_Picker {
  // Make sure input has 100% of containers, set parent v-cols auto to adjust with menu width
  .dp__input_wrap {
    width: 100%;
    box-sizing: inherit !important;
  }

  // Adjust height of the input block
  .v-text-field input {
    color: #657484 !important;
  }

  .v-field__input {
    padding-top: 0% !important;
    padding-bottom: 0% !important;
  }
}
</style>
