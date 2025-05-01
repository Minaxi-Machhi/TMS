<template>

    <v-row style="position: relative;">

        <div class="d-flex align-center ga-2 px-3" style="position: absolute; top:-41px">
            <v-menu>
                <template v-slot:activator="{ props }">
                    <v-btn class="rounded" v-bind="props" :color="getColor('pink')" size="x-small"
                        @click.stop="getSavedState">
                        <v-icon color="white">ri-table-view</v-icon>
                        <v-tooltip activator="parent">Grid Configurations</v-tooltip>
                    </v-btn>
                </template>

                <v-list class="mt-1 border" style="max-height: 50vh; overflow-y: auto;">
                    <draggable v-model="savedState" item-key="colId" handle=".drag-handle" @end="reorderColumns"
                        :animation="200" ghost-class="drag-ghost" chosen-class="drag-chosen">
                        <template #item="{ element: col, index }">
                            <v-list-item v-if="!['ag-Grid-SelectionColumn'].includes(col.colId)"
                                style="min-height: unset" @click.stop>
                                <v-list-item-title>
                                    <div class="d-flex">
                                        <span class="d-flex align-center justify-space-betweeen w-100">
                                            <v-checkbox :false-value="false" :true-value="true" :model-value="!col.hide"
                                                @change="savedState[index].hide = !savedState[index].hide, toggleColumnVisibility(col.colId, !savedState[index].hide)"></v-checkbox>
                                            <span class="font-weight-light ml-1 text-capitalize"
                                                style="font-size: small;">
                                                {{ col.colId.replaceAll('_', ' ') }}
                                            </span>
                                        </span>
                                        <span class="d-flex align-center">
                                            <v-icon class="mr-2 drag-handle" size="small"
                                                color="grey darken-1">mdi-drag</v-icon>
                                        </span>
                                    </div>
                                </v-list-item-title>
                            </v-list-item>
                        </template>
                    </draggable>
                </v-list>
            </v-menu>

            <v-menu>
                <template v-slot:activator="{ props }">
                    <v-btn class="rounded" v-bind="props" :color="getColor('blue')" size="x-small">
                        <v-icon color="white">
                            mdi-cogs
                        </v-icon>
                        <v-tooltip activator="parent">Filters Configuration</v-tooltip>
                    </v-btn>
                </template>

                <v-list class="mt-1 border" style="max-height: 50vh; min-height: auto; overflow-y: auto;">
                    <template v-for="(config, key) in filterManagerConfig" :key="key">
                        <v-list-item style="min-height: unset" v-if="!['limit', 'offset'].includes(key)" @click.stop>
                            <v-list-item-title>
                                <div class="d-flex align-center">
                                    <v-checkbox v-model="visibilityList" :value="key"></v-checkbox>
                                    <span class="font-weight-light mr-2 ml-1" style="font-size:small;">{{
                                        config.label
                                        }}</span>
                                </div>
                            </v-list-item-title>
                        </v-list-item>
                    </template>
                </v-list>
            </v-menu>

            <v-btn class="rounded" icon size="x-small" :color="getColor('orange')" @click="dialog = true"
                :disabled="visibilityList.length === Object.keys(filterManagerConfig).length">
                <v-icon size="14" color="white">
                    mdi-filter-plus
                </v-icon>
                <v-tooltip activator="parent">More Filters</v-tooltip>
            </v-btn>

            <v-badge dot v-model="hasActiveFilters" :color="getColor('red')">
                <v-btn class="rounded" icon size="x-small" :color="getColor('black')" @click="resetFilters"
                    :disabled="!hasActiveFilters">
                    <v-icon size="15" color="white">
                        mdi-filter-off
                    </v-icon>
                    <v-tooltip activator="parent">Reset Filters</v-tooltip>
                </v-btn>
            </v-badge>
        </div>

        <!-- Visible Filters -->
        <template v-for="(config, key) in filterManagerConfig" :key="key">
            <v-col v-if="visibilityList.includes(key)" :cols="columnsLength">

                <!-- v-autocomplete -->
                <v-autocomplete v-if="config.type === 'v-autocomplete'" class="text-capitalize" density="compact"
                    v-model="filterManager[key]" :label="config.label" :items="config.items || []"
                    :item-title="config.itemTitle" :item-value="config.itemValue" @update:model-value="applyFilter"
                    :prepend-inner-icon="config.icon || ''" clearable />

                <!-- InputField -->
                <InputField v-else-if="config.type === 'InputField'" v-model="filterManager[key]" :label="config.label"
                    @update:modelValue="debouncedApplyFilter" :prepend-inner-icon="config.icon || ''" clearable />

                <!-- DatePicker -->
                <DatePicker v-else-if="config.type === 'DatePicker'" v-model="filterManager[key]" :label="config.label"
                    @update:modelValue="applyFilter" />

                <!-- DateRangePicker -->
                <DateRangePicker v-else-if="config.type === 'DateRangePicker'" v-model="filterManager[key]"
                    :placeholder="config.label" @update:modelValue="applyFilter" @input.stop @focus.stop @blur.stop />

            </v-col>
        </template>

    </v-row>

    <!-- Hidden Filters in Dialog -->
    <v-dialog v-if="dialog" v-model="dialog" max-width="600px" persistent :overlay="false"
        transition="dialog-transition">
        <v-card>
            <v-card-title class="px-6 py-2 d-flex align-center justify-space-between">
                <div class="d-flex align-center">
                    <v-icon size="x-small" :color="getColor('orange')" class="mr-3">mdi-filter-plus</v-icon>
                    <span class="text-h5 text-capitalize">
                        More Filters
                    </span>
                </div>
                <v-btn icon color="error" variant="plain" @click="dialog = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-card-title>
            <v-card-text class="my-2">
                <v-row>
                    <template v-for="(config, key) in filterManagerConfig" :key="key">
                        <v-col v-if="!visibilityList.includes(key) && !['limit', 'offset'].includes(key)" cols="12"
                            md="6" lg="6">
                            <!-- v-autocomplete -->
                            <v-autocomplete v-if="config.type === 'v-autocomplete'" v-model="filterManager[key]"
                                :label="config.label" :items="config.items || []" :item-title="config.itemTitle"
                                :item-value="config.itemValue" density="compact" variant="outlined"
                                :prepend-inner-icon="config.icon || ''" clearable />

                            <!-- InputField -->
                            <InputField v-else-if="config.type === 'InputField'" v-model="filterManager[key]"
                                :label="config.label" density="compact" :prepend-inner-icon="config.icon || ''"
                                clearable />

                            <!-- DatePicker -->
                            <DatePicker v-else-if="config.type === 'DatePicker'" v-model="filterManager[key]"
                                :label="config.label" />

                            <!-- DateRangePicker -->
                            <DateRangePicker v-else-if="config.type === 'DateRangePicker'" v-model="filterManager[key]"
                                :placeholder="config.label" />
                        </v-col>
                    </template>
                </v-row>
            </v-card-text>
            <v-card-actions class="mr-4 mb-1">
                <v-btn color="success" variant="elevated" @click="applyFilter">Apply</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

