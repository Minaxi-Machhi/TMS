<template>
    <v-dialog v-model="localDialogVisible" persistent width="900" :overlay="false" transition="dialog-transition">
        <v-card>
            <v-card-title class="px-6 py-2 d-flex align-center justify-space-between">
                <div class="d-flex align-center">
                    <v-icon size="x-small" :color="color" class="mr-3">ri-key-line</v-icon>
                    <span class="text-h5 text-capitalize">
                        Change Password
                    </span>
                </div>
                <v-btn icon color="error" variant="plain" @click="closeDialog">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-card-title>


            <v-card-text>
                <div class="v-container pa-1 my-2 pb-0">
                    <v-row>
                        <v-col cols="4">
                            <InputField v-model="changePasswordForm.current_password" label=" Old Password"
                                name="old_password" :type="isPasswordVisible ? 'text' : 'password'"
                                :append-inner-icon="isPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
                                @click:append-inner="isPasswordVisible = !isPasswordVisible"
                                @blur="v$.current_password.$validate"
                                :error-messages="v$.current_password.$errors.map(e => e.$message)"
                                @input="v$.current_password.$reset" @focus="v$.current_password.$reset" />
                        </v-col>

                        <v-col cols="4">
                            <InputField v-model="changePasswordForm.new_password" label="New Password"
                                name="new_password" :type="isNewPasswordVisible ? 'text' : 'password'"
                                :append-inner-icon="isNewPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'
                                    " @click:append-inner="
                                        isNewPasswordVisible = !isNewPasswordVisible
                                        " @blur="v$.new_password.$validate"
                                :error-messages="v$.new_password.$errors.map(e => e.$message)"
                                @input="v$.new_password.$reset" @focus="v$.new_password.$reset" />
                        </v-col>

                        <v-col cols="4">
                            <InputField v-model="changePasswordForm.confirm_new_password" label="Confirm Password"
                                name="confirm_password" :type="isConfirmPasswordVisible ? 'text' : 'password'"
                                :append-inner-icon="isConfirmPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'
                                    " @click:append-inner="
                                        isConfirmPasswordVisible = !isConfirmPasswordVisible
                                        " @blur="v$.confirm_new_password.$validate"
                                :error-messages="v$.confirm_new_password.$errors.map(e => e.$message)"
                                @input="v$.confirm_new_password.$reset" @focus="v$.confirm_new_password.$reset" />
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
import { userProfileServices } from '@/services/user-profile';
import loaderUtility from '@/utilities/loader/loader-utility';
import { toastUtility } from '@/utilities/toast-utility';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';


// props
const props = defineProps({
    dialogVisible: {
        type: Boolean,
        default: false
    },
});

// initialization of reactive data
const localDialogVisible = ref(props.dialogVisible);
const isPasswordVisible = ref(false);
const isNewPasswordVisible = ref(false);
const isConfirmPasswordVisible = ref(false);

const changePasswordForm = reactive({
    current_password: null,
    new_password: null,
    confirm_new_password: null,
});

const rules = reactive({
    current_password: { required },
    new_password: { required },
    confirm_new_password: { required },
});

// vuelidate instance to bind form fields and validation rules
const v$ = useVuelidate(rules, changePasswordForm);

// define emit
const emit = defineEmits(['close']);

// method to close the dialog
const closeDialog = () => {
    localDialogVisible.value = false;
    emit('close');
};

// handle the case when user clicks outside the modal
watch(localDialogVisible, (newVal) => {
    if (!newVal) {
        emit('close');
    }
});

// method to reset the location form
const resetForm = async () => {
    changePasswordForm.current_password = null;
    changePasswordForm.new_password = null;
    changePasswordForm.confirm_new_password = null;
    await v$.value.$reset();
}

// method to submit the location form
const submitForm = async () => {
    const isValidate = await v$.value.$validate();
    if (!isValidate) {
        toastUtility.showError("Please correct all the errors to submit the form!");
        return;
    }
    try {
        loaderUtility.show();
        const res = await userProfileServices.changePassword(changePasswordForm);
        toastUtility.showSuccess(`Password changed successfully.`);
        closeDialog();
    } catch (error) {
        toastUtility.showError(error);
    } finally {
        loaderUtility.hide();
    }
};

onMounted(() => {
});

</script>

<style scoped></style>
