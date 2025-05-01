<template>
  <v-dialog v-model="bulkUploadDialog" persistent scrollable width="60%" height="auto">
    <v-card flat class="rounded-lg">
      <v-card-title class="px-6 py-2 d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon size="x-small" :color="color" class="mr-3">ri-stack-line</v-icon>
          <span class="text-h5 text-capitalize">
            {{ getTextChange(uploadTo) }}
          </span>
        </div>
        <v-btn icon color="error" variant="plain" @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-row class="pt-8">
          <v-col cols="6" class="d-flex">
            <FileField id="bulkUploadSelectFile" v-model="file" label="Select File" accept=".xlsx, .xls, .csv"
              @change="getFileData($event)" />
            <v-icon id="bulkUploadInformationButton" class="d-flex align-center ma-2" color="primary"
              @click="openInstructionDialog">
              mdi-information
            </v-icon>

          </v-col>
          <v-col class="d-flex justify-end">
            <v-btn color="primary" variant="flat" class="bg-primary" rounded="xl" height="32"
              @click="handleButtonClick()">
              Download Sample Excel File
            </v-btn>
          </v-col>
          <v-col cols="12" class="d-flex justify-space-between pt-0">
            <span>Total Records : {{ totalRecordCount }}</span>
            <span>Records with Error : {{ rowData.length }}</span>
          </v-col>
          <v-col v-if="distinctErrors.length > 0" class="py-0">
            <v-alert class="custom-alert" variant="outlined" border="start" type="error">
              <v-row no-gutters align="center">
                <v-col cols="8">
                  <v-list class="py-0" style="background-color: #f8d7da">
                    <v-list-item-title class="error-box">
                      Error(s):
                    </v-list-item-title>
                    <v-list-item v-for="(err, index) in distinctErrors" :key="index" class="text-black">
                      {{ err }}
                    </v-list-item>
                  </v-list>
                </v-col>
                <v-col cols="4" class="d-flex justify-end">
                  <v-btn id="bulkUploadRemoveErrorButton" class="bg-error" color="error" text-wrap
                    @click="removeAllRecordWithError">
                    Remove All With Error
                  </v-btn>
                </v-col>
              </v-row>
            </v-alert>
          </v-col>
          <v-col v-if="rowData.length > 0" cols="12">
            <AgGridVue :column-defs="columnDefs" :grid-options="gridOptions" :default-col-def="defaultColDef"
              style="width: 100%; height: 400px" :row-data="rowData" class="ag-theme-quartz" @grid-ready="gridReady">
            </AgGridVue>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="pa-4 d-flex justify-end">
        <v-btn id="bulkUploadSubmitButton" color="primary" variant="flat" :loading="loading"
          :disabled="!file || rowData.length != 0" @click="submitData()">
          Submit
        </v-btn>

      </v-card-actions>
    </v-card>
    <Instruction v-model="instructionDialog" :requestType="requestType" @closeDialogBox="closeChildDiaologBox" />
  </v-dialog>
</template>

<script>
/* eslint-disable */

import { AgGridVue } from "ag-grid-vue3";

import bulkSampleData from "@/utilities/sample-data-utility";
import { read, utils, write } from "xlsx";
import FileField from "./components/FileField.vue";
import Instruction from "./components/Instructions.vue";
import RemoveRowButtonBulkUpload from "./components/RemoveRowButtonBulkUpload.vue";
import { compareTwoStrings, toCapitalize } from "./helpers";

import { errorHandlerUtility } from "@/utilities/error-handler-utility";
import loaderUtility from "@/utilities/loader/loader-utility";
import { toastUtility } from "@/utilities/toast-utility";
import { orderServices } from "@/services/orders/orders";
import { addressBookServices } from "@/services/addresses/address-book";
import { driverServices } from "@/services/asset-management/driver";
import { vehicleServices } from "@/services/asset-management/vehicle";

