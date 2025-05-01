import * as XLSX from "xlsx";

export const excelUtility = {
    /**
     * Exports data to Excel with custom column headers and value mapping.
     * @param {Array} columns - The list of column objects containing `displayKey` and `valueKey`.
     * @param {Array} data - The data array to export.
     * @param {String} filename - The name of the exported file.
     **/
    export(columns, data, filename) {
        let modifiedData = data.map(
            (i) => {
                if (i.created) { i.created = i.created.split("T")[0]; }
                return i;
            }
        );

        modifiedData = modifiedData.map(
            (i) => {
                if (i.added_on) { i.added_on = i.added_on.split("T")[0]; }
                return i;
            }
        );

        // Map the columns to get the header names from the valueKey
        const filteredData = modifiedData.map(item => {
            return columns.reduce((obj, column) => {
                const displayKey = column.displayKey;
                const valueKey = column.valueKey;

                // Add the key-value pair to the result object
                obj[displayKey] = item[valueKey];
                return obj;
            }, {});
        });

        // Create a worksheet from the filtered data
        const ws = XLSX.utils.json_to_sheet(filteredData);

        // Format the headers: change them to match `value_key`
        const headers = columns.map(col => col.value_key);
        ws["!rows"] = ws["!rows"] || [];
        ws["!rows"].push(...headers);

        // Create a new workbook and append the worksheet
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Data");

        // Write the workbook to a file
        XLSX.writeFile(wb, filename);
    }

}
