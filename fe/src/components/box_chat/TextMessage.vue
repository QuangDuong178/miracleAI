<script lang="ts" setup>
import {onMounted, ref} from "vue";

const props = defineProps<{
  placeholder: string,
  messageWaiting: boolean
}>()
const message = ref('');
const emit = defineEmits(['handleClickSend'])
const send = () => {
  if (message.value.innerText.trim() === "") {
    message.value.innerText = "";
    return;
  }
  emit('handleClickSend', message.value.innerText.trim());
  message.value.innerText = '';
}

const sendEnable = ref(true);
const breakLine = (event: KeyboardEvent) => {
  if (event.key === "Enter" && !props.messageWaiting && !event.shiftKey && sendEnable.value) {
    event.preventDefault();
    send();
  }
}

onMounted(() => {
  const inputElement = document.getElementById("message");

  inputElement?.addEventListener("compositionstart", (event) => {
    sendEnable.value = false
  })
  inputElement?.addEventListener("compositionend", () => {
    sendEnable.value = true
  })
})

</script>

<template>
  <el-row class="input_box">
    <el-col :span="21" class="pr-1.5 pl-3 h-100">
      <span role="textbox" id="message" class="textarea message_input py-1 my-1 h-100" v-on:keydown="breakLine"
            contenteditable ref="message"></span>
    </el-col>
    <el-col :span="3" class="">
      <img src="@/assets/img/send.png" class="btn_send" @click="messageWaiting ? null : send()"/>
    </el-col>
  </el-row>
</template>

<style scoped>

.input_box {
  height: 100%;
  width: 100%;
  align-items: center;
  overflow-y: hidden;
}

.message_input {
  display: block;
  border-radius: 10px;
  background: #F5F5F5;
  resize: none;
  width: 100%;
  font-size: 16px;
  outline: none;
  color: black;
  margin-top: 15px;
  margin-bottom: 14px;
  padding-left: 5px;
  max-height: 35vh;
  overflow-y: auto;
}

.btn_send {
  margin-bottom: 5px;
  margin-right: 9px;
  margin-left: 10px;
}

</style>