export default {
  components: {
    AgGridVue,
    Instruction,
    RemoveRowButtonBulkUpload,
    FileField,
  },
  props: {
    modelValue: {
      type: Boolean,
    },
    uploadTo: {
      required: true,
      type: String,
    },
    contractParams: {
      type: Object,
    },
  },
  data() {
    return {
      toCapitalize,
      compareTwoStrings,
      instructionDialog: false,
      requestType: null,
      loading: false,
      file: null,
      fulldata: [],
      rowData: [],
      columnDefs: [],
      reqFields: [],
      allFields: null,
      gridApi: null,
      columnApi: null,
      gridOptions: {
        headerHeight: 40,
        rowHeight: 40,
        rowSelection: "multiple",
        suppressRowClickSelection: true,
        suppressDragLeaveHidesColumns: true,
        enableCellTextSelection: true,
      },
      defaultColDef: {
        lockPosition: true,
      },
      requiredHeaders: [],
      serverErrors: [],
      networkRowData: [],
      contractRatesData: [],
      dataObject: {},
      selectedEvent: null
    };
  },
  computed: {
    totalRecordCount() {
      return this.fulldata.filter((obj) => Object.keys(obj).length !== 0)
        .length;
    },
    bulkUploadDialog: {
      get() {
        return this.modelValue;
      },
      set(modelValue) {
        // ? For backward compatibility
        this.$emit("input", modelValue);
        this.$emit("update:modelValue", modelValue);
      },
    },
    addressFields() {
      return [
        {
          name: "Addreess ID",
          key: "address_id",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Name",
          key: "name",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Customer",
          key: "customer",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Address",
          key: "address",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Contact Number",
          key: "contact_number",
          type: "string",
          required: false,
          matchRatio: 0.95,
        },
        {
          name: "Email",
          key: "email",
          type: "string",
          required: false,
          matchRatio: 0.95,
        }
      ];
    },
    driverFields() {
      return [
        {
          name: "Project",
          key: "project",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Assigned Vehicle",
          key: "assigned_vehicle",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Name",
          key: "name",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Employee Id",
          key: "employee_id",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Contact Number",
          key: "contact_number",
          type: "string",
          required: false,
          matchRatio: 0.95,
        },
      ];
    },
    vehicleFields() {
      return [
        {
          name: "Project",
          key: "project",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Vehicle Type",
          key: "vehicle_type",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Vehicle Number",
          key: "vehicle_number",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Last Odometer Reading",
          key: "last_odometer_reading",
          type: "string",
          required: false,
          matchRatio: 0.95,
        },
        {
          name: "Registration Expiry Date",
          key: "registration_expiry_date",
          type: "string",
          required: false,
          matchRatio: 0.95,
        },
        {
          name: "Insurance Expiry Date",
          key: "insurance_expiry_date",
          type: "string",
          required: false,
          matchRatio: 0.95,
        },
        {
          name: "Fuel Type",
          key: "fuel_type",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Fuel Efficiency",
          key: "fuel_efficiency",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Cost Per KM",
          key: "cost_per_km",
          type: "string",
          required: true,
          matchRatio: 0.95,
        },
        {
          name: "Refrigerated",
          key: "refrigerated",
          type: "string",
          required: true,
          matchRatio: 0.95,
        }
      ];
    },
    ordersWithoutAddressMasterFields() {
      return [
        { name: "Customer", key: "customer", type: "string", required: true, matchRatio: 0.95 },
        { name: "Project", key: "project", type: "string", required: true, matchRatio: 0.95 },
        { name: "Reference Number", key: "reference_number", type: "string", required: true, matchRatio: 0.95 },
        { name: "Dispatch Date", key: "dispatch_date", type: "string", required: true, matchRatio: 0.95 },
        { name: "Order Date", key: "order_date", type: "string", required: true, matchRatio: 0.95 },
        { name: "Receiver Name", key: "receiver_name", type: "string", required: true, matchRatio: 0.95 },
        { name: "Contact Number", key: "contact_number", type: "string", required: false, matchRatio: 0.95 },
        { name: "Address", key: "address", type: "string", required: true, matchRatio: 0.95 },
        { name: "Weight", key: "weight", type: "string", required: true, matchRatio: 0.95 },
        { name: "Total Quantity", key: "total_quantity", type: "string", required: false, matchRatio: 0.95 }
      ]
    },
    ordersWithAddressMasterFields() {
      return [
        { name: "Customer", key: "customer", type: "string", required: true, matchRatio: 0.95 },
        { name: "Project", key: "project", type: "string", required: true, matchRatio: 0.95 },
        { name: "Reference Number", key: "reference_number", type: "string", required: true, matchRatio: 0.95 },
        { name: "Address Id", key: "address_book", type: "string", required: true, matchRatio: 0.95 },
        { name: "Dispatch Date", key: "dispatch_date", type: "string", required: true, matchRatio: 0.95 },
        { name: "Order Date", key: "order_date", type: "string", required: true, matchRatio: 0.95 },
        { name: "Receiver Name", key: "receiver_name", type: "string", required: true, matchRatio: 0.95 },
        { name: "Contact Number", key: "contact_number", type: "string", required: false, matchRatio: 0.95 },
        { name: "Weight", key: "weight", type: "string", required: true, matchRatio: 0.95 },
        { name: "Total Quantity", key: "total_quantity", type: "string", required: false, matchRatio: 0.95 }
      ]
    },
    distinctErrors() {
      let err = [];

      this.serverErrors
        .filter((e) => {
          return Object.keys(e).length > 0;
        })
        .map((m) => {
          return Object.keys(m).map((k) => {
            return m[k];
          });
        })
        .forEach((r) => {
          r.forEach((s) => {
            err = [...new Set([...err, ...s])];
          });
        });
      return err;
    }
  },
  methods: {
    getTextChange(type) {
      switch (type) {
        case "addresses":
          return "bulk Upload Addresses";
        case "drivers":
          return "bulk Upload Drivers";
        case "vehicles":
          return "bulk Upload Vehicles";
        case "orders_without_am":
          return "Bulk Upload Orders (Without Address Master)";
        case "orders_with_am":
          return "Bulk Upload Orders (With Address Master)";
      }
    },
    openInstructionDialog() {
      this.instructionDialog = true;
      this.requestType = this.uploadTo;
    },
    closeChildDiaologBox() {
      this.instructionDialog = false;
    },
    gridReady(params) {
      this.gridApi = params.api;
      this.columnApi = params.columnApi;
    },
    setMandatoryFields() {
      if (this.uploadTo == "addresses") {
        this.reqFields = this.addressFields.filter((f) => f.required);
        this.allFields = this.addressFields;
      }
      if (this.uploadTo == "drivers") {
        this.reqFields = this.driverFields.filter((f) => f.required);
        this.allFields = this.driverFields;
      }
      if (this.uploadTo == "vehicles") {
        this.reqFields = this.vehicleFields.filter((f) => f.required);
        this.allFields = this.vehicleFields;
      }
      if (this.uploadTo == "orders_without_am") {
        this.reqFields = this.ordersWithoutAddressMasterFields.filter((f) => f.required);
        this.allFields = this.ordersWithoutAddressMasterFields;
      }
      if (this.uploadTo == "orders_with_am") {
        this.reqFields = this.ordersWithAddressMasterFields.filter((f) => f.required);
        this.allFields = this.ordersWithAddressMasterFields;
      }
    },
    getFileData(file) {
      if (file) {
        this.file = file;
        this.loading = true;
        let reader = new FileReader();

        this.setMandatoryFields();

        reader.onload = async () => {
          /**
           * Clear previous data if any
           */
          this.excelData = [];

          /**
           * Read the uploaded file
           */
          let fileData = reader.result;
          let wb = read(fileData, {
            type: "binary",
          });

          if (this.hasMissingHeader(wb.Sheets[wb.SheetNames[0]])) {
            return;
          }

          let rowData = utils.sheet_to_row_object_array(
            wb.Sheets[wb.SheetNames[0]]
          );
          // console.log("row_data", rowData);

          // Extract fields with blank values
          let blankFields = rowData.filter((row) => {
            return Object.values(row).every((value) => value === "");
          });
          let filterdData = this.checkData(rowData);
          // console.log("filtered_data", filterdData);
          this.setData(filterdData);
        };

        reader.readAsBinaryString(file);
      } else {
        this.clearDialogData();
      }
    },
    hasMissingHeader(sheetData) {
      let headers = utils.sheet_to_csv(sheetData).split(/\r?\n/)[0].split(",");

      let missingHeaders = this.getMissingHeaders(headers);

      if (missingHeaders.length > 0) {
        this.clearDialogData();
        this.loading = false;
        alert("Column(s) '" + missingHeaders.join(", ") + "' are missing");
        return true;
      } else {
        this.correctSpellingMistakesInHeaders(headers);
        return false;
      }
    },
    getMissingHeaders(headers) {
      let missingFields = [];
      this.reqFields.forEach((_field, index) => {
        let field = headers.find((head, index) => {
          return (
            compareTwoStrings(_field.name, head) >= _field.matchRatio ||
            compareTwoStrings(_field.key, head) >= _field.matchRatio
          );
        });
        if (!field) {
          missingFields.push(_field.name);
        }
      });
      return missingFields;
    },
    correctSpellingMistakesInHeaders(headers) {
      headers.forEach((header, index) => {
        let keyConfig = this.getKeyConfig(header);
        headers[index] = keyConfig.name;
        if (headers.length - 1 == index) {
          this.setHeaders(headers);
        }
      });
    },
    checkData(rowObj) {
      let data = [];
      let dataWithError = [];

      rowObj.forEach((obj, index) => {
        Object.keys(obj).forEach((k) => {
          if (typeof obj[k] == "object") {
            let __o;
            if (Array.isArray(obj[k])) {
              __o = obj[k][0];
            } else {
              __o = obj[k];
            }
            Object.keys(__o).forEach((__k) => {
              obj[__k] = __o[__k];
            });
            delete obj[k];
          }
        });

        obj = this.correctSpellingMistakesInKeys(obj);

        let keys = Object.keys(obj);

        let missingFields = this.checkMissingFieldsForRecord(keys);

        if (missingFields.length > 0 || this.hasServerError(index)) {
          obj.oldIndex = index;
          dataWithError.push(obj);
          let err = {};
          missingFields.forEach((mf) => {
            err[mf.key] = [`${mf.name} is Required`];
          });
          this.serverErrors.push(err);
        } else {
          this.serverErrors.push({});
        }

        keys.forEach((name) => {
          let type = this.getKeyConfig(name);
          if (type) {
            if (type.key != name) {
              obj[type.key] = obj[name];
              delete obj[name];
            }

            if (type.type === "date" || type.type === "time") {
              obj[type.key] = this.getDate(obj[type.key], type.type);
            }
            if (type.type === "number" && type.dp) {
              obj[type.key] = Number.parseFloat(obj[type.key]).toFixed(type.dp);
            }
            if (type.merge_into) {
              if (!obj[type.merge_into]) {
                if (type.merge_type == "array") {
                  obj[type.merge_into] = [{}];
                } else {
                  obj[type.merge_into] = {};
                }
              }
              if (type.merge_type == "array") {
                obj[type.merge_into][0][type.key] = obj[type.key];
              } else {
                obj[type.merge_into][type.key] = obj[type.key];
              }
              delete obj[type.key];
            }
          }
        });
        data.push(obj);
      });

      return { data: data, dataWithError: dataWithError };
    },
    correctSpellingMistakesInKeys(object) {
      let obj = {};
      Object.keys(object).forEach((key, index) => {
        let keyConfig = this.getKeyConfig(key);
        obj[keyConfig.name] = object[key];
      });
      return obj;
    },
    getKeyConfig(name) {
      let field = this.allFields.find((f) => {
        return (
          compareTwoStrings(f.name, name.trim()) >= f.matchRatio ||
          compareTwoStrings(f.key, name.trim()) >= f.matchRatio
        );
      });

      if (field) {
        return field;
      } else {
        return null;
      }
    },
    setData(filterdData) {
      this.fulldata = filterdData.data;
      if (filterdData.dataWithError.length > 0) {
        this.rowData = filterdData.dataWithError;
      }
      this.loading = false;
    },
    hasServerError(index) {
      if (
        this.serverErrors &&
        this.serverErrors.length > 0 &&
        this.serverErrors[index] &&
        Object.keys(this.serverErrors[index]).length > 0
      ) {
        return true;
      } else {
        return false;
      }
    },
    checkMissingFieldsForRecord(fields) {
      return this.reqFields.filter((field) => {
        let map = fields.map((k) => {
          return k.trim();
        });

        return map.indexOf(field.name) == -1 && map.indexOf(field.key) == -1;
      });
    },
    async checkEditedRecord(param) {
      if (param.newValue == param.oldValue) {
        return null;
      }

      let record = param.data;

      let keys = Object.keys(record);
      let i = 0;

      while (i < keys.length) {
        let k = keys[i];
        if (typeof record[k] == "object") {
          let __o;
          if (Array.isArray(record[k])) {
            __o = record[k][0];
          } else {
            __o = record[k];
          }
          Object.keys(__o).forEach((__k) => {
            record[__k] = __o[__k];
          });
        }
        i++;
      }

      keys = Object.keys(record);

      let _errhead = this.reqFields.filter((f) => {
        let hasKey =
          keys.indexOf(f.key.toLowerCase().replace(/\ /g, "_")) == -1;

        if (f.merge_into) {
          delete record[f.key];
        }

        return hasKey;
      });

      if (_errhead.length > 0) {
        return null;
      }

      let reqKeys = this.reqFields.map((k) => {
        return k.key;
      });

      while (i < reqKeys.length) {
        let type = this.getKeyConfig(reqKeys[i]);

        if (record[type.key] == null || record[type.key] == "") {
          return null;
        } else {
          if (type) {
            if (type.type == "number" && type.dp) {
              record[type.key] = parseFloat(record[type.key]).toFixed(type.dp);
            }
          }
        }
        i++;
      }

      this.rowData.splice(
        this.rowData.indexOf(
          this.rowData.find((d) => d.oldIndex == record.oldIndex)
        ),
        1
      );
      let index = record.oldIndex;
      delete record.oldIndex;
      this.fulldata.splice(index, 1, record);

      if (this.rowData.length == 0) {
        this.serverErrors = [];
      }
    },
    removeAllRecordWithError() {
      while (this.rowData.length > 0) {
        this.removeDataFromRow(this.rowData[0].oldIndex, 0);
      }
    },
    removeDataFromRow(oldIndex, currentIndex) {
      this.fulldata.splice(oldIndex, 1, {});
      this.rowData.splice(currentIndex, 1);

      let data = this.fulldata.filter((obj) => Object.keys(obj).length !== 0);

      if (data.length == 0) {
        this.clearDialogData();
      }

      if (this.rowData.length == 0) {
        this.serverErrors = [];
      }
    },
    async setHeaders(headers) {
      this.columnDefs = [];

      headers.forEach((header) => {
        let field = this.getKeyConfig(header);
        let key = field.key;
        header = field.name;

        if (field.merge_into) {
          key = `${field.merge_into}.${field.key}`;
        }

        let obj = {
          headerName: header,
          field: key,
          editable: true,
          onCellValueChanged: (param) => {
            this.checkEditedRecord(param);
          },
        };

        obj.cellClass = (param) => {
          let f = param.colDef.field.split(".");
          let field = f[f.length - 1];
          if (
            this.serverErrors.length > 0 &&
            Object.keys(param.data).indexOf("oldIndex") > -1 &&
            Array.isArray(this.serverErrors[param.data.oldIndex][field])
          ) {
            return "cell-error";
          }
        };

        this.columnDefs.push(obj);
      });
    },
    getDate(serial, type) {
      if (typeof serial == "number") {
        let utc_days = Math.floor(serial - 25569);
        let utc_value = utc_days * 86400;
        let date_info = new Date(utc_value * 1000);

        let fractional_day = serial - Math.floor(serial) + 0.0000001;

        let total_seconds = Math.floor(86400 * fractional_day);

        let seconds = total_seconds % 60;

        total_seconds -= seconds;

        let hours = Math.floor(total_seconds / (60 * 60));
        let minutes = Math.floor(total_seconds / 60) % 60;

        if (hours < 10) {
          hours = "0" + hours;
        }
        if (minutes < 10) {
          minutes = "0" + minutes;
        }

        if (type == "date") {
          return [
            date_info.getFullYear(),
            date_info.getMonth() + 1,
            date_info.getDate(),
          ].join("-");
        } else {
          return [hours, minutes].join(":");
        }
      } else {
        return serial;
      }
    },
    getSheetData() {
      if (this.uploadTo == "addresses") {
        let ws = utils.json_to_sheet(bulkSampleData.addressSampleData);
        return ws;
      }
      else if (this.uploadTo == "drivers") {
        let ws = utils.json_to_sheet(bulkSampleData.driverSampleData);
        return ws;
      }
      else if (this.uploadTo == "vehicles") {
        let ws = utils.json_to_sheet(bulkSampleData.vehicleSampleData);
        return ws;
      }
      else if (this.uploadTo == "orders_without_am") {
        let ws = utils.json_to_sheet(bulkSampleData.orderWithoutAddressMasterSampleData);
        return ws;
      }
      else if (this.uploadTo == "orders_with_am") {
        let ws = utils.json_to_sheet(bulkSampleData.orderWithAddressMasterSampleData);
        return ws;
      }
      else {
        let ws = utils.json_to_sheet([]);
        return ws;
      }
    },
    downloadSampleExcel() {
      var wb = utils.book_new();
      wb.Props = {
        Title: toCapitalize(this.uploadTo) + " sample excel file",
        Subject: "Sample Excel",
        Author: "Fero",
        CreatedDate: new Date(),
      };

      wb.SheetNames.push(`${this.uploadTo} Sheet`);

      wb.Sheets[`${this.uploadTo} Sheet`] = this.getSheetData();

      var wbout = write(wb, { bookType: "xlsx", type: "binary" });

      let blob = new Blob([this.s2ab(wbout)], {
        type: "application/octet-stream",
      });

      this.download(blob);
    },
    s2ab(s) {
      var buf = new ArrayBuffer(s.length);
      var view = new Uint8Array(buf);
      for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xff;
      return buf;
    },
    download(blob) {
      let url = window.URL.createObjectURL(blob);

      let a = document.createElement("a");
      a.href = url;
      a.download = this.uploadTo + " sample excel file.xlsx";
      a.click();
      window.URL.revokeObjectURL(url);
    },
    convertExcelDate(excelSerial) {
      const date = new Date(0, 0, excelSerial);
      date.setFullYear(date.getFullYear());
      return date.toISOString().slice(0, 10); // Format as YYYY-MM-DD
    },
    closeDialog() {
      this.bulkUploadDialog = false;
      this.loading = false;
      this.clearDialogData();
      this.$emit("refreshList");
    },
    clearDialogData() {
      this.file = null;
      this.fulldata = [];
      this.rowData = [];
      this.reqFields = [];
      this.serverErrors = [];
    },
    handleButtonClick() {
      if (
        this.uploadTo === "addresses" ||
        this.uploadTo === "drivers" ||
        this.uploadTo === "vehicles" ||
        this.uploadTo === "orders_without_am" ||
        this.uploadTo === "orders_with_am"
      ) {
        this.downloadSampleExcel();
      } else {
        this.getSampleData();
      }
    },
    getModule() {
      let isUpdate = false;

      if (
        this.uploadTo === "rates_update" ||
        this.uploadTo === "drivers_update" ||
        this.uploadTo === "vehicles_update" ||
        this.uploadTo === "customer_address_update" ||
        this.uploadTo === "address_update"
      ) {
        isUpdate = true;
      }
      let moduleName, functionName;

      if (this.uploadTo === "rates" || this.uploadTo === "rates_update") {
        moduleName = "rates";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "drivers" ||
        this.uploadTo === "drivers_update"
      ) {
        moduleName = "driver";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "vehicles" ||
        this.uploadTo === "vehicles_update"
      ) {
        moduleName = "vehicle";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "customer_address" ||
        this.uploadTo === "customer_address_update"
      ) {
        moduleName = "customerAddress";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "items" ||
        this.uploadTo === "items_update"
      ) {
        moduleName = "item";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "orders" ||
        this.uploadTo === "orders_update"
      ) {
        moduleName = "order";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "address" ||
        this.uploadTo === "address_update"
      ) {
        moduleName = "address";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "network_routes" ||
        this.uploadTo === "network_routes_update"
      ) {
        moduleName = "network";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "contracts" ||
        this.uploadTo === "contracts_update"
      ) {
        moduleName = "contract";
        functionName = "getSampleData";
      } else if (
        this.uploadTo === "order_with_pallets"
      ) {
        moduleName = "order";
        functionName = "getSampleDataOrderPackages";
      }
      return {
        moduleFunction: this.$api[moduleName][functionName],
        isUpdate: isUpdate,
      };
    },
    async getSampleData() {
      const { moduleFunction, isUpdate } = this.getModule();
      if (moduleFunction) {
        try {
          let params = {
            is_update: isUpdate,
          };
          if (this.uploadTo === "contracts") {
            params = {
              ...this.contractParams,
            };
          }
          const response = await moduleFunction(params, {
            responseType: "arraybuffer",
          });
          this.downloadWorkbook(response.data);
        } catch (error) {
          console.error("Error fetching workbook:", error);
        }
      } else {
        console.error("Module not available for current uploadTo value.");
      }
    },

    downloadWorkbook(data) {
      // Create a Blob from the binary data
      const blob = new Blob([data], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });
      // this.downloadBlobData(data)
      // Create a link element
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;

      // Set the filename for the download
      const name = toCapitalize(this.uploadTo) + " Sample excel file";
      link.setAttribute("download", name + ".xlsx");

      // Append the link to the body and trigger the download
      document.body.appendChild(link);
      link.click();

      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);
    },
    async submitData() {
      this.loading = true;

      this.serverErrors = [];
      this.fulldata = this.fulldata.filter((obj) => {
        return Object.keys(obj).length !== 0;
      });

      if (this.fulldata.length == 0) {
        this.loading = false;
        alert("Please add values in Document");
        this.clearDialogData();
        return null;
      }

      if (this.uploadTo === "addresses") {
        try {
          loaderUtility.show();
          const res = await addressBookServices.bulkUploadAddress(this.fulldata);
          toastUtility.showSuccess(`Bulk upload address completed.`);
          this.closeDialog();
        } catch (error) {
          this.serverErrors = error;
          let filterdData = this.checkData(this.fulldata);
          this.setData(filterdData);
        } finally {
          loaderUtility.hide();
          this.loading = false;
        }
      }

      if (this.uploadTo === "drivers") {
        try {
          loaderUtility.show();
          const res = await driverServices.bulkUploadDrivers(this.fulldata);
          toastUtility.showSuccess(`Bulk upload drivers completed.`);
          this.closeDialog();
        } catch (error) {
          this.serverErrors = error;
          let filterdData = this.checkData(this.fulldata);
          this.setData(filterdData);
        } finally {
          loaderUtility.hide();
          this.loading = false;
        }
      }

      if (this.uploadTo === "vehicles") {
        try {
          loaderUtility.show();
          const res = await vehicleServices.bulkUploadVehicles(this.fulldata);
          toastUtility.showSuccess(`Bulk upload vehicles completed.`);
          this.closeDialog();
        } catch (error) {
          this.serverErrors = error;
          let filterdData = this.checkData(this.fulldata);
          this.setData(filterdData);
        } finally {
          loaderUtility.hide();
          this.loading = false;
        }
      }

      if (this.uploadTo === "orders_without_am") {
        try {
          loaderUtility.show();
          const res = await orderServices.bulkUploadOrdersWithoutAddressMaster(this.fulldata);
          toastUtility.showSuccess(`Bulk upload orders completed.`);
          this.closeDialog();
        } catch (error) {
          this.serverErrors = error;
          let filterdData = this.checkData(this.fulldata);
          this.setData(filterdData);
        } finally {
          loaderUtility.hide();
          this.loading = false;
        }
      }

      if (this.uploadTo === "orders_with_am") {
        try {
          loaderUtility.show();
          const res = await orderServices.bulkUploadOrdersWithAddressMaster(this.fulldata);
          toastUtility.showSuccess(`Bulk upload orders completed.`);
          this.closeDialog();
        } catch (error) {
          this.serverErrors = error;
          let filterdData = this.checkData(this.fulldata);
          this.setData(filterdData);
        } finally {
          loaderUtility.hide();
          this.loading = false;
        }
      }
    },
  },
  mounted() { }
};
</script>

<style scoped>
.custom-alert {
  background-color: #f8d7da;
  /* Light red */
  border-color: #f5c6cb;
  /* Red */
  color: #721c24;
  /* Dark red */
  padding: 10px;
  border-radius: 5px;
}

.custom-alert .v-alert__text {
  font-size: 16px;
}

.custom-alert .v-btn {
  min-width: 150px;
}

.error-box {
  background-color: #f8d7da;
  /* Light red */
}
</style>
