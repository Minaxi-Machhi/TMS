<script setup>
import { authenticationService } from '@/services/authentication';
import avatar1 from '@images/avatars/avatar-1.png';
import ChangePasswordDialog from './change-password-dialog.vue';

// props
const props = defineProps({
  userData: {
    type: Object,
    required: true
  },
});

const changePasswordDialogVisible = ref(false);

const closeChangePasswordDialog = async () => {
  changePasswordDialogVisible.value = false;
};

const logout = () => {
  authenticationService.logout();
}


</script>

<template>
  <VBadge dot location="bottom right" offset-x="3" offset-y="3" color="success" bordered>
    <VAvatar class="cursor-pointer" color="primary" variant="tonal">
      <VImg :src="avatar1" />

      <!-- SECTION Menu -->
      <VMenu activator="parent" width="230" location="bottom end" offset="14px">
        <VList>
          <!-- 👉 User Avatar & Name -->
          <VListItem>
            <template #prepend>
              <VListItemAction start>
                <VBadge dot location="bottom right" offset-x="3" offset-y="3" color="success">
                  <VAvatar color="primary" variant="tonal">
                    <VImg :src="avatar1" />
                  </VAvatar>
                </VBadge>
              </VListItemAction>
            </template>

            <VListItemTitle class="font-weight-semibold">
              {{ props.userData?.full_name }}
            </VListItemTitle>
            <VListItemSubtitle>{{ props.userData?.username }}</VListItemSubtitle>
          </VListItem>
          <VDivider class="my-2" />

          <!-- 👉 Profile -->
          <VListItem link @click="changePasswordDialogVisible = true">
            <template #prepend>
              <VIcon class="me-2" icon="ri-key-line" size="22" />
            </template>

            <VListItemTitle>Change Password</VListItemTitle>
          </VListItem>

          <!-- 👉 Settings -->
          <!-- <VListItem link>
            <template #prepend>
              <VIcon class="me-2" icon="ri-settings-4-line" size="22" />
            </template>

            <VListItemTitle>Settings</VListItemTitle>
          </VListItem> -->

          <!-- 👉 Pricing -->
          <!-- <VListItem link>
            <template #prepend>
              <VIcon
                class="me-2"
                icon="ri-money-dollar-circle-line"
                size="22"
              />
            </template>

            <VListItemTitle>Pricing</VListItemTitle>
          </VListItem> -->

          <!-- 👉 FAQ -->
          <!-- <VListItem link>
            <template #prepend>
              <VIcon
                class="me-2"
                icon="ri-question-line"
                size="22"
              />
            </template>

            <VListItemTitle>FAQ</VListItemTitle>
          </VListItem> -->

          <!-- Divider -->
          <VDivider class="my-2" />

          <!-- 👉 Logout -->
          <VListItem @click.stop="logout">
            <template #prepend>
              <VIcon class="me-2" icon="ri-logout-box-r-line" size="22" />
            </template>

            <VListItemTitle>Logout</VListItemTitle>
          </VListItem>
        </VList>
      </VMenu>
      <!-- !SECTION -->
    </VAvatar>
  </VBadge>

  <!-- dialog -->
  <ChangePasswordDialog v-if="changePasswordDialogVisible" :dialogVisible="changePasswordDialogVisible"
    @close="closeChangePasswordDialog">
  </ChangePasswordDialog>
</template>