</template>

<script setup>
import { profileTypeChoices } from "@/utilities/choice-filter-utility";
import { getColor } from "@/utilities/helpers-utility";
import { localStorageUtility } from "@/utilities/local-storage-utility";
import { debounce } from "@antfu/utils";
import { computed, onMounted, reactive, ref, watch } from "vue";
import draggable from 'vuedraggable';
import { useStorage } from '@vueuse/core';

const dialog = ref(false);
const columnsLength = ref(3);

// Define all possible filters
const filterManager = ref({
    search: null,
    profile_type: null,
});

const filterManagerConfig = reactive({
    search: { type: "InputField", label: "Search", icon: 'ri-search-2-line' },
    profile_type: { type: "v-autocomplete", label: "Type", items: profileTypeChoices, itemTitle: "key", itemValue: "value", icon: "" }
});

// Visibility list from local storage or default
const visibilityList = ref(localStorageUtility.getItemFromLocalStorage("user-filter-visibility-list") || ["search",]);

// grid state from the local storage.
const savedState = ref([]);

// define emit
const emit = defineEmits(['applyFilter', 'setGridColumnVisible', 'reorderColumns']);

const applyFilter = async () => {
    await new Promise(resolve => setTimeout(resolve, 500));
    emit('applyFilter');
    dialog.value = false;
}

// computed property to check for active filters
const hasActiveFilters = computed(() => {
    return !!(
        filterManager.value.search
    );
});

// debounce once and use that instance
const debouncedApplyFilter = debounce(500, applyFilter);

// method to get the saved state
const getSavedState = () => savedState.value = localStorageUtility.getItemFromLocalStorage('user-list-state');

// Reset filters
const resetFilters = async () => {
    filterManager.value.search = null;
    await new Promise(resolve => setTimeout(resolve, 500));
    emit('applyFilter');
}

// method to toggle clumn visibility
const toggleColumnVisibility = (colId, shouldShow) => {
    emit('setGridColumnVisible', colId, shouldShow);
}

// method to reorder columns
const reorderColumns = async () => {
    await new Promise(resolve => setTimeout(resolve, 300));
    emit('reorderColumns');
}

// Watch changes and persist in local storage
watch(visibilityList, (newList) => {
    localStorageUtility.setItemToLocalStorage("user-filter-visibility-list", newList);
}, { deep: true });

// Watch changes and persist in local storage
watch(savedState, (newList) => {
    localStorageUtility.setItemToLocalStorage("user-list-state", newList);
}, { deep: true });

watch(filterManager, (newFilters) => {
    const filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage("user-list-filter-manager");
    localStorageUtility.setItemToLocalStorage("user-list-filter-manager", { ...filtersFromLocalStorage, ...newFilters });
}, { deep: true });

// Load stored filters on mount
onMounted(async () => {
    const filtersFromLocalStorage = localStorageUtility.getItemFromLocalStorage("user-list-filter-manager");
    if (filtersFromLocalStorage) {
        filterManager.value = { ...filterManager.value, ...filtersFromLocalStorage };
    }
});

</script>
