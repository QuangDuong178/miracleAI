<script lang="ts" setup>

import {ref} from "vue";
import {RENDER_TIME} from "@/constant/constant";

const props = defineProps<{
  msg: object
}>()
const emit = defineEmits(['finishRender']);


</script>

<template>
  <div class="mr-auto flex space-x-4 my-2 caret-transparent">
    <div class="char-by-char chat-text rounded-xl chat p-2 py-4 text-black">
      {{ props.msg.message }}
    </div>
  </div>
</template>

<style scoped>
.chat {
  border-radius: 20px 20px 20px 2px;
  background-color: white;
  width: fit-content;
  max-width: 90%;
  white-space: pre-line;
  overflow-wrap: break-word;
}

p {
  white-space: pre-line;
}

.char-by-char {
  display: inline-block;
  opacity: 0;
  transform: translateY(10px);
  animation: charFadeIn 0.5s ease-out forwards;
}

@keyframes charFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>