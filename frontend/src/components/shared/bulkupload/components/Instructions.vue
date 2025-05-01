<template>
  <v-dialog v-model="openDialog" persistent max-width="500px">
    <v-card class="">
      <v-card-title class="d-flex justify-space-between align-center">
        <span class="text-h6 font-weight-bold text-capitalize">
          <v-icon size="small" :color="color" class="mr-3">ri-information-2-line</v-icon>
          Instructions
        </span>
        <v-spacer></v-spacer>
        <v-btn icon color="error" size="small" variant="plain" @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="pt-3">
        <div v-if="requestType == 'addresses'">
          <h5 class="text-md-Subtitle-2">Note</h5>
          <h4 class="text-caption text-primary mb-4">
            The header given in your excel must be same as below Mandatory
            Fields. For reference download sample excel file.
          </h4>
          <h5 class="text-lg-Subtitle-2">Mandatory Fields are :</h5>
          <h5 class="text-lg-caption" style="color: grey;">
            Address ID
            <br />
            Name
            <br />
            Customer
            <br />
            Address
            <br />
          </h5>
          <h5 class="text-lg-Subtitle-1 mt-4">Non Mandatory Fields are :</h5>
          <h5 class="text-lg-caption" style="color: grey;">
            Contact Number
            <br />
            Email
            <br />
          </h5>
        </div>

        <div v-if="requestType == 'orders'">
          <h5 class="text-md-Subtitle-2">Note</h5>
          <h4 class="text-caption text-primary mb-4">
            The header given in your excel must be same as below Mandatory
            Fields. For reference download sample excel file.
          </h4>
          <h5 class="text-lg-Subtitle-2">Mandatory Fields are :</h5>
          <h5 class="text-lg-caption" style="color: grey;">
            Reference Number
            <br />
            Customer Name
            <br />
            Country
            <br />
            Contact Number
            <br />
            Commodities
            <br />
            Order Date
            <br />
            Holding Area
            <br />
            Zone
            <br />
            Booth
            <br />

          </h5>
          <h5 class="text-lg-Subtitle-1 mt-4">Non Mandatory Fields are :</h5>
          <h5 class="text-lg-caption" style="color: grey;">
            Remarks
            <br />
          </h5>
        </div>
      </v-card-text>
      <v-card-actions class="d-flex justify-end">
        <!-- <v-btn color="primary" @click="closeDialog"> Close </v-btn> -->
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  name: "instruction-dialog",
  props: {
    modelValue: Boolean,

    requestType: {
      type: String,
    },
  },
  computed: {
    openDialog: {
      get() {
        return this.modelValue;
      },
      set(modelValue) {
        this.$emit("input", modelValue);
        this.$emit("update:modelValue", modelValue);
      },
    },
  },

  methods: {
    closeDialog() {
      this.$emit("closeDialogBox", false);
    },
  },
};
</script>
