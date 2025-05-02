<template>
    <v-dialog v-model="localDialogVisible" persistent width="600" :overlay="false" transition="dialog-transition">
        <v-card>
            <v-card-title class="px-6 py-2 d-flex align-center justify-space-between">
                <div class="d-flex align-center">
                    <v-icon size="x-small" :color="color" class="mr-3">ri-projector-line</v-icon>
                    <span class="text-h5 text-capitalize">
                        {{ props.id ? "Edit" : "Add" }} Project
                    </span>
                </div>
                <v-btn icon color="error" variant="plain" @click="closeDialog">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-card-title>

            <v-card-text>
                <div class="v-container pa-1 my-2 pb-0">
                    <v-row>
                        <v-col cols="6">
                            <v-autocomplete outlined v-model="addEditProjectForm.branch" :items="branchList"
                                density="compact" label="Branch *" item-title="name" item-value="id"
                                @blur="v$.branch.$validate" :error-messages="v$.branch.$errors.map(e => e.$message)"
                                @input="v$.branch.$reset" @focus="v$.branch.$reset" clear-on-select>
                            </v-autocomplete>
                        </v-col>
                        <v-col cols="6">
                            <InputField v-model="addEditProjectForm.name" label="Name *" @blur="v$.name.$validate"
                                :error-messages="v$.name.$errors.map(e => e.$message)" @input="v$.name.$reset"
                                @focus="v$.name.$reset">
                            </InputField>
                        </v-col>
                        <v-col cols="6">
                            <InputField v-model="addEditProjectForm.project_id" label="Project Id *"
                                @blur="v$.project_id.$validate"
                                :error-messages="v$.project_id.$errors.map(e => e.$message)"
                                @input="v$.project_id.$reset" @focus="v$.project_id.$reset">
                            </InputField>
                        </v-col>
                        <v-col cols="6">
                            <v-checkbox v-model="addEditProjectForm.default" label="Default">
                            </v-checkbox>
                        </v-col>
                    </v-row>
                </div>
            </v-card-text>

            <v-card-actions class="d-flex justify-end mb-3 mr-4">
                <v-btn color="error" variant="outlined" @click="resetForm">Reset</v-btn>
                <v-btn color="success" variant="elevated" @click="submitForm">Submit</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
// internal imports
import { onMounted, reactive, ref, watch } from 'vue';

// external imports
import { projectServices } from '@/services/project';
import loaderUtility from '@/utilities/loader/loader-utility';
import { toastUtility } from '@/utilities/toast-utility';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';


// props
const props = defineProps({
    id: {
        type: [Number, null],
        required: true
    },
    dialogVisible: {
        type: Boolean,
        default: false
    },
    color: {
        type: String,
        default: 'black'
    }
});

// initialization of reactive data
const localDialogVisible = ref(props.dialogVisible);
const branchList = ref([]);

const addEditProjectForm = reactive({
    branch: null,
    name: null,
    project_id: null,
    serviceable_area: null,
    default: false
});

const rules = reactive({
    branch: { required },
    name: { required },
    project_id: { required },
    serviceable_area: {},
    default: { required }
});

// vuelidate instance to bind form fields and validation rules
const v$ = useVuelidate(rules, addEditProjectForm);

// define emit
const emit = defineEmits(['close']);

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

// method to reset the project form
const resetForm = async () => {
    addEditProjectForm.branch = null;
    addEditProjectForm.name = null;
    addEditProjectForm.project_id = null;
    addEditProjectForm.serviceable_area = null;
    addEditProjectForm.default = false;
    await v$.value.$reset();
}


// method to fetch project detail
const getProjectDetail = async (id) => {
    try {
        loaderUtility.show();
        const { data } = await projectServices.getProjectDetail(id);
        addEditProjectForm.branch = data.branch;
        addEditProjectForm.name = data.name;
        addEditProjectForm.project_id = data.project_id;
        addEditProjectForm.serviceable_area = data.serviceable_area;
        addEditProjectForm.default = data.default;
    } catch (error) {
        toastUtility.showError(error);
    } finally {
        loaderUtility.hide();
    }
}

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
            const res = await projectServices.updateProject(props.id, addEditProjectForm);
            toastUtility.showSuccess(`Project has been updated successfully.`);
        } else {
            const res = await projectServices.createProject(addEditProjectForm);
            toastUtility.showSuccess(`Project has been added successfully.`);
        }
        closeDialog();
    } catch (error) {
        toastUtility.showError(error);
    } finally {
        loaderUtility.hide();
    }
};

onMounted(async () => {
    props.id ? await getProjectDetail(props.id) : null;
})

</script>

<style scoped></style>
