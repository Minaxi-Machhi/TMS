<template>
    <v-dialog v-model="localDialogVisible" persistent width="400" :overlay="false" transition="dialog-transition">
        <v-card>
            <v-card-title class="px-6 py-2 d-flex align-center justify-space-between">
                <div class="d-flex align-center">
                    <v-icon size="x-small" :color="color" class="mr-3">mdi-alert</v-icon>
                    <span class="text-h5 text-capitalize">
                        Caution
                    </span>
                </div>
                <v-btn icon color="error" variant="plain" @click="closeDialog">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-card-title>


            <v-card-text class="text-black">
                Are you sure you want to perform this action?
            </v-card-text>

            <v-card-actions class="d-flex justify-end mb-3 mr-4">
                <v-btn color="#FF0000" variant="elevated" @click="confirm">Yes</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
// internal imports
import { onMounted, ref, watch } from 'vue';

// external imports


// props
const props = defineProps({
    dialogVisible: {
        type: Boolean,
        default: false
    },
    color: {
        type: String,
        default: 'black'
    },
});

// initialization of reactive data
const localDialogVisible = ref(props.dialogVisible);

// define emit
const emit = defineEmits(['close', 'confirm']);

// method to close the dialog
const closeDialog = () => {
    localDialogVisible.value = false;
    emit('close');
};

// handel the case when user clicks outside the modal
watch(localDialogVisible, (newVal) => {
    if (!newVal) {
        emit('close');
    }
});


// method to submit the effortlog form
const confirm = async () => {
    localDialogVisible.value = false;
    emit('confirm', true);
};

onMounted(() => {
})

</script>

<style scoped></style>
