<template>
    <v-app-bar class="rounded-ts-lg" :elevation="15" density="compact" color="primary">
        <template v-slot:prepend>
            <v-app-bar-nav-icon icon="ri-user-line" size="small" class="ml-3" color="white"></v-app-bar-nav-icon>
        </template>
        <v-app-bar-title style="font-size: medium;">
            {{ props.id ? "Edit" : "Add" }} User
        </v-app-bar-title>
        <template v-slot:append>
            <div class="mr-1 d-flex align-center ga-1" v-if="userCreationTimeStamp">
                <v-divider vertical color="white" :thickness="2" class="mx-2"></v-divider>
                <span>{{ userCreationTimeStamp }}</span>
            </div>
        </template>
    </v-app-bar>
    <div class="h-100 d-flex justify-center mt-13">
        <v-card class="elevation-0 mx-15">
            <v-card-item class="d-flex allign-center justify-center">
                <v-card-title class="d-flex align-center justify-center">
                    <v-avatar :color="color" size="80" class="text-h3">
                        <span v-if="addEditUserForm.first_name && addEditUserForm.last_name">
                            {{ addEditUserForm.first_name[0] }}{{ addEditUserForm.last_name[0] }}
                        </span>
                        <v-icon size="50" v-else>
                            mdi-account
                        </v-icon>
                    </v-avatar>
                </v-card-title>
                <v-card-subtitle v-if="addEditUserForm.username" class="mt-3 d-flex flex-column align-center">
                    <span>{{ addEditUserForm.username }}</span>
                </v-card-subtitle>
            </v-card-item>
            <v-card-text class="pa-4">
                <v-row>
                    <v-col cols="6">
                        <InputField v-model="addEditUserForm.first_name" label="First Name *"
                            @blur="v$.first_name.$validate" :error-messages="v$.first_name.$errors.map(e => e.$message)"
                            @input="v$.first_name.$reset" @focus="v$.first_name.$reset">
                        </InputField>
                    </v-col>
                    <v-col cols="6">
                        <InputField v-model="addEditUserForm.last_name" label="Last Name *"
                            @blur="v$.last_name.$validate" :error-messages="v$.last_name.$errors.map(e => e.$message)"
                            @input="v$.last_name.$reset" @focus="v$.last_name.$reset">
                        </InputField>
                    </v-col>
                    <v-col cols="6">
                        <InputField :readonly="props.id" v-model="addEditUserForm.username" label="Username *"
                            @blur="v$.username.$validate" :error-messages="v$.username.$errors.map(e => e.$message)"
                            @input="v$.username.$reset" @focus="v$.username.$reset">
                        </InputField>
                    </v-col>
                    <v-col v-if="!props.id" cols="6">
                        <InputField v-model="addEditUserForm.password" label="Password *" type="password"
                            @blur="v$.password.$validate" :error-messages="v$.password.$errors.map(e => e.$message)"
                            @input="v$.password.$reset" @focus="v$.password.$reset">
                        </InputField>
                    </v-col>
                    <v-col cols="6">
                        <InputField v-model="addEditUserForm.email" label="Email" @blur="v$.email.$validate"
                            :error-messages="v$.email.$errors.map(e => e.$message)" @input="v$.email.$reset"
                            @focus="v$.email.$reset">
                        </InputField>
                    </v-col>
                    <v-col cols="6">
                        <InputField v-model="addEditUserForm.contact_number" label="Contact Number"
                            @blur="v$.contact_number.$validate"
                            :error-messages="v$.contact_number.$errors.map(e => e.$message)"
                            @input="v$.contact_number.$reset" @focus="v$.contact_number.$reset">
                        </InputField>
                    </v-col>
                    <v-col cols="6">
                        <v-autocomplete outlined v-model="addEditUserForm.user_type" :items="profileTypeChoices"
                            density="compact" label="Profile Type *" item-title="key" item-value="value"
                            @blur="v$.user_type.$validate"
                            :error-messages="v$.user_type.$errors.map(e => e.$message)"
                            @input="v$.user_type.$reset" @focus="v$.user_type.$reset" clear-on-select>
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="6">
                        <v-autocomplete outlined v-model="addEditUserForm.is_active" :items="profileStatusChoices"
                            density="compact" label="Status *" item-title="key" item-value="value"
                            @blur="v$.is_active.$validate" :error-messages="v$.is_active.$errors.map(e => e.$message)"
                            @input="v$.is_active.$reset" @focus="v$.is_active.$reset" clear-on-select>
                        </v-autocomplete>
                    </v-col>
                </v-row>
            </v-card-text>

            <v-card-actions class="d-flex align-center justify-end mt-5">
                <v-btn class="px-5" color="error" variant="outlined" @click="resetForm">Reset</v-btn>
                <v-btn class="px-5" color="success" variant="elevated" @click="submitForm">Submit</v-btn>
            </v-card-actions>
        </v-card>
    </div>

    <!-- dialogs -->
    <div>
    </div>
