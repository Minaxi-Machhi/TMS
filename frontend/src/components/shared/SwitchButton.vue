<template>
  <VSwitch v-model="toggle" label="Show messages"></VSwitch>
</template>

<script>
export default {
  props: {
    toggle: {
      type: Boolean,
    },
  },
};
</script>
