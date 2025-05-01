<script setup>
// internal imports
import { onMounted, ref } from "vue";

// external imports
import { AgGridVue } from "ag-grid-vue3";

// service imports
import { userProfileServices } from "@/services/user-profile";

// utility imports
import { excelUtility } from "@/utilities/excel-utility";
import { gridUtility } from "@/utilities/grid-utility";
import { getColor, getProfileTypeColor, getRandomColor } from "@/utilities/helpers-utility";
import loaderUtility from "@/utilities/loader/loader-utility";
import { localStorageUtility } from "@/utilities/local-storage-utility";
import { toastUtility } from "@/utilities/toast-utility";

// component imports
import Pagination from "@/components/shared/Pagination.vue";
import AddEditUserDrawer from "./components/add-edit-user-drawer.vue";

// store import (state management)
import { useUsersStore } from "./useUsersStore";
import FilterManager from "./components/filter-manager.vue";


// varibales initialization
const usersStore = useUsersStore();
const gridApi = ref(null);
const itemsPerPage = ref(10);
const selectedUsers = ref([]);
const userList = ref([]);
const totalRecords = ref(0);
const currentUserId = ref(null);
const speedDial = ref(false);
const drawer = ref(false);

watch(drawer, (newVal) => {
  if (!newVal) {
    currentUserId.value = null;
  }
});

const columnDefs = ref([
  {
    colId: "Initials",
    headerName: "",
    field: "full_name",
    sortable: false,
    cellRendererParams: (params) => {
      let initials = params.value.split(" ").map(word => word[0]).join("");
      return {
        initials: initials,
        bgColor: getRandomColor(),
      }
    },
    cellRenderer: gridUtility.createAvatarCell(),
    minWidth: 65,
    width: 65,
  },
  {
    colId: "full_name",
    headerName: "Name",
    field: "full_name",
    sortable: true,
    sort: 'asc',
    headerTooltip: "Name",
    tooltipField: "full_name",
    minWidth: 400,
  },
  {
    colId: "username",
    headerName: "Username",
    field: "username",
    sortable: true,
    headerTooltip: "Username",
    tooltipField: "username",
  },
  {
    colId: "email",
    headerName: "Email",
    field: "email",
    sortable: false,
    headerTooltip: "Email",
    tooltipField: "email",
  },
  {
    colId: "profile_type",
    headerName: "Type",
    field: "profile_type",
    sortable: false,
    cellRendererParams: (params) => {
      return {
        value: params.value.replaceAll("_", " "),
        color: getProfileTypeColor(params.value),
      }
    },
    cellRenderer: gridUtility.createChipCell(),
  },
  {
    colId: "contact_number",
    headerName: "Contact No.",
    field: "contact_number",
    sortable: false,
    headerTooltip: "Contact Number",
    tooltipField: "contact_number",
  }
]);

const defaultColDef = ref({
  filter: false,
  sortable: false,
  resizable: false,
  flex: 1,
  minWidth: 150,
  icons: {
    sortAscending: `<i class="ri-sort-alphabet-asc mt-1" style="color: green; font-size: 14px;"></i>`,
    sortDescending: `<i class="ri-sort-alphabet-desc mt-1" style="color: red; font-size: 14px;"></i>`
  },
  suppressMovable: true
});

const gridOptions = ref({
  animateRows: true,
});

//============================================== Filter section ============================================
const userFilters = ref({
  limit: 10,
  offset: 0,
  // search: null, (if you provide search in filter manager than do not write it here.)
  // ordering: null (This field will set dynamically based on coldefs)
});

// method for filteration perpose
const applyFilter = async () => {
  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage('user-list-filter-manager');
  userFilters.value = { ...userFilters.value, ...filtersFromLocalStorage, offset: 0 };
  await getUserProfileList(userFilters.value);
}

// method to set column visible of the grid
const setGridColumnVisible = (colId, shouldShow) => {
  gridApi.value.setColumnsVisible([colId], shouldShow);
  localStorageUtility.setItemToLocalStorage('user-list-state', gridApi.value.getColumnState());
}


// method to reorder columns of the grid
const reorderColumns = () => {
  const savedState = localStorageUtility.getItemFromLocalStorage('user-list-state');
  gridApi.value.applyColumnState({ state: savedState, applyOrder: true, });

}

const handleSearch = () => {
  let timer;
  clearTimeout(timer);
  timer = setTimeout(async () => {
    await getUserProfileList(userFilters.value);
  }, 1000);
}

// method to export data to excel
const onExport = async () => {
  loaderUtility.show();
  let date = new Date().toISOString().split("T")[0];
  let columns;
  let filename = null;
  columns = [
    { displayKey: 'Name', valueKey: 'full_name' },
    { displayKey: 'Username', valueKey: 'username' },
    { displayKey: 'Email', valueKey: 'email' },
    { displayKey: 'Type', valueKey: 'profile_type' },
    { displayKey: 'Contact Number', valueKey: 'contact_number' },
  ];
  filename = `users_${date}.xlsx`;
  excelUtility.export(columns, userList.value, filename);
  loaderUtility.hide();
}

// method to handle the row click of the grid
const handleRowClicked = (params) => {
  currentUserId.value = params.data.id;
  drawer.value = true;
}

// method to handle paginition.
const handlePagination = async ({ page, itemsPerPage }) => {
  userFilters.value.limit = itemsPerPage;
  userFilters.value.offset = (page - 1) * itemsPerPage;
  const filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage("user-list-filter-manager");
  localStorageUtility.setItemToLocalStorage("user-list-filter-manager", { ...filtersFromLocalStorage, ...userFilters.value });
  await getUserProfileList(userFilters.value);
}

