<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { projectServices } from "@/services/project";
import { taskServices } from "@/services/task";
import loaderUtility from "@/utilities/loader/loader-utility";
import { toastUtility } from "@/utilities/toast-utility";
import { useRouter } from "vue-router";
import AddUserInProjectDialog from "./add-user-in-project-dialog.vue";

const route = useRouter();
const projectData = ref({});
const projectId = ref("");
const addUserInProjectDialogVisible = ref(false);
const bucketList = ref([]);
const showTextField = ref(false);
const bucket_name = ref("");
const taskList = ref([]);

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
const getBucketList = async (id) => {
  try {
    loaderUtility.show();
    const { data } = await projectServices.getBucketList({
      project: id,
      limit: "all",
    });
    if (data && data.results) {
      bucketList.value = data.results;
    }
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
};

const addBucket = async () => {
  try {
    loaderUtility.show();
    let payload = { project: projectId.value, name: bucket_name.value };
    const res = await projectServices.createBucket(payload);
    showTextField.value = false;
    bucket_name.value = null;
    toastUtility.showSuccess(`Bucket has been added successfully.`);
    getBucketList(projectId.value);
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
};

const getTaskList = async (id) => {
  try {
    loaderUtility.show();
    const { data } = await taskServices.getTaskList({
      project: id,
      limit: "all",
    });
    if (data && data.results) {
      taskList.value = data.results;
    }
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

const addTask = (bucketId) => {
  console.log("bucketId", bucketId);
};

onMounted(async () => {
  projectId.value = route?.currentRoute?.value.params.id;
  projectId.value ? await getProjectDetail(projectId.value) : null;
  await getBucketList(projectId.value);
  await getTaskList(projectId.value);
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
      <v-divider></v-divider>
      <v-card-text>
        <v-row class="ma-0">
          <v-col
            cols="2"
            v-for="bucket in bucketList.reverse()"
            :key="bucket.id"
            class="mr-4"
          >
            <h4 class="mb-2">{{ bucket.name }}</h4>
            <v-card @click="addTask(bucket.id)">
              <v-card-text class="pa-2 text-primary">
                <v-icon>mdi-plus</v-icon> Add Task
              </v-card-text>
            </v-card>
            <div
              v-for="task in taskList.filter((t) => t.bucket == bucket.id)"
              :key="task.id"
              class="mt-4"
            >
              <v-card>
                <v-card-text class="pa-1">
                  <v-chip label color="primary" size="x-small">
                    {{ task.project }} </v-chip
                  ><br />
                  <span class="ml-2">{{ task.title }}</span
                  ><br />
                  <span class="text-body-2 ml-2">{{ task.description }}</span>
                </v-card-text>
                <v-divider></v-divider>
                <span class="text-caption ml-3">
                  <v-icon size="small">mdi-calendar</v-icon>
                  {{ task.due_date }}
                </span>
              </v-card>
            </div>
          </v-col>
          <v-col cols="2">
            <v-text-field
              v-if="showTextField"
              hide-details="auto"
              flat
              density="compact"
              v-model="bucket_name"
              label="Bucket Name"
              @keypress.enter="addBucket"
              @blur="
                !bucket_name ? (showTextField = false) : (showTextField = true)
              "
            >
            </v-text-field>
            <h4
              v-else
              class="mb-2"
              role="button"
              tabindex="0"
              @click="showTextField = true"
            >
              Add a new bucket
            </h4>
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