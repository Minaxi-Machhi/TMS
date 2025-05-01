<template>
    <v-row class="d-flex align-center justify-end px-5">
        
        <!-- Items per page selection -->
        <v-col class="d-flex align-center justify-end" style="max-width: fit-content;">
            <span class="px-2">Items per page: </span>
            <v-select style="max-width: 100px;" v-model="localItemsPerPage" :items="itemsPerPageOptionsComputed"
                item-title="title" item-value="value" variant="outlined" density="compact" hide-details
                @update:model-value="updateItemsPerPage"></v-select>
        </v-col>

        <!-- Page info -->
        <v-col class="d-flex align-center" style="max-width: max-content;">
            {{ startItem }} - {{ endItem }} of {{ totalItems }}
        </v-col>

        <!-- Pagination Controls -->
        <v-col class="d-flex align-center" style="max-width: fit-content;">
            <v-btn icon variant="text" :disabled="localPage === 1" @click="goToFirstPage">
                <v-icon>mdi-page-first</v-icon>
            </v-btn>

            <v-btn icon variant="text" :disabled="localPage === 1" @click="prevPage">
                <v-icon>mdi-chevron-left</v-icon>
            </v-btn>

            <v-btn icon variant="text" :disabled="localPage === totalPages" @click="nextPage">
                <v-icon>mdi-chevron-right</v-icon>
            </v-btn>

            <v-btn icon variant="text" :disabled="localPage === totalPages" @click="goToLastPage">
                <v-icon>mdi-page-last</v-icon>
            </v-btn>
        </v-col>
    </v-row>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

// Props
const props = defineProps({
    totalItems: { type: Number, required: true },
    itemsPerPage: { type: Number, default: 10 },
    itemsPerPageOptions: {
        type: Array,
        default: null
    }
})

// Emits
const emit = defineEmits(['update-pagination'])

// Local state
const localItemsPerPage = ref(props.itemsPerPage);
const localPage = ref(1);

// Computed properties
const totalPages = computed(() => Math.ceil(props.totalItems / localItemsPerPage.value));
const startItem = computed(() => (localPage.value - 1) * localItemsPerPage.value + 1);
const endItem = computed(() => Math.min(localPage.value * localItemsPerPage.value, props.totalItems));

// Compute options dynamically, adding "All" if applicable
const itemsPerPageOptionsComputed = computed(() => {
    const defaultOptions = props.itemsPerPageOptions ?? [
        { title: '10', value: 10 },
        { title: '25', value: 25 },
        { title: '50', value: 50 },
        { title: '100', value: 100 }
    ];
    return defaultOptions;
});

// Emit the pagination event
const emitPagination = () => {
    emit('update-pagination', { page: localPage.value, itemsPerPage: localItemsPerPage.value });
};

// Methods
const prevPage = () => {
    if (localPage.value > 1) {
        localPage.value--;
        emitPagination();
    }
};

const nextPage = () => {
    if (localPage.value < totalPages.value) {
        localPage.value++;
        emitPagination();
    }
};

const goToFirstPage = () => {
    localPage.value = 1;
    emitPagination();
};

const goToLastPage = () => {
    localPage.value = totalPages.value;
    emitPagination();
};

const updateItemsPerPage = (value) => {
    localItemsPerPage.value = value;
    localPage.value = 1; // Reset to first page
    emitPagination();
};

</script>
