<template>
  <v-dialog
    v-model="localDialogVisible"
    persistent
    width="700"
    :overlay="false"
    transition="dialog-transition"
  >
    <v-card>
      <v-card-title class="px-6 py-2 d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon size="x-small" :color="color" class="mr-3">
            ri-projector-line
          </v-icon>
          <span class="text-h5 text-capitalize"> Invite User </span>
        </div>
        <v-btn icon color="error" variant="plain" @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <!-- <v-card-text class="px-6 py-2 d-flex align-center justify-space-between">
        Your Group :Name
      </v-card-text> -->

      <v-card-text>
        <div class="v-container pa-1 my-2 pb-0">
          <v-row class="d-flex">
            <v-col cols="10">
              <v-combobox
                variant="outlined"
                density="compact"
                id="add-user"
                name="add-user"
                v-model="users"
                item-title="username"
                item-value="id"
                :items="userList"
                label="Add User"
                chips
                multiple
                closable-chips
              />
            </v-col>
            <v-col cols="auto">
              <v-btn color="success" variant="elevated" @click="submitForm">
                Invite
              </v-btn>
            </v-col>
          </v-row>
        </div>
      </v-card-text>
      <v-row class="ma-0">
        <!-- <v-col class="ml-3">Members(1)</v-col> -->
      </v-row>

      <v-card-actions class="d-flex justify-end mb-3 mr-4">
        <!-- <v-btn color="error" variant="outlined" @click="resetForm">Reset</v-btn> -->
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
// internal imports
import { onMounted, reactive, ref, watch } from "vue";

// external imports
import { projectServices } from "@/services/project";
import { userProfileServices } from "@/services/user-profile";
import loaderUtility from "@/utilities/loader/loader-utility";
import { toastUtility } from "@/utilities/toast-utility";
import useVuelidate from "@vuelidate/core";

// props
const props = defineProps({
  projectData: {
    // type: [Number, null],
    required: true,
  },
  dialogVisible: {
    type: Boolean,
    default: false,
  },
  color: {
    type: String,
    default: "black",
  },
});

// initialization of reactive data
const localDialogVisible = ref(props.dialogVisible);
const userList = ref([]);
const users = ref([]);

// define emit
const emit = defineEmits(["close"]);

// method to close the dialog
const closeDialog = () => {
  localDialogVisible.value = false;
  emit("close");
};

// handel the case when user clicks outside the modal
watch(localDialogVisible, (newVal) => {
  if (!newVal) {
    emit("close");
  }
});

// method to reset the project form
const resetForm = async () => {
  users.value = [];
  await v$.value.$reset();
};

// method to fetch project detail
const getUserProfileList = async (params = {}) => {
  try {
    loaderUtility.show();
    params = { user_type: "Team Member", project: props.projectData.id };
    const { data } = await userProfileServices.getUserProfileList(params);
    userList.value = data.results;
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
};

// method to submit the project form
const submitForm = async () => {
  try {
    loaderUtility.show();
    if (props.projectData.id) {
      let userIds = users.value.map((u) => u.id);
      const res = await projectServices.addUserInProject(props.projectData.id, {
        user: userIds.join(""),
      });
      toastUtility.showSuccess(`User has been added in Project successfully.`);
    }
    closeDialog();
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
};

onMounted(() => {
  getUserProfileList();
});
</script>

<style scoped></style>
