<!-- eslint-disable vue/attribute-hyphenation -->
<template>
  <v-btn id="editOrder" class="mr-2" size="x-small" @click="copyOrder">
    <v-icon start icon="mdi-plus" />
    Add User
  </v-btn>
</template>
      
      <script>
export default {
  components: {},
  props: {
    params: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {
    copyOrder() {
      this.params.context.parentComponent.copyOrder(this.params.data.id);
    },
  },
};
</script>
        