<script lang="ts" setup>
const props = defineProps<{
  size: number
  master: object
}>();

const emit = defineEmits(['openSelectMaster'])

const selectMaster = (master) => {
  emit('openSelectMaster', master);
}

</script>
<template>
  <el-row class="content-center pb-2">
    <el-col :span="5">
      <el-avatar :size="props.size" class="el-avatar" :src="props.master?.avatar"/>
    </el-col>
    <el-col :span="13" class="information pt-2 pl-1">
      <h1>{{ props.master?.name }}</h1>
      <p>{{ props.master?.description }}</p>
    </el-col>
    <el-col :span="6" class="text-center">
      <button class="button-select-yellow change-master text-black" @click="selectMaster(props.master)">
        切 替
      </button>
    </el-col>

  </el-row>

</template>


<style scoped>
h1 {
  color: #FFF;
  font-family: Noto Sans;
  font-size: 14px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
}

p {
  padding-top: 2px;
  color: #FFF;
  font-family: Noto Sans;
  font-size: 12px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.el-avatar {
  border: 2px solid white;
}

.change-master {
  width: 50px;
}

</style>