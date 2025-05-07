<script setup>
// internal imports
import { onMounted, ref } from "vue";

// external imports
import { AgGridVue } from "ag-grid-vue3";

// service imports
import { projectServices } from "@/services/project";

// utility imports
import { excelUtility } from "@/utilities/excel-utility";
import { getColor } from "@/utilities/helpers-utility";
import loaderUtility from "@/utilities/loader/loader-utility";
import { localStorageUtility } from "@/utilities/local-storage-utility";
import { toastUtility } from "@/utilities/toast-utility";

// component imports
import Pagination from "@/components/shared/Pagination.vue";
import AddEditProjectDialog from "./components/add-edit-project-dialog.vue";
import FilterManager from "./components/filter-manager.vue";
import { useRouter } from "vue-router";

const router = useRouter();

// varibales initialization
const gridApi = ref(null);
const itemsPerPage = ref(10);
const projectList = ref([]);
const totalRecords = ref(0);
const currentProjectId = ref(null);
const speedDial = ref(false);

const columnDefs = ref([
  {
    colId: "code",
    headerName: "Project Code",
    field: "code",
    tooltipField: "code",
  },
  {
    colId: "name",
    headerName: "Project Name",
    field: "name",
    tooltipField: "name",
  },
  {
    colId: "description",
    headerName: "Description",
    field: "description",
    tooltipField: "description",
  },
  {
    colId: "created_at",
    headerName: "Created",
    field: "created_at",
  },
  {
    colId: "owner_name",
    headerName: "Project Owner",
    field: "owner_name",
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
const projectFilters = ref({
  limit: 10,
  offset: 0,
  // search: null, (if you provide search in filter manager than do not write it here.)
  // ordering: null (This field will set dynamically based on coldefs)
});

// method for filteration perpose
const applyFilter = async () => {
  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage(
    "project-list-filter-manager"
  );
  projectFilters.value = {
    ...projectFilters.value,
    ...filtersFromLocalStorage,
    offset: 0,
  };
  await getProjectList(projectFilters.value);
};

// method to set column visible of the grid
const setGridColumnVisible = (colId, shouldShow) => {
  gridApi.value.setColumnsVisible([colId], shouldShow);
  localStorageUtility.setItemToLocalStorage(
    "project-list-state",
    gridApi.value.getColumnState()
  );
};

// method to reorder columns of the grid
const reorderColumns = () => {
  const savedState =
    localStorageUtility.getItemFromLocalStorage("project-list-state");
  gridApi.value.applyColumnState({ state: savedState, applyOrder: true });
};

const handleSearch = () => {
  let timer;
  clearTimeout(timer);
  timer = setTimeout(async () => {
    await getProjectList(projectFilters.value);
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
  filename = `projects_${date}.xlsx`;
  excelUtility.export(columns, projectList.value, filename);
  loaderUtility.hide();
};

// ======================================== Add/Edit branch dialog ============================================
const addEditProjectDialogVisible = ref(false);

const closeAddEditProjectDialog = async () => {
  addEditProjectDialogVisible.value = false;
  gridApi.value.deselectAll();
  await getProjectList(projectFilters.value);
};

// method to handle the row click of the grid
const handleRowClicked = (params) => {
  // params.node.setSelected(true);
  currentProjectId.value = params.data.id;
  router.push({
    name: "project-detail",
    params: { id: currentProjectId.value },
  });
  // drawer.value = true;
};

// method to handle the checkbox selection of the grid
const handleSelectionChanged = (params) => {
  let selected = params.api.getSelectedRows();
  if (selected.length > 0) {
    currentProjectId.value = selected[0].id;
    addEditProjectDialogVisible.value = true;
  }
};

// method to handle paginition.
const handlePagination = async ({ page, itemsPerPage }) => {
  projectFilters.value.limit = itemsPerPage;
  projectFilters.value.offset = (page - 1) * itemsPerPage;
  const filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage(
    "project-list-filter-manager"
  );
  localStorageUtility.setItemToLocalStorage("project-list-filter-manager", {
    ...filtersFromLocalStorage,
    ...projectFilters.value,
  });
  await getProjectList(projectFilters.value);
};

// method to fetch the order list
const getProjectList = async (params) => {
  params = { ...params };
  try {
    loaderUtility.show();
    const { data } = await projectServices.getProjectList(params);
    projectList.value = data.results;
    totalRecords.value = data.count;
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
};

// method for sorting perpose
const handleSorting = async (params) => {
  projectList.value = [];

  const state = params.api.getState();
  if (!state.sort) {
    projectFilters.value.ordering = null;
  } else {
    let sortModelObject = state.sort.sortModel[0];
    if (sortModelObject.sort === "asc") {
      projectFilters.value.ordering = sortModelObject.colId;
    } else if (sortModelObject.sort === "desc") {
      projectFilters.value.ordering = "-" + sortModelObject.colId;
    }
  }

  // Save the grid state in local storage
  localStorageUtility.setItemToLocalStorage(
    "project-list-state",
    params.api.getColumnState()
  );

  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage(
    "project-list-filter-manager"
  );
  projectFilters.value = {
    ...filtersFromLocalStorage,
    ...projectFilters.value,
    offset: 0,
  };
  localStorageUtility.setItemToLocalStorage(
    "project-list-filter-manager",
    projectFilters.value
  );
  await getProjectList(projectFilters.value);
};

const handleGridReady = async (params) => {
  gridApi.value = params.api;
  const currentState = params.api.getColumnState();
  const savedState =
    localStorageUtility.getItemFromLocalStorage("project-list-state");
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
      "project-list-state",
      params.api.getColumnState()
    );
    await getProjectList(projectFilters.value);
  }
};

onMounted(async () => {
  getProjectList();
  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage(
    "project-list-filter-manager"
  );
  if (filtersFromLocalStorage) {
    projectFilters.value = {
      ...projectFilters.value,
      ...filtersFromLocalStorage,
    };
  } else {
    localStorageUtility.setItemToLocalStorage(
      "project-list-filter-manager",
      projectFilters.value
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
      <v-btn variant="tonal" density="compact" :color="getColor('red')">
        <v-icon size="15" class="px-3">ri-swap-2-fill</v-icon>
        <v-speed-dial
          v-model="speedDial"
          location="bottom center"
          transition="slide-x-reverse-transition"
          activator="parent"
        >
          <v-btn key="1" color="warning" icon size="x-small">
            <v-icon size="20">mdi-pencil</v-icon>
            <v-tooltip activator="parent" location="left"
              >Bulk Update</v-tooltip
            >
          </v-btn>
          <v-btn key="2" color="error" icon size="x-small">
            <v-icon size="20">mdi-plus</v-icon>
            <v-tooltip activator="parent" location="left"
              >Bulk Create</v-tooltip
            >
          </v-btn>
        </v-speed-dial>
        <v-tooltip activator="parent" location="top">Bulk Actions</v-tooltip>
      </v-btn>

      <v-btn
        class="text-uppercase d-flex align-center"
        density="compact"
        variant="tonal"
        @click="
          currentProjectId = null;
          addEditProjectDialogVisible = true;
        "
      >
        <v-icon size="12" class="mr-1"> ri-add-fill </v-icon>
        <v-icon size="14"> ri-projector-fill </v-icon>
        <v-tooltip activator="parent" location="top">Add Project</v-tooltip>
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
        :rowData="projectList"
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

  <!-- dialogs -->
  <AddEditProjectDialog
    v-if="addEditProjectDialogVisible"
    :dialogVisible="addEditProjectDialogVisible"
    :id="currentProjectId"
    @close="closeAddEditProjectDialog"
  >
  </AddEditProjectDialog>
</template>

<style></style>
