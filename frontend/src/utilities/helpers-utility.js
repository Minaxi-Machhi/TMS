export const capitalize = (val) => {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}

export const removeUnderScore = (val) => {
    return String(val).replaceAll("_", " ");
}

export const removeUnderScoreAndCapitalize = (val) => {
    return capitalize(removeUnderScore(val));
}

export const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

export const getColor = (colorName) => {
    const colorMap = {
        orange: '#FF9800',
        green: '#4CAF50',
        blue: '#2196F3',
        red: '#F44336',
        yellow: '#FFEB3B',
        purple: '#9C27B0',
        pink: '#E91E63',
        teal: '#009688',
        indigo: '#3F51B5',
        grey: '#9E9E9E',
        cyan: '#00BCD4',
        amber: '#FFC107',
        lime: '#CDDC39',
        deepOrange: '#FF5722',
        deepPurple: '#673AB7',
        burgundy: '#800020',
        brown: '#795548',
        darkBrown: '#5C4033',
        lightBlue: '#03A9F4',
        lightGreen: '#8BC34A',
        darkBlue: '#191970',
        darkGreen: '#2E7D32',
        oliveGreen: '#808000',
        waterMelon: '#E8476A',
        deepViolet: '#330066',
        claret: '#7f1734',
        rust: '#B7410E',
        black: '#000000',
        white: '#FFFFFF',
    };

    return colorMap[colorName] || '#000000'; // Default to black if color not found
}

export const getOrderItemStatusColor = (status) => {
    switch (status) {
        case "created":
            return "#8D6E63";
        case "in_holding_area":
            return "#42A5F5";
        case "in_transit":
            return "#FFCA28";
        case "in_zone":
            return "#FF7043";
        case "in_booth":
            return "#AB47BC";
        case "empty_collected":
            return "#F06292";
        case "returned":
            return "#EF5350";
        case "completed":
            return "#66BB6A";
        case "shipped_out":
            return "#29B6F6";
        default:
            return "#B0BEC5";
    }
};

export const getOrderFinancialStateColor = (financialState) => {
    switch (financialState) {
        case "pending":
            return "#F44336";
        case "confirmed_inbound":
            return "#1976D2";
        case "confirmed_outbound":
            return "#FFC107";
        default:
            return "#000000";
    }
}

export const getProfileTypeColor = (profileType) => {
    switch (profileType) {
        case 'System Admin': return '#C62828';
        case 'Team Member': return '#1B5E20';
        default: return '#9E9E9E';
    }
}

export const isImage = (url) => {
    if (url) { return (url.match(/\.(jpeg|jpg|gif|png)$/) != null); }
}

export const getOrderStatusColor = (status) => {
    switch (status) {
        case "unassigned":
            return "#37474F";
        case "assigned":
            return "#1976D2";
        case "in_transit":
            return "#FF9800";
        case "delivered":
            return "#4CAF50";
        case "delivery_failed":
            return "#F44336";
        case "cancelled":
            return "#424242";
        case "rescheduled":
            return "#9C27B0";
        default:
            return "#000000";
    }
};

export const getTripStatusColor = (status) => {
    switch (status) {
        case "scheduled":
            return "#1976D2";
        case "active":
            return "#FF9800";
        case "completed":
            return "#1B5E20";
        default:
            return "#000000";
    }
};

export const getDriverStatusColor = (status) => {
    switch (status) {
        case "active":
            return "#1976D2";
        case "deactivated":
            return "#37474F";
        default:
            return "#000000";
    }
};

export const getVehicleStatusColor = (status) => {
    switch (status) {
        case "active":
            return "#1976D2";
        case "deactivated":
            return "#37474F";
        default:
            return "#000000";
    }
};

export const formatLocalTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    })
}

export const formatTime = (timeStr) => {
    return timeStr.slice(0, 5); // Extracts "HH:MM"
}
