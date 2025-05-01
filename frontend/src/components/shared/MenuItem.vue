<template>
  <v-btn
    variant="text"
    class="Menu_Item"
    :class="{
      'is-active': isActive && isActive(),
      'text-white': isActive && isActive(),
    }"
    @click="action"
    :title="title"
    :icon="icon"
    size="x-small"
    color="primary"
  ></v-btn>
</template>

<script setup>
// Define props
const props = defineProps({
  icon: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  action: {
    type: Function,
    required: true,
  },
  isActive: {
    type: Function,
    default: null,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});
</script>

<style lang="scss">
@import "vuetify/lib/styles/settings/_colors.scss";

.Menu_Item {
  background: transparent;
  border: none;
  border-radius: 3rem;
  color: #fff;
  cursor: pointer;
  height: 1.75rem;
  padding: 0.25rem;
  margin-right: 0.25rem;
  width: 1.75rem;
  transition: 0.25s all ease;

  i {
    color: map-get($map: $purple, $key: "darken-3");
  }

  &.is-active,
  &:hover {
    background-color: map-get($map: $purple, $key: "darken-2");

    i {
      color: map-get($map: $shades, $key: "white");
    }
  }

  &.text-white {
    color: map-get($map: $shades, $key: "white") !important;
  }

  &:not(.is-active):hover {
    background-color: map-get($map: $shades, $key: "transparent");
    border: 1px solid map-get($map: $purple, $key: "darken-3");

    i {
      color: map-get($map: $purple, $key: "darken-3");
    }
  }
}
</style>
