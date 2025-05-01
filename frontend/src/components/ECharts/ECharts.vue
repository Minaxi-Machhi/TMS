  <template>
  <div ref="chart" :style="{ width: '100%', height: height }" autoresize></div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import * as echarts from "echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { useTheme } from "vuetify";

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

const props = defineProps({
  options: Object,
  height: {
    type: String,
    default: "400px",
  },
});

const chart = ref(null);
let myChart;

// Retrieve and watch the Vuetify theme
const vuetifyTheme = useTheme();
const theme = computed(() => vuetifyTheme.global.current.value.dark ? 'dark' : 'light');

// Initialize the chart
function initializeChart() {
  if (chart.value) {
    if (myChart) {
      myChart.dispose();
    }
    myChart = echarts.init(chart.value, theme.value);
    if (props.options) {
      myChart.setOption(props.options);
    }
  }
}

onMounted(() => {
  initializeChart();
});

watch(
  () => props.options,
  (newOptions) => {
    if (myChart) {
      myChart.setOption(newOptions);
    }
  },
  { deep: true }
);

watch(
  theme,
  () => {
    initializeChart();
  }
);
</script>

<style scoped>
</style>
