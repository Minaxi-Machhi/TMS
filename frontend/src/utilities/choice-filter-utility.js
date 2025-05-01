export const profileTypeChoices = [
    {
        key: "System Admin",
        value: "system_admin"
    },
    {
        key: "Normal",
        value: "normal"
    },
    {
        key: "Customer",
        value: "customer"
    }
]

export const profileTypeFilters = [
    {
        key: "All",
        value: null
    },
    ...profileTypeChoices
]

export const profileStatusChoices = [
    {
        key: "Active",
        value: "active"
    },
    {
        key: "Deactivated",
        value: "deactivated"
    },
]

export const profileStatusFilters = [
    {
        key: "All",
        value: null
    },
    ...profileStatusChoices
]

export const exceptionStatusChoices = [
    {
        key: "Cancelled",
        value: "cancelled"
    },
    {
        key: "Delivery Failed",
        value: "delivery_failed"
    }
]

export const exceptionStatusFilters = [
    {
        key: "All",
        value: null
    },
    ...exceptionStatusChoices
]

export const addressWarningChoices = [
    {
        key: "Yes",
        value: true,
    },
    {
        key: "No",
        value: false,
    },
]


export const addressWarningFilters = [
    {
        key: "All",
        value: null
    },
    ...addressWarningChoices
]

export const storageTypeRefrigeratedChoices = [
    {
        key: "Yes",
        value: true,
    },
    {
        key: "No",
        value: false,
    },
]


export const storageTypeRefrigeratedFilters = [
    {
        key: "All",
        value: null
    },
    ...storageTypeRefrigeratedChoices
]

export const fuelTypeChoices = [
    {
        key: "Petrol",
        value: "petrol"
    },
    {
        key: "Diesel",
        value: "diesel"
    },
    {
        key: "Electric",
        value: "electric"
    },
    {
        key: "Other",
        value: "other"
    }
]
export const vehicleStatusChoices = [
    {
        key: "Active",
        value: "active"
    },
    {
        key: "Deactivated",
        value: "deactivated"
    },
]
export const driverStatusChoices = [
    {
        key: "Active",
        value: "active"
    },
    {
        key: "Deactivated",
        value: "deactivated"
    },
]

export const orderStatusChoices = [
    {
        key: "Unassigned",
        value: "unassigned"
    },
    {
        key: "Assigned",
        value: "assigned"
    },
    {
        key: "In Transit",
        value: "in_transit"
    },
    {
        key: "Delivered",
        value: "delivered"
    },
    {
        key: "Delivery Failed",
        value: "delivery_failed"
    },
    {
        key: "Cancelled",
        value: "cancelled"
    },
    {
        key: "Rescheduled",
        value: "rescheduled"
    },
]

export const orderStatusFilters = [
    {
        key: "All",
        value: null
    },
    ...orderStatusChoices
]

export const tripStatusChoices = [
    {
        key: "Scheduled",
        value: "scheduled"
    },
    {
        key: "Active",
        value: "active"
    },
    {
        key: "Completed",
        value: "completed"
    }
]

export const TripStatusFilters = [
    {
        key: "All",
        value: null
    },
    ...orderStatusChoices
]

