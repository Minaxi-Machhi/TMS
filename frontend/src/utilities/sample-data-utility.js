export default {
    addressSampleData: [
        {
            "Customer": "CUST001",
            "Name": "Keval Plaza",
            "Address Id": "KP1234",
            "Contact number": "212121212122",
            "Email": null,
            "Address": "SHJAl Tarfa DUBAI UAE"
        },
        {
            "Customer": "CUST002",
            "Name": "Yamini Bergers",
            "Address Id": "YB1234",
            "Contact Number": "212121212122",
            "Email": null,
            "Address": "Ahmedabad, Gujarat, India"
        }
    ],
    vehicleSampleData: [
        {
            "Project": "Keval-default",
            "Vehicle Type": "Dyna - 5 Ton",
            "Vehicle Number": "MH12AB1234",
            "Last Odometer Reading": "256000",
            "Registration Expiry Date": "2025-12-31",
            "Insurance Expiry Date": "2025-06-15",
            "Fuel Type": "diesel",
            "Fuel Efficiency": "5.5",
            "Cost Per Km": "12.50",
            "Refrigerated": "No",
        },
    ],
    driverSampleData: [
        {
            "Project": "Keval-default",
            "Assigned Vehicle": "MH12AB1234",
            "Name": "Keval Patel",
            "Employee Id": "EMP0001",
            "Contact Number": "1212121212"
        }
    ],
    orderWithoutAddressMasterSampleData: [
        {
            "Customer": "CUST001",
            "Project": "Keval-default",
            "Reference Number": "REF-2025-0422",
            "Dispatch Date": "2025-04-20",
            "Order Date": "2025-04-18",
            "Receiver Name": "John Doe",
            "Contact Number": "5551234567",
            "Address": "123 Industrial Park Road, Springfield, IL, 62704",
            "Weight": "15",
            "Total Quantity": "250"
        }
    ],
    orderWithAddressMasterSampleData: [
        {
            "Customer": "CUST001",
            "Project": "Keval-default",
            "Reference Number": "REF-2025-042234",
            "Address Id": "KP1234",
            "Dispatch Date": "2025-04-20",
            "Order Date": "2025-04-18",
            "Receiver Name": "John Doe",
            "Contact Number": "5551234567",
            "Weight": "150",
            "Total Quantity": "250"
        }
    ]
}
