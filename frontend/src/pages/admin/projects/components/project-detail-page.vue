<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { projectServices } from "@/services/project";
import loaderUtility from "@/utilities/loader/loader-utility";
import { toastUtility } from "@/utilities/toast-utility";
import { useRouter } from "vue-router";
import AddUserInProjectDialog from "./add-user-in-project-dialog.vue";

const route = useRouter();
const projectData = ref({});
const projectId = ref("");
const addUserInProjectDialogVisible = ref(false);

const getProjectDetail = async (id) => {
  try {
    loaderUtility.show();
    const { data } = await projectServices.getProjectDetail(id);
    projectData.value = data;
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
};

const addUser = () => {
  addUserInProjectDialogVisible.value = true;
};

const closeAddUserInProjectDialog = async () => {
  addUserInProjectDialogVisible.value = false;
  await getProjectDetail(projectId.value);
};

onMounted(async () => {
  projectId.value = route?.currentRoute?.value.params.id;
  projectId.value ? await getProjectDetail(projectId.value) : null;
});
</script>

<template>
  <div>
    <v-card>
      <v-card-title class="px-6 py-2 d-flex align-center justify-space-between">
        <v-row>
          <v-col cols="8"> {{ projectData.name }} </v-col>
          <v-col cols="4" class="d-flex justify-end">
            <v-btn size="x-small" class="rounded-lg" @click="addUser">
              Add User
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-row>
          <v-col cols="6"> Code: {{ projectData.code }} </v-col>
          <v-col cols="6"> Description: {{ projectData.description }} </v-col>
          <v-col cols="6">
            Members:
            <b>
              <span v-for="user in projectData.project_users" :key="user">{{
                user.username
              }}</span>
            </b>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <AddUserInProjectDialog
      v-if="addUserInProjectDialogVisible"
      :dialogVisible="addUserInProjectDialogVisible"
      :projectData="projectData"
      @close="closeAddUserInProjectDialog"
    >
    </AddUserInProjectDialog>
  </div>
</template>