</template>

<script setup>
// internal imports 
import { onMounted, ref } from 'vue';

// external imports
import useVuelidate from '@vuelidate/core';

// components

// services imports
import { userProfileServices } from '@/services/user-profile';

// utility imports
import { getRandomColor } from '@/utilities/helpers-utility';
import loaderUtility from '@/utilities/loader/loader-utility';
import { toastUtility } from '@/utilities/toast-utility';
import { email, required } from '@vuelidate/validators';
import { profileStatusChoices, profileTypeChoices } from '@/utilities/choice-filter-utility';

// props
const props = defineProps({
    id: { type: [Number, null], required: true }
})

// variable initialization
const color = getRandomColor();
const userCreationTimeStamp = ref(null);
const addEditUserForm = reactive({
    first_name: null,
    last_name: null,
    username: null,
    password: null,
    email: null,
    contact_number: null,
    user_type: 'normal',
    is_active: true
});

const rules = reactive({
    first_name: { required },
    last_name: { required },
    username: { required },
    password: { required: props.id ? '' : required },
    email: { email },
    contact_number: {},
    user_type: { required },
    is_active: { required }
});

// vuelidate instance to bind form fields and validation rules
const v$ = useVuelidate(rules, addEditUserForm);

// define emit
const emit = defineEmits(['close']);

// method to close the dialog
const closeDrawer = () => {
    emit('close');
};

// method to reset the location form
const resetForm = async () => {
    addEditUserForm.first_name = null;
    addEditUserForm.last_name = null;
    addEditUserForm.username = props.id ? addEditUserForm.username : null;
    addEditUserForm.password = null;
    addEditUserForm.email = null;
    addEditUserForm.contact_number = null;
    addEditUserForm.user_type = null;
    addEditUserForm.is_active = null;
    await v$.value.$reset();
}


// method to fetch user-profile detail
const getUserProfileDetail = async (id) => {
    try {
        loaderUtility.show();
        const { data } = await userProfileServices.getUserProfileDetail(id);
        addEditUserForm.first_name = data.first_name;
        addEditUserForm.last_name = data.last_name;
        addEditUserForm.username = data.username;
        addEditUserForm.password = data.password;
        addEditUserForm.email = data.email;
        addEditUserForm.contact_number = data.contact_number;
        addEditUserForm.user_type = data.user_type;
        addEditUserForm.is_active = data.is_active;
        userCreationTimeStamp.value = data.added_on;
    } catch (error) {
        toastUtility.showError(error);
    } finally {
        loaderUtility.hide();
    }
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
        if (props.id) {
            const res = await userProfileServices.updateUserProfile(props.id, addEditUserForm);
            toastUtility.showSuccess(`User has been updated successfully.`);
        } else {
            const res = await userProfileServices.createUserProfile(addEditUserForm);
            toastUtility.showSuccess(` User has been added successfully.`);
        }
        closeDrawer();
    } catch (error) {
        toastUtility.showError(error);
    } finally {
        loaderUtility.hide();
    }
};

onMounted(async () => {
    props.id ? await getUserProfileDetail(props.id) : userCreationTimeStamp.value = null;
})
</script>

<style scoped></style>
