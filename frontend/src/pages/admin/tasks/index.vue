<script setup>
// internal imports
import { onMounted, ref } from "vue";

// external imports
import { AgGridVue } from "ag-grid-vue3";

// service imports
import { taskServices } from "@/services/task";

// utility imports
import { excelUtility } from "@/utilities/excel-utility";
import { getColor } from "@/utilities/helpers-utility";
import loaderUtility from "@/utilities/loader/loader-utility";
import { localStorageUtility } from "@/utilities/local-storage-utility";
import { toastUtility } from "@/utilities/toast-utility";

// component imports
import Pagination from "@/components/shared/Pagination.vue";
import AddEditTaskDialog from "./components/add-edit-task-dialog.vue";
import FilterManager from "./components/filter-manager.vue";
import { useRouter } from "vue-router";

const router = useRouter();

// varibales initialization
const gridApi = ref(null);
const itemsPerPage = ref(10);
const taskList = ref([]);
const totalRecords = ref(0);
const currentTaskId = ref(null);
const speedDial = ref(false);

const columnDefs = ref([
  {
    colId: "title",
    headerName: "Task Title",
    field: "title",
    tooltipField: "code",
  },
  {
    colId: "description",
    headerName: "Description",
    field: "description",
  },
  {
    colId: "project",
    headerName: "Project Name",
    field: "project",
  },
  {
    colId: "due_date",
    headerName: "Due Date",
    field: "due_date",
  },
  {
    colId: "priority",
    headerName: "Priority",
    field: "priority",
  },
  {
    colId: "status",
    headerName: "Status",
    field: "status",
  },
  {
    colId: "created_at",
    headerName: "Created",
    field: "created_at",
  },
]);

const defaultColDef = ref({
  filter: false,
  sortable: false,
  resizable: false,
  flex: 1,
  minWidth: 150,
  icons: {
    sortAscending: `<i class="ri-sort-alphabet-asc mt-1" style="color: green; font-size: 14px;"></i>`,
    sortDescending: `<i class="ri-sort-alphabet-desc mt-1" style="color: red; font-size: 14px;"></i>`,
  },
  suppressMovable: true,
});

const gridOptions = ref({
  animateRows: true,
});

//============================================== Filter section ============================================
const taskFilters = ref({
  limit: 10,
  offset: 0,
  // search: null, (if you provide search in filter manager than do not write it here.)
  // ordering: null (This field will set dynamically based on coldefs)
});

// method for filteration perpose
const applyFilter = async () => {
  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage(
    "task-list-filter-manager"
  );
  taskFilters.value = {
    ...taskFilters.value,
    ...filtersFromLocalStorage,
    offset: 0,
  };
  await getTaskList(taskFilters.value);
};

// method to set column visible of the grid
const setGridColumnVisible = (colId, shouldShow) => {
  gridApi.value.setColumnsVisible([colId], shouldShow);
  localStorageUtility.setItemToLocalStorage(
    "task-list-state",
    gridApi.value.getColumnState()
  );
};

// method to reorder columns of the grid
const reorderColumns = () => {
  const savedState =
    localStorageUtility.getItemFromLocalStorage("task-list-state");
  gridApi.value.applyColumnState({ state: savedState, applyOrder: true });
};

const handleSearch = () => {
  let timer;
  clearTimeout(timer);
  timer = setTimeout(async () => {
    await getTaskList(taskFilters.value);
  }, 1000);
};

// method to export data to excel
const onExport = async () => {
  loaderUtility.show();
  let date = new Date().toISOString().split("T")[0];
  let columns;
  let filename = null;
  columns = [
    { displayKey: "Name", valueKey: "name" },
    { displayKey: "Project Id", valueKey: "project_id" },
    { displayKey: "Branch", valueKey: "branch_name" },
    { displayKey: "Default", valueKey: "default" },
    { displayKey: "Created", valueKey: "added_on" },
  ];
  filename = `tasks_${date}.xlsx`;
  excelUtility.export(columns, taskList.value, filename);
  loaderUtility.hide();
};

// ======================================== Add/Edit branch dialog ============================================

// method to handle the row click of the grid
const handleRowClicked = (params) => {
  // params.node.setSelected(true);
  currentTaskId.value = params.data.id;
  router.push({
    name: "task-detail",
    params: { id: currentTaskId.value },
  });
  // drawer.value = true;
};

// method to handle the checkbox selection of the grid
const handleSelectionChanged = (params) => {
  let selected = params.api.getSelectedRows();
  if (selected.length > 0) {
    currentTaskId.value = selected[0].id;
  }
};

