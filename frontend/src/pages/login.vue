<script setup>
import logo from '@images/logo.svg?raw';
import authV1MaskDark from '@images/pages/auth-v1-mask-dark.png';
import authV1MaskLight from '@images/pages/auth-v1-mask-light.png';
import authV1Tree2 from '@images/pages/auth-v1-tree-2.png';
import authV1Tree from '@images/pages/auth-v1-tree.png';
// external imports
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useTheme } from 'vuetify';

// service imports
import { authenticationService } from '@/services/authentication';

// utility imports
import { localStorageUtility } from '@/utilities/local-storage-utility';
import { toastUtility } from '@/utilities/toast-utility';
import { useRouter } from 'vue-router';

const vuetifyTheme = useTheme();
const isPasswordVisible = ref(false);
const router = useRouter();

const loginForm = reactive({
  username: null,
  password: null
});

const rules = reactive({
  username: { required },
  password: { required }
});

const v$ = useVuelidate(rules, loginForm);

const login = async () => {
  const isValidate = await v$.value.$validate();
  if (!isValidate) {
    toastUtility.showError("Please correct all the errors to submit the form!");
    return;
  }
  try {
    let { data } = await authenticationService.login(loginForm);
    localStorageUtility.setItemToLocalStorage("tms_user", data.token);
    router.push({ name: "dashboard" });
  } catch (error) {
    toastUtility.showError(error);
  } finally {

  }
}

const authThemeMask = computed(() => {
  return vuetifyTheme.global.name.value === 'light' ? authV1MaskLight : authV1MaskDark
})

</script>

<template>
  <!-- eslint-disable vue/no-v-html -->
  <div class="auth-wrapper d-flex align-center justify-center pa-4">
    <VCard class="auth-card pa-4 pt-7" max-width="448">
      <VCardItem class="justify-center">
        <VCardTitle>
          <RouterLink to="/">
            <!-- eslint-disable vue/no-v-html -->
            <div v-html="logo"></div>

            <!-- <h2 class="font-weight-medium text-2xl text-uppercase">
            Noatum
          </h2> -->
          </RouterLink>
        </VCardTitle>
      </VCardItem>
      <VCardText class="pt-2">
        <h4 class="text-h4 mb-1">
          Welcome! 👋🏻
        </h4>
        <p class="mb-0">
          Please sign-in to your account and start the adventure
        </p>
      </VCardText>

      <VCardText>
        <VRow>
          <!-- email -->
          <VCol cols="12">
            <VTextField v-model="loginForm.username" label="Username" @blur="v$.username.$validate"
              :error-messages="v$.username.$errors.map(e => e.$message)" @input="v$.username.$reset"
              @focus="v$.username.$reset" />
          </VCol>

          <!-- password -->
          <VCol cols="12">
            <VTextField v-model="loginForm.password" label="Password" placeholder="············"
              :type="isPasswordVisible ? 'text' : 'password'"
              :append-inner-icon="isPasswordVisible ? 'ri-eye-off-line' : 'ri-eye-line'"
              @click:append-inner="isPasswordVisible = !isPasswordVisible" @blur="v$.password.$validate"
              :error-messages="v$.password.$errors.map(e => e.$message)" @input="v$.password.$reset"
              @focus="v$.password.$reset" />

            <!-- remember me checkbox -->
            <div class="d-flex align-center justify-space-between flex-wrap my-4">
              <!-- <VCheckbox v-model="form.remember" label="Remember me" />

                <a class="text-primary" href="javascript:void(0)">
                  Forgot Password?
                </a> -->
            </div>

            <!-- login button -->
            <VBtn block @click="login">
              Login
            </VBtn>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <VImg class="auth-footer-start-tree d-none d-md-block" :src="authV1Tree" :width="250" />

    <VImg :src="authV1Tree2" class="auth-footer-end-tree d-none d-md-block" :width="350" />

    <!-- bg img -->
    <VImg class="auth-footer-mask d-none d-md-block" :src="authThemeMask" />
  </div>
</template>

<style lang="scss" scoped>
@use "@core/scss/template/pages/page-auth";
</style>
