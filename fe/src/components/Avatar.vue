<script lang="ts" setup>

const props = defineProps<{
  master: object
}>();

</script>
<template>
  <div class="avatar">
    <el-avatar :size="90" class="el-avatar" :src="props.master?.avatar"/>
    <h1 class="text-black">{{ props.master.name }}</h1>
  </div>
</template>


<style scoped>
h1 {
  color: #000;
  font-family: Noto Sans;
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  padding-right: 7px;
  padding-bottom: 5px;
  padding-top: 6px;
}

.avatar {
  text-align: center;
}

</style>