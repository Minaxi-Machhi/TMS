<script setup>
// internal imports
import { reactive, toRefs, computed, onMounted, onBeforeUnmount, watchEffect, watch, } from "vue";

// external imports
import StarterKit from "@tiptap/starter-kit";
import { useTheme } from "vuetify";
import MenuBar from "./MenuBar.vue";
import TextAlign from "@tiptap/extension-text-align";
import Placeholder from "@tiptap/extension-placeholder";
import { Editor, EditorContent } from "@tiptap/vue-3";

// Define props
const props = defineProps({
  modelValue: {
    type: String,
  },
  placeholder: {
    type: String,
    default: "",
  },
  width: {
    type: String,
    default: "70%",
  },
  readonly: {
    type: Boolean,
    default: false,
  },
});


// variables or states
const vuetifyTheme = useTheme();

const state = reactive({
  editor: null,
});

const { editor } = toRefs(state);

/*
===========================  Define emits ===========================
*/

const emit = defineEmits(["update:modelValue", "blur", "focus"]);

// custom method to handel focus behaviour of editor field
const handleFocus = () => {
  emit("focus");
};

// custom method to handel blur behaviour of editor field
const handleBlur = () => {
  emit("blur");
};


/*
=========================== watchers ================================
*/


// handelling editable feature based on readonly prop.
watch(props, () => {
  if (props.readonly === false) {
    state.editor.options.editable = true;
  }
  else {
    state.editor.options.editable = false;
  }
})

// Watch for changes in modelValue
watchEffect(() => {
  if (state.editor && props.modelValue !== state.editor.getHTML()) {
    state.editor.commands.setContent(props.modelValue, false, {
      preserveWhitespace: "full",
    });
  }
});

/*
=========================== Computed Properties ===========================
*/

// Computed property for CSS props
const cssProps = computed(() => ({
  "--editor-width": props.width,
}));

// Computed property for dynamic styles based on the theme
const dynamicStyles = computed(() => {
  const isDark = vuetifyTheme.global.current.value.dark;
  return {
    headerBackgroundColor: isDark ? "#3A3E5B" : "#ffffff",
    headerBorderColor: isDark ? "#616161" : "#0d0d0d36",
    contentBackgroundColor: isDark ? "#2B2C40" : "#ffffff",
    contentColor: isDark ? "#ffffff" : "#0d0d0d",
  };
});

/*
===================================================================
*/

// method to initialize the editor instance
const initializeEditor = () => {
  state.editor = new Editor({
    content: props.modelValue,
    editable: !props.readonly, // Set editable based on readonly prop
    parseOptions: {
      preserveWhitespace: "full",
    },
    editorProps: {
      attributes: {
        spellcheck: "false",
      },
      handleDOMEvents: {
        focus: () => {
          handleFocus();
          return false;
        },
        blur: () => {
          handleBlur();
          return false;
        },
      },
    },
    onUpdate: ({ editor }) => {
      const htmlValue = editor.getHTML();
      emit("update:modelValue", htmlValue);
    },
    extensions: [
      StarterKit.configure({
        history: true,
      }),
      Placeholder.configure({
        placeholder: props.placeholder,
      }),
      TextAlign.configure({
        types: ["heading", "paragraph"],
        alignments: ["left", "right", "center"],
      }),
    ],
  });
}

// Lifecycle hooks
onMounted(() => {
  initializeEditor();
});

onBeforeUnmount(() => {
  if (state.editor) {
    state.editor.destroy();
  }
});

/* 
  if we want to use [Element: focusin event] -----> https://developer.mozilla.org/en-US/docs/Web/API/Element/focusin_event

<template>
  <div class="editor" v-if="editor" :style="cssProps" @focusin="handleFocusIn" @focusout="handleFocusOut">
    <MenuBar class="editor__header" :editor="editor" :style="{ 
      backgroundColor: dynamicStyles.headerBackgroundColor,
      borderBottomColor: dynamicStyles.headerBorderColor
    }" />
    <EditorContent class="editor__content tiptap" :editor="editor" :style="{ 
      backgroundColor: dynamicStyles.contentBackgroundColor,
      color: dynamicStyles.contentColor 
    }" />
  </div>
</template>

const handleFocusIn = () => {
  state.isFocused = true;
};

const handleFocusOut = () => {
  if (state.isFocused) {
    emit('blur');
    state.isFocused = false;
  }
};
*/

</script>

<template>
  <div class="editor" v-if="editor" :style="cssProps">
    <MenuBar class="editor__header" :editor="editor" :style="{
      backgroundColor: dynamicStyles.headerBackgroundColor,
      borderBottomColor: dynamicStyles.headerBorderColor,
    }" v-if="!props.readonly" />
    <EditorContent class="editor__content tiptap" :editor="editor" :style="{
      backgroundColor: dynamicStyles.contentBackgroundColor,
      color: dynamicStyles.contentColor,
    }" />
  </div>
</template>

<style lang="scss">
.editor {
  border: 2px solid #0d0d0d18;
  border-radius: 0.3rem;
  display: flex;
  flex-direction: column;
  max-width: var(--editor-width);

  &__header {
    align-items: center;
    border-bottom: 2px solid;
    border-top-left-radius: 0.5rem;
    border-top-right-radius: 0.5rem;
    display: flex;
    flex: 0 0 auto;
    flex-wrap: wrap;
    padding: 0.25rem;
  }

  &__content {
    flex: 1 1 auto;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 1.25rem 1rem;
    -webkit-overflow-scrolling: touch;

    /* Fix for cursor getting hidden for no text, and space getting stripped from sides */
    &>.ProseMirror {
      padding: 2px;
      white-space: normal;
      word-break: break-word;
    }
  }
}

/* Basic editor styles */
.tiptap {
  >*+* {
    margin-top: 0.75em;
  }

  /* Placeholder (at the top) */
  & p.is-editor-empty:first-child::before {
    color: #adb5bd;
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;
  }

  ul,
  ol {
    padding: 0 1rem;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
  }

  code {
    background-color: rgba(#616161, 0.1);
    color: #616161;
  }

  pre {
    background: #0d0d0d;
    border-radius: 0.5rem;
    color: #fff;
    padding: 0.75rem 1rem;

    code {
      background: none;
      color: inherit;
      font-size: 0.8rem;
      padding: 0;
    }
  }

  mark {
    background-color: #faf594;
  }

  img {
    height: auto;
    max-width: 100%;
  }

  hr {
    margin: 1rem 0;
  }

  blockquote {
    border-left: 2px solid rgba(#0d0d0d, 0.1);
    padding-left: 1rem;
  }

  hr {
    border: none;
    border-top: 2px solid rgba(#0d0d0d, 0.1);
    margin: 2rem 0;
  }

  ul[data-type="taskList"] {
    list-style: none;
    padding: 0;

    li {
      align-items: center;
      display: flex;

      >label {
        flex: 0 0 auto;
        margin-right: 0.5rem;
        user-select: none;
      }

      >div {
        flex: 1 1 auto;
      }
    }
  }
}
</style>
