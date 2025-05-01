export const createLineChartOptions = (data) => {
  return {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      trigger: "axis",
    },
    xAxis: {
      type: "category",
      data: data.data.map((item) => item.key),
    },
    yAxis: {
      type: "value",
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    series: [
      {
        name: data.chart_info.legend,
        type: "line",
        data: data.data.map((item) => item.value),
        // itemStyle: {
        //   color: color || "#0000ff",
        // },
      },
    ],
  };
};

export const createBarChartOptions = (data) => {
  return {
    title: {
      text: data.title,
      left: "center",
      top: "3%",
    },
    tooltip: {
      trigger: "axis",
    },
    xAxis: {
      type: "category",
      data: data.data.map((item) => item.key),
    },
    yAxis: {
      type: "value",
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    series: [
      {
        name: data.chart_info.legend,
        type: "bar",
        data: data.data.map((item) => ({ value: item.value, name: item.key })),
        showBackground: true,
        backgroundStyle: {
          color: "rgba(180, 180, 180, 0.2)",
        },
        label: {
          show: true,
          position: "inside",
          color: "#fff",
        },
        axisTick: {
          alignWithLabel: true,
        },
      },
    ],
  };
};

export const createPieChartOptions = (title, data, legendLabel, color) => {
  return {
    title: {
      text: title,
      left: "center",
    },
    tooltip: {
      trigger: "item",
      formatter: "{a} <br/>{b} : {c} ({d}%)",
    },
    legend: {
      orient: "vertical",
      left: "left",
      data: data.map((item) => item[legendLabel]),
    },
    series: [
      {
        name: legendLabel,
        type: "pie",
        radius: "55%",
        center: ["50%", "60%"],
        data: data.map((item) => ({
          value: item.value,
          name: item[legendLabel],
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
        },
      },
    ],
  };
};
