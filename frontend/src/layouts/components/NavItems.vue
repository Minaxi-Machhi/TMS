<script setup>
import VerticalNavSectionTitle from "@/@layouts/components/VerticalNavSectionTitle.vue";
import { userProfileServices } from "@/services/user-profile";
import { getColor } from "@/utilities/helpers-utility";
import { toastUtility } from "@/utilities/toast-utility";
import VerticalNavLink from "@layouts/components/VerticalNavLink.vue";

const userPermissions = ref({});

// method to fetch the order list
const getUserPermissions = async () => {
  try {
    const { data } = await userProfileServices.getLoggedInUserPermissions();
    userPermissions.value = data;
  } catch (error) {
    toastUtility.showError(error);
  } finally {
  }
};

onMounted(async () => {
  // await getUserPermissions();
});
</script>

<template>
  <VerticalNavSectionTitle
    :item="{
      heading: 'Navigation',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Dashboard',
      icon: 'ri-dashboard-2-line',
      name: 'dashboard',
      color: getColor('darkGreen'),
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'My Projects',
      icon: 'ri-projector-line',
      name: 'project-list',
      color: getColor('pink'),
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'My Tasks',
      icon: 'ri-projector-line',
      name: 'task-list',
      color: getColor('pink'),
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Users',
      icon: 'ri-projector-line',
      name: 'user-list',
      color: getColor('pink'),
    }"
  />
</template>
