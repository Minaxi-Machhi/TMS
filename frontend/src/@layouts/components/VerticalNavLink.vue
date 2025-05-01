<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const router = useRouter();
</script>

<template>
  <li class="nav-link" :class="{ disabled: item.disable }">
    <Component :is="item.to || item.name ? 'RouterLink' : 'a'"
      :to="item.name ? { name: item.name, params: item.params || {} } : item.to" :href="item.href"
      :target="item.target">
      <VIcon :icon="item.icon || 'ri-checkbox-blank-circle-line'" class="nav-item-icon" :color="item.color" />
      <!-- 👉 Title -->
      <span class="nav-item-title">
        {{ item.title }}
      </span>
      <span class="nav-item-badge" :class="item.badgeClass">
        {{ item.badgeContent }}
      </span>
    </Component>
  </li>
</template>

<style lang="scss">
.layout-vertical-nav {
  .nav-link a {
    display: flex;
    align-items: center;
    cursor: pointer;
  }
}
</style>
