<template>
  <v-dialog
    v-model="localDialogVisible"
    persistent
    width="500"
    :overlay="false"
    transition="dialog-transition"
  >
    <v-card>
      <v-card-title class="px-6 py-2 d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon size="x-small" :color="color" class="mr-3"
            >ri-projector-line</v-icon
          >
          <span class="text-h5 text-capitalize"> Invite User </span>
        </div>
        <v-btn icon color="error" variant="plain" @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <div class="v-container pa-1 my-2 pb-0">
          <v-row>
            <v-col cols="12">
              <v-autocomplete
                outlined
                v-model="addUserInProjectForm.user"
                :items="userList"
                density="compact"
                label="User *"
                item-title="username"
                item-value="id"
                @blur="v$.user.$validate"
                :error-messages="v$.user.$errors.map((e) => e.$message)"
                @input="v$.user.$reset"
                @focus="v$.user.$reset"
                clear-on-select
              >
              </v-autocomplete>
            </v-col>
          </v-row>
        </div>
      </v-card-text>

      <v-card-actions class="d-flex justify-end mb-3 mr-4">
        <v-btn color="error" variant="outlined" @click="resetForm">Reset</v-btn>
        <v-btn color="success" variant="elevated" @click="submitForm"
          >Submit</v-btn
        >
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
import { required } from "@vuelidate/validators";

// props
const props = defineProps({
  id: {
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

const addUserInProjectForm = reactive({
  user: null,
});

const rules = reactive({
  user: { required },
});

// vuelidate instance to bind form fields and validation rules
const v$ = useVuelidate(rules, addUserInProjectForm);

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
  addUserInProjectForm.user = null;
  await v$.value.$reset();
};

// method to fetch project detail
const getUserProfileList = async (params = {}) => {
  try {
    loaderUtility.show();
    params = { user_type: "Team Member" };
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
  const isValidate = await v$.value.$validate();
  if (!isValidate) {
    toastUtility.showError("Please correct all the errors to submit the form!");
    return;
  }
  try {
    loaderUtility.show();
    if (props.id) {
      const res = await projectServices.addUserInProject(
        props.id,
        addUserInProjectForm
      );
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
