<script lang="ts" setup>

</script>

<template>

  <div class="flex space-x-4 my-5 caret-transparent">
    <div class="chat text-black p-5">
      <div class="bounce1 mx-1">.</div>
      <div class="bounce2 mx-1">.</div>
      <div class="bounce3 mx-1">.</div>
    </div>
  </div>
</template>

<style scoped>
.chat {
  border-radius: 20px 20px 20px 2px;
  background-color: white;
  width: 100%;
  display: flex;
  align-items: start;
  justify-content: start;
}

.bounce1 {
  animation: bounce 2s ease infinite;
  animation-delay: -0.32s;
}

.bounce2 {
  animation: bounce 2s ease infinite;
  animation-delay: -0.16s;
}

.bounce3 {
  animation: bounce 2s ease infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-10px);
  }
}

</style>