// method to fetch the order list
const getUserProfileList = async (params) => {
  params = { ...params };
  try {
    loaderUtility.show();
    const { data } = await userProfileServices.getUserProfileList(params);
    userList.value = data.results;
    totalRecords.value = data.count;
  } catch (error) {
    toastUtility.showError(error);
  } finally {
    loaderUtility.hide();
  }
};

// method for sorting perpose
const handleSorting = async (params) => {

  userList.value = [];

  const state = params.api.getState();
  if (!state.sort) {
    userFilters.value.ordering = null;
  } else {
    let sortModelObject = state.sort.sortModel[0];
    if (sortModelObject.sort === 'asc') {
      userFilters.value.ordering = sortModelObject.colId;
    } else if ((sortModelObject.sort === 'desc')) {
      userFilters.value.ordering = "-" + sortModelObject.colId;
    }
  }

  // Save the grid state in local storage
  localStorageUtility.setItemToLocalStorage('user-list-state', params.api.getColumnState());

  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage('user-list-filter-manager');
  userFilters.value = { ...filtersFromLocalStorage, ...userFilters.value, offset: 0 };
  localStorageUtility.setItemToLocalStorage('user-list-filter-manager', userFilters.value);
  await getUserProfileList(userFilters.value);
}

const handleGridReady = async (params) => {
  gridApi.value = params.api;
  const currentState = params.api.getColumnState();
  const savedState = localStorageUtility.getItemFromLocalStorage('user-list-state');
  if (savedState) {
    if (JSON.stringify(currentState) !== JSON.stringify(savedState)) {
      params.api.applyColumnState({ state: savedState });
    } else {
      await handleSorting(params);
    }
  } else if (params.api.getState().sort) {
    await handleSorting(params);
  } else {
    localStorageUtility.setItemToLocalStorage('user-list-state', params.api.getColumnState());
    await getUserProfileList(userFilters.value);
  }
};

onMounted(async () => {
  let filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage('user-list-filter-manager');
  if (filtersFromLocalStorage) {
    userFilters.value = { ...userFilters.value, ...filtersFromLocalStorage, };
  } else {
    localStorageUtility.setItemToLocalStorage('user-list-filter-manager', userFilters.value);
  }
});

</script>

<template>

  <v-navigation-drawer v-model="drawer" :width="600" location="right" temporary class="rounded-s-lg">
    <AddEditUserDrawer v-if="drawer" :id="currentUserId"
      @close="async () => { drawer = false, await getUserProfileList(userFilters.value); }">
    </AddEditUserDrawer>
  </v-navigation-drawer>

  <v-row>
    <v-col class="d-flex align-center justify-end ga-3" style="margin-left: 9.375rem;">
      <v-btn variant="tonal" density="compact" :color="getColor('red')">
        <v-icon size="15" class="px-3">ri-swap-2-fill</v-icon>
        <v-speed-dial v-model="speedDial" location="bottom center" transition="slide-x-reverse-transition"
          activator="parent">
          <v-btn key="1" color="warning" icon size="x-small">
            <v-icon size="20">mdi-pencil</v-icon>
            <v-tooltip activator="parent" location="left">Bulk Update</v-tooltip>
          </v-btn>
          <v-btn key="2" color="error" icon size="x-small">
            <v-icon size="20">mdi-plus</v-icon>
            <v-tooltip activator="parent" location="left">Bulk Create</v-tooltip>
          </v-btn>
        </v-speed-dial>
        <v-tooltip activator="parent" location="top">Bulk Actions</v-tooltip>
      </v-btn>

      <v-btn class="text-uppercase d-flex align-center" density="compact" variant="tonal"
        @click="currentUserId = null; drawer = true">
        <v-icon size="12">
          ri-add-fill
        </v-icon>
        <v-icon size="14">
          ri-user-fill
        </v-icon>
        <v-tooltip activator="parent" location="top">Add User</v-tooltip>
      </v-btn>

    </v-col>
    <v-col cols="12">
      <FilterManager @applyFilter="applyFilter" @setGridColumnVisible="setGridColumnVisible"
        @reorderColumns="reorderColumns"></FilterManager>
    </v-col>
  </v-row>

  <v-card class="mt-4">

    <v-card-text>
      <ag-grid-vue style="width: 100%; height: 55vh;" :rowHeight="40" :rowData="userList" :columnDefs="columnDefs"
        :defaultColDef="defaultColDef" :gridOptions="gridOptions" :tooltipShowDelay="500" :tooltipMouseTrack="true"
        :autoSizeStrategy="{ type: 'fitGridWidth' }" @gridReady="handleGridReady" @sortChanged="handleSorting"
        @rowClicked="handleRowClicked" />
    </v-card-text>


    <v-card-actions class="mb-3">
      <v-row class="d-flex align-center justify-end">

        <v-col cols="6" class="d-flex align-center pl-10">
          <!-- <v-text-field prepend-inner-icon="mdi-magnify" v-model="orderFilters.search" label="Search" density="compact"
            variant="outlined" @input="handleSearch"></v-text-field> -->

          <v-btn @click="onExport" color="grey" class="text-uppercase" density="compact" variant="tonal" size="small"
            prepend-icon="ri-upload-2-line">
            Export
          </v-btn>
        </v-col>

        <v-col cols="6">
          <Pagination :total-items="totalRecords" :items-per-page="itemsPerPage" @update-pagination="handlePagination">
          </Pagination>
        </v-col>

      </v-row>
    </v-card-actions>
  </v-card>
</template>

<style></style>
