<template>
  <div>
    <template v-for="(item, index) in items" :key="index">
      <!-- Render Divider -->
      <div
        class="Divider"
        v-if="item.type === 'divider'"
        :key="`divider${index}`"
      />
      <!-- Else render menu items -->
      <MenuItem v-else v-bind="item" />
    </template>
  </div>
</template>
<script setup>
import { computed, onMounted } from "vue";
import MenuItem from "./MenuItem.vue";

// Define props
const props = defineProps({
  editor: {
    type: Object,
    required: true,
  },
});

// Computed property for menu items configuration
const items = computed(() => [
  {
    icon: "mdi-format-bold",
    title: "Bold",
    action: () => props.editor.chain().focus().toggleBold().run(),
    isActive: () => props.editor.isActive("bold"),
  },
  {
    icon: "mdi-format-italic",
    title: "Italic",
    action: () => props.editor.chain().focus().toggleItalic().run(),
    isActive: () => props.editor.isActive("italic"),
  },
  {
    icon: "mdi-format-strikethrough",
    title: "Strike",
    action: () => props.editor.chain().focus().toggleStrike().run(),
    isActive: () => props.editor.isActive("strike"),
  },
  {
    icon: "mdi-code-tags",
    title: "Code",
    action: () => props.editor.chain().focus().toggleCode().run(),
    isActive: () => props.editor.isActive("code"),
  },
  {
    type: "divider",
  },
  {
    icon: "mdi-format-header-1",
    title: "Heading 1",
    action: () =>
      props.editor.chain().focus().toggleHeading({ level: 1 }).run(),
    isActive: () => props.editor.isActive("heading", { level: 1 }),
  },
  {
    icon: "mdi-format-header-2",
    title: "Heading 2",
    action: () =>
      props.editor.chain().focus().toggleHeading({ level: 2 }).run(),
    isActive: () => props.editor.isActive("heading", { level: 2 }),
  },
  {
    icon: "mdi-format-paragraph",
    title: "Paragraph",
    action: () => props.editor.chain().focus().setParagraph().run(),
    isActive: () => props.editor.isActive("paragraph"),
  },
  {
    icon: "mdi-format-list-bulleted",
    title: "Bullet List",
    action: () => props.editor.chain().focus().toggleBulletList().run(),
    isActive: () => props.editor.isActive("bulletList"),
  },
  {
    icon: "mdi-format-list-numbered",
    title: "Ordered List",
    action: () => props.editor.chain().focus().toggleOrderedList().run(),
    isActive: () => props.editor.isActive("orderedList"),
  },
  {
    icon: "mdi-code-block-tags",
    title: "Code Block",
    action: () => props.editor.chain().focus().toggleCodeBlock().run(),
    isActive: () => props.editor.isActive("codeBlock"),
  },
  {
    type: "divider",
  },
  {
    icon: "mdi-format-align-left",
    title: "Left Align",
    action: () => props.editor.chain().focus().setTextAlign("left").run(),
    isActive: () => props.editor.isActive({ textAlign: "left" }),
  },
  {
    icon: "mdi-format-align-center",
    title: "Center Align",
    action: () => props.editor.chain().focus().setTextAlign("center").run(),
    isActive: () => props.editor.isActive({ textAlign: "center" }),
  },
  {
    icon: "mdi-format-align-right",
    title: "Right Align",
    action: () => props.editor.chain().focus().setTextAlign("right").run(),
    isActive: () => props.editor.isActive({ textAlign: "right" }),
  },
  {
    type: "divider",
  },
  {
    icon: "mdi-format-quote-open",
    title: "Blockquote",
    action: () => props.editor.chain().focus().toggleBlockquote().run(),
    isActive: () => props.editor.isActive("blockquote"),
  },
  {
    icon: "mdi-minus",
    title: "Horizontal Rule",
    action: () => props.editor.chain().focus().setHorizontalRule().run(),
  },
  {
    type: "divider",
  },
  {
    icon: "mdi-format-text-wrapping-wrap",
    title: "Hard Break",
    action: () => props.editor.chain().focus().setHardBreak().run(),
  },
  {
    icon: "mdi-format-clear",
    title: "Clear Format",
    action: () =>
      props.editor.chain().focus().clearNodes().unsetAllMarks().run(),
  },
  {
    type: "divider",
  },
  {
    icon: "mdi-undo",
    title: "Undo",
    action: () => props.editor.chain().focus().undo().run(),
    disabled: !props.editor.can().undo(), // TODO: Not working properly
  },
  {
    icon: "mdi-redo",
    title: "Redo",
    action: () => props.editor.chain().focus().redo().run(),
    disabled: !props.editor.can().redo(), // TODO: Not working properly
  },
]);
</script>
<style lang="scss">
.Divider {
  background-color: rgba(#000000, 0.25);
  height: 1.25rem;
  margin-left: 0.5rem;
  margin-right: 0.75rem;
  width: 1px;
}
</style>
