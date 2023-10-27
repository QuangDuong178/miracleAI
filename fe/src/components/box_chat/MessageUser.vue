<script lang="ts" setup>
defineProps<{
  msg: string
}>()
</script>

<template>
  <div class="pl-3 ml-auto flex space-x-4 my-2 justify-end caret-transparent">
    <div class="chat p-3 text-black">
      {{ msg }}
    </div>
  </div>
</template>

<style scoped>
.chat {
  border-radius: 20px;
  background-color: #FFFDC8;
  width: fit-content;
  max-width: 90%;
  overflow-wrap: break-word;
  white-space: pre-line;
}
</style>