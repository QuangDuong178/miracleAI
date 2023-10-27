<script lang="ts" setup>
const props = defineProps<{
  msg: string
}>()
const emit = defineEmits(['handleClickSend'])

const handleClick = () => {
  emit("handleClickSend", props.msg)
}
</script>

<template>
  <div class="flex justify-end my-2 ml-6 caret-transparent">
    <div class="chat p-3 text-black flex content-around items-center">
      <span @click="handleClick">
        {{ msg }}
      </span>

      <!--            <img src="public/right-arrow.png" alt=""/>-->
    </div>
  </div>
</template>

<style scoped>
.chat {
  border-radius: 20px;
  background-color: #FFE500;
  width: fit-content;
  max-width: 90%;
  white-space: pre-line;
  overflow-wrap: break-word;
}

.chat::after {
  content: url("@/assets/img/right-arrow.png");
  padding-left: 11px;
}
</style>