// method to handle paginition.
const handlePagination = async ({ page, itemsPerPage }) => {
  taskFilters.value.limit = itemsPerPage;
  taskFilters.value.offset = (page - 1) * itemsPerPage;
  const filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage(
    "task-list-filter-manager"
  );
  localStorageUtility.setItemToLocalStorage("task-list-filter-manager", {
    ...filtersFromLocalStorage,
    ...taskFilters.value,
  });
  await getTaskList(taskFilters.value);
};

// method to fetch the order list
const getTaskList = async (params) => {
  params = { ...params };
  try {
    loaderUtility.show();
    const { data } = await taskServices.getTaskList(params);
    taskList.value = data.results;
    totalRecords.value = data.count;
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
};

// method for sorting perpose
const handleSorting = async (params) => {
  taskList.value = [];

  const state = params.api.getState();
  if (!state.sort) {
    taskFilters.value.ordering = null;
  } else {
    let sortModelObject = state.sort.sortModel[0];
    if (sortModelObject.sort === "asc") {
      taskFilters.value.ordering = sortModelObject.colId;
    } else if (sortModelObject.sort === "desc") {
      taskFilters.value.ordering = "-" + sortModelObject.colId;
    }
  }

  // Save the grid state in local storage
  localStorageUtility.setItemToLocalStorage(
    "task-list-state",
    params.api.getColumnState()
  );

  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage(
    "task-list-filter-manager"
  );
  taskFilters.value = {
    ...filtersFromLocalStorage,
    ...taskFilters.value,
    offset: 0,
  };
  localStorageUtility.setItemToLocalStorage(
    "task-list-filter-manager",
    taskFilters.value
  );
  await getTaskList(taskFilters.value);
};

const handleGridReady = async (params) => {
  gridApi.value = params.api;
  const currentState = params.api.getColumnState();
  const savedState =
    localStorageUtility.getItemFromLocalStorage("task-list-state");
  if (savedState) {
    if (JSON.stringify(currentState) !== JSON.stringify(savedState)) {
      params.api.applyColumnState({ state: savedState });
    } else {
      await handleSorting(params);
    }
  } else if (params.api.getState().sort) {
    await handleSorting(params);
  } else {
    localStorageUtility.setItemToLocalStorage(
      "task-list-state",
      params.api.getColumnState()
    );
    await getTaskList(taskFilters.value);
  }
};

onMounted(async () => {
  getTaskList();
  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage(
    "task-list-filter-manager"
  );
  if (filtersFromLocalStorage) {
    taskFilters.value = {
      ...taskFilters.value,
      ...filtersFromLocalStorage,
    };
  } else {
    localStorageUtility.setItemToLocalStorage(
      "task-list-filter-manager",
      taskFilters.value
    );
  }
});
</script>

<template>
  <v-row>
    <v-col
      class="d-flex align-center justify-end ga-3"
      style="margin-left: 9.375rem"
    >
      <v-btn
        class="text-uppercase d-flex align-center"
        density="compact"
        variant="tonal"
        disabled
      >
        <v-icon size="14"> ri-projector-fill </v-icon>
        <v-tooltip activator="parent" location="top">Add Task</v-tooltip>
      </v-btn>
    </v-col>
    <v-col cols="12">
      <FilterManager
        @applyFilter="applyFilter"
        @setGridColumnVisible="setGridColumnVisible"
        @reorderColumns="reorderColumns"
      ></FilterManager>
    </v-col>
  </v-row>

  <v-card class="mt-4">
    <v-card-text>
      <ag-grid-vue
        style="width: 100%; height: 55vh"
        :rowHeight="40"
        :rowData="taskList"
        :columnDefs="columnDefs"
        :defaultColDef="defaultColDef"
        :gridOptions="gridOptions"
        :tooltipShowDelay="500"
        :tooltipMouseTrack="true"
        :autoSizeStrategy="{ type: 'fitGridWidth' }"
        :rowSelection="{ mode: 'singleRow' }"
        :selectionColumnDef="{ pinned: true }"
        @gridReady="handleGridReady"
        @sortChanged="handleSorting"
        @rowClicked="handleRowClicked"
        @selectionChanged="handleSelectionChanged"
      />
    </v-card-text>

    <v-card-actions class="mb-3">
      <v-row class="d-flex align-center justify-end">
        <v-col cols="6" class="d-flex align-center pl-10">
          <!-- <v-text-field prepend-inner-icon="mdi-magnify" v-model="orderFilters.search" label="Search" density="compact"
            variant="outlined" @input="handleSearch"></v-text-field> -->

          <v-btn
            @click="onExport"
            color="grey"
            class="text-uppercase"
            density="compact"
            variant="tonal"
            size="small"
            prepend-icon="ri-upload-2-line"
          >
            Export
          </v-btn>
        </v-col>

        <v-col cols="6">
          <Pagination
            :total-items="totalRecords"
            :items-per-page="itemsPerPage"
            @update-pagination="handlePagination"
          >
          </Pagination>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<style></style>
