<script setup>
</script>

<template>
  <VApp>
    <LoaderComponent /> <!-- It is a global component so, no need to register or import. -->
    <RouterView />
  </VApp>
</template>


<style scoped>
:deep(.ag-root-wrapper) {
  border: none !important;
}

:deep(.ag-header) {
  background-color: white !important;
  border-bottom: 1px solid #ddd !important;
  font-weight: bold !important;
}

:deep(.ag-header-cell) {
  background-color: white !important;
  font-size: smaller !important;
}

:deep(.ag-cell) {
  font-size: smaller !important;
}
</style>

<style>
.ag-root ::-webkit-scrollbar {
  width: 6px;
  height: 6px;
  border-radius: 10px;
}

/* Remove scrollbar arrows */
.ag-root ::-webkit-scrollbar-button {
  display: none;
}

/* Scrollbar track (background) */
.ag-root ::-webkit-scrollbar-track-piece {
  background: #f1f1f1;
  /* Light gray for a soft background */
  border-radius: 10px;
}

/* Scrollbar thumb (draggable part) */
.ag-root ::-webkit-scrollbar-thumb {
  background: #a0a0a0;
  /* Medium gray */
  border-radius: 10px;
}

/* Hover effect */
.ag-root ::-webkit-scrollbar-thumb:hover {
  background: #808080;
  /* Darker gray for contrast */
}

/* .ag-icon-asc {
    content: &#xF460;
    color: green;
}

.ag-icon-desc {
  color: red;
} */
</style>
