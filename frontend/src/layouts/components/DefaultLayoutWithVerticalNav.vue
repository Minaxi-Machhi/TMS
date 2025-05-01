<script setup>
import NavItems from '@/layouts/components/NavItems.vue';
import UserProfile from '@/layouts/components/user-profile.vue';
import { userProfileServices } from '@/services/user-profile';
import { getColor } from '@/utilities/helpers-utility';
import loaderUtility from '@/utilities/loader/loader-utility';
import { toastUtility } from '@/utilities/toast-utility';
import logo from '@images/logo.svg?raw';
import VerticalNavLayout from '@layouts/components/VerticalNavLayout.vue';
import moment from 'moment';
import { onMounted, onUnmounted } from 'vue';

const userData = ref({});

// method to fetch order details
const getLoggedInUserDetails = async (id) => {
  try {
    loaderUtility.show();
    const { data } = await userProfileServices.getLoggedInUserDetails();
    userData.value = data;
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
}

// computed property for date formating.
const nativeTimeStamp = (isoTimeString) => {
  return moment(isoTimeString).format("YYYY-MM-DD HH:mm:ss A");
}


onMounted(async () => {
  await getLoggedInUserDetails();
});

</script>

<template>
  <VerticalNavLayout>
    <!-- 👉 navbar -->
    <template #navbar="{ toggleVerticalOverlayNavActive }">
      <div class="d-flex h-100 align-center">
        <!-- 👉 Vertical nav toggle in overlay mode -->
        <IconBtn class="ms-n3 d-lg-none" @click="toggleVerticalOverlayNavActive(true)">
          <VIcon icon="ri-menu-line" />
        </IconBtn>

        <!-- 👉 Search -->
        <!-- <div
          class="d-flex align-center cursor-pointer"
          style="user-select: none;"
        >
          
          <IconBtn>
            <VIcon icon="ri-search-line" />
          </IconBtn>

          <span class="d-none d-md-flex align-center text-disabled">
            <span class="me-3">Search</span>
            <span class="meta-key">&#8984;K</span>
          </span>
        </div> -->

        <VSpacer />

        <!-- <IconBtn
          href="https://github.com/themeselection/materio-vuetify-vuejs-admin-template-free"
          target="_blank"
          rel="noopener noreferrer"
        >
          <VIcon icon="ri-github-fill" />
        </IconBtn> -->

        <IconBtn class="mr-5">

          <v-menu offset-y :close-on-content-click="false">
            <!-- Activator (Button with Badge) -->
            <template #activator="{ props }">
              <v-badge v-bind="props" :content="10" :color="getColor('red')">
                <VIcon icon="ri-notification-line" />
              </v-badge>
            </template>
          </v-menu>
        </IconBtn>
        <!-- 
        <NavbarThemeSwitcher class="me-2" /> -->

        <UserProfile :userData="userData" />
      </div>
    </template>

    <template #vertical-nav-header="{ toggleIsOverlayNavActive }">
      <RouterLink to="/" class="app-logo app-title-wrapper" style="height: 40px;">
        <!-- eslint-disable vue/no-v-html -->
        <div v-html="logo" />
        <!-- eslint-enable -->

        <!-- <h1 class="font-weight-medium leading-normal text-xl text-uppercase">
          Noatum
        </h1> -->
      </RouterLink>

      <IconBtn class="d-block d-lg-none" @click="toggleIsOverlayNavActive(false)">
        <VIcon icon="ri-close-line" />
      </IconBtn>

    </template>

    <template #vertical-nav-content>
      <NavItems />
    </template>

    <!-- 👉 Pages -->
    <slot />

    <!-- 👉 Footer -->
    <!-- <template #footer>
      <Footer />
    </template> -->
  </VerticalNavLayout>
</template>

<style lang="scss" scoped>
.meta-key {
  border: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 6px;
  block-size: 1.5625rem;
  line-height: 1.3125rem;
  padding-block: 0.125rem;
  padding-inline: 0.25rem;
}

.app-logo {
  display: flex;
  align-items: center;
  column-gap: 0.75rem;

  .app-logo-title {
    font-size: 1.25rem;
    font-weight: 500;
    line-height: 1.75rem;
    text-transform: uppercase;
  }
}

.scroll-container {
  max-height: 400px;
  overflow: hidden;
}

.bg-grey {
  background-color: rgb(214, 209, 209);
}

.bg-light-grey {
  background-color: rgb(249, 244, 244);
}
</style>
