<script lang="ts">

import {defineComponent, ref} from "vue";
import MasterAvatar from "@/components/box_chat/MasterAvatar.vue";
import BoxChat from "@/components/box_chat/BoxChat.vue";

import axios from "axios";
import {API_BASE_PATH} from "@/constant/api";
import {masterListMessages} from "@/data/ConversationList";
import Avatar from "@/components/Avatar.vue";

export default defineComponent ({
  components: {Avatar, MasterAvatar, BoxChat},
  setup() {
    const masterList = ref([]);
    const showMasterListFlag = ref(false);
    const currentMaster = ref(null);
    const resetConversation = ref(false);

    return {
      masterList, currentMaster, showMasterListFlag, resetConversation
    }
  },
  methods: {
    selectMaster() {
      this.showMasterListFlag = !this.showMasterListFlag;
    },
    handleSelectMaster(master) {
      this.currentMaster = master;

      this.selectMaster();
    },
    handleResetConversation() {
      this.resetConversation = !this.resetConversation;
    },
    async initScreen() {
      await axios
          .get(API_BASE_PATH + "chat-bot/masters/")
          .then(response => {
            this.masterList = response.data;
            this.masterList.forEach((master) => {
              masterListMessages.push({
                id: master.id,
                messages: []
              })
            })
            this.currentMaster = this.masterList.length > 0 ? this.masterList[0] : null;
          })
          .catch(error => {
            console.log(error)
          });
    }
  },
  mounted() {
    this.initScreen();
  }
})

</script>

<template>
  <div class="common-layout px-4">
    <div v-if="showMasterListFlag" class="enable">
      <el-icon id="exit-master-list" :size="30" color="#FFFFFF" @click="selectMaster">
        <CloseBold/>
      </el-icon>
      <MasterAvatar v-for="master in masterList" class="flex items-center master-avatar" :size="70" :master="master"
                    @open-select-master="handleSelectMaster"/>
    </div>

    <el-container id="container" class="wrapper flex flex-col">
      <el-header id="header">
        <el-row class="mt-2 justify-between py-3 pt-3">
          <el-button class="button-select-yellow change-master text-black" tag="b" @click="selectMaster">
            <div class="flex flex-col mr-2">
              <el-icon>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                  <path
                      d="M4.5 6.375a4.125 4.125 0 118.25 0 4.125 4.125 0 01-8.25 0zM14.25 8.625a3.375 3.375 0 116.75 0 3.375 3.375 0 01-6.75 0zM1.5 19.125a7.125 7.125 0 0114.25 0v.003l-.001.119a.75.75 0 01-.363.63 13.067 13.067 0 01-6.761 1.873c-2.472 0-4.786-.684-6.76-1.873a.75.75 0 01-.364-.63l-.001-.122zM17.25 19.128l-.001.144a2.25 2.25 0 01-.233.96 10.088 10.088 0 005.06-1.01.75.75 0 00.42-.643 4.875 4.875 0 00-6.957-4.611 8.586 8.586 0 011.71 5.157v.003z"/>
                </svg>
              </el-icon>
              <el-icon>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
                  <path fill-rule="evenodd"
                        d="M13.2 2.24a.75.75 0 00.04 1.06l2.1 1.95H6.75a.75.75 0 000 1.5h8.59l-2.1 1.95a.75.75 0 101.02 1.1l3.5-3.25a.75.75 0 000-1.1l-3.5-3.25a.75.75 0 00-1.06.04zm-6.4 8a.75.75 0 00-1.06-.04l-3.5 3.25a.75.75 0 000 1.1l3.5 3.25a.75.75 0 101.02-1.1l-2.1-1.95h8.59a.75.75 0 000-1.5H4.66l2.1-1.95a.75.75 0 00.04-1.06z"
                        clip-rule="evenodd"/>
                </svg>
              </el-icon>
            </div>
            AI 切替
          </el-button>
          <el-button class="button-select-yellow change-master text-black" tag="b" @click="handleResetConversation">
            <div class="flex flex-col mr-2">
              <el-icon>
                <svg xmlns="http://www.w3.org/2000/svg"
                     viewBox="0 0 512 512" style="transform: scale(-1,1)"><!--! Font Awesome Pro 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
                  <path d="M463.5 224H472c13.3 0 24-10.7 24-24V72c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1c-87.5 87.5-87.5 229.3 0 316.8s229.3 87.5 316.8 0c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0c-62.5 62.5-163.8 62.5-226.3 0s-62.5-163.8 0-226.3c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8H463.5z"/>
                </svg>
              </el-icon>
            </div>
            新規会話
          </el-button>
        </el-row>
        <el-row class="justify-center pb-2">
          <Avatar class="avatar" v-if="currentMaster" :master="currentMaster"
                  @open-select-master="selectMaster"/>
        </el-row>
      </el-header>

      <el-main>
        <BoxChat v-if="currentMaster" :master="currentMaster" :resetConversation="resetConversation"
                 :handleSelectMaster="handleSelectMaster"/>
      </el-main>

    </el-container>
  </div>
</template>

<style scoped>
#header {
  height: fit-content;
}

.common-layout {
  width: 100vw;
  max-height: 100vh;
  overflow-y: hidden;
  background-image: url('@/assets/img/background-main.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;

}

#exit-master-list {
  position: absolute;
  top: 1.5rem;
  right: 1rem;
  z-index: 2;
}

.enable {
  background: rgba(0, 0, 0, 0.80);
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 20px;
  flex-direction: column;
}

.wrapper {
  height: 100%;
  width: 100%;
}

.master-avatar {
  padding-bottom: 25px;
  padding-bottom: 25px;
  padding-top: 25px;
  width: 100%;
}

.change-master {
  width: 91px;
}
</style>
