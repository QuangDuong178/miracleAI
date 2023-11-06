<script lang="ts" setup>
import MessageBot from "@/components/box_chat/MessageBot.vue";
import MessageUser from "@/components/box_chat/MessageUser.vue";
import {onMounted, onUpdated, ref, watch} from "vue";
import {BOT_GUIDE, BOT_TYPE, SAMPLE_QUESTION, USER_TYPE} from "@/constant/MessageType";
import axios from "axios";
import {masterListMessages, messageDefault, questionSampleDefault} from "@/data/ConversationList";
import MessageLoading from "@/components/box_chat/MessageLoading.vue";
import TextMessageV2 from "@/components/box_chat/TextMessage.vue";
import MessageGuide from "@/components/box_chat/MessageGuide.vue";
import {API_BASE_PATH} from "@/constant/api";
import {MESSAGE_ROLE, RENDER_TIME} from "@/constant/constant";

const props = defineProps<{
  master: object,
  resetConversation: boolean
}>()

const currentMaster = ref(masterListMessages.find(master => master.id === props.master.id))
const elementList = ref(new Map([
  [props.master.id, currentMaster.value.messages],
]));

const scrollHeight = ref(0);
const messageGuideWaiting = ref(masterListMessages.map(master => master.id));
const messageWaitingIdList = ref([])
const openai_model_version = new URL(location.href).searchParams.get('model')
const messageRendering = ref(false);

watch(() => props.master, () => {
  currentMaster.value = masterListMessages.find(master => master.id === props.master.id)
  elementList.value.set(props.master.id, currentMaster.value.messages);
  initMasterConversation(props.master.id);
  const messagebox = document.getElementById("boxMessage")

  if (messagebox) {
    scrollHeight.value = messagebox.scrollHeight;
  }
});

watch(() => props.resetConversation, () => {
  if (!messageWaitingIdList.value.some(item => item === props.master.id) &&
      !messageGuideWaiting.value.some(item => item === props.master.id)) {
    currentMaster.value!.messages = [];
    elementList.value.delete(props.master.id);
    messageGuideWaiting.value.push(props.master.id)
    initMasterConversation(props.master.id);
  }

});

onUpdated(() => {
  const messagebox = document.getElementById("boxMessage")

  if (messagebox) {
    scrollHeight.value = messagebox.scrollHeight;
  }
})

const handleSuggestion =  (messageGuides: Array<object>, masterId: number) => {
  const messageDefault = messageGuides.slice();
  return new Promise((resolve, reject) => {
    elementList.value.get(masterId).push(messageDefault[0])
    setTimeout(() => {
      elementList.value.get(masterId).push(messageDefault[1])
    }, (RENDER_TIME * messageDefault[0].message.length));

    setTimeout(() => {
      elementList.value.get(masterId).push(messageDefault[2])

    }, (RENDER_TIME * (messageDefault[0].message.length + messageDefault[1].message.length)));

    setTimeout(() => {
      messageGuideWaiting.value = messageGuideWaiting.value.filter(item => item !== masterId)
      resolve();
    }, (RENDER_TIME * (messageDefault[0].message.length + messageDefault[1].message.length + messageDefault[2].message.length)));
  });
}

const initMasterConversation = async (masterId) => {
  if (!elementList.value.has(masterId)) {
    elementList.value.set(masterId, [])

  }
  if (elementList.value.get(masterId).length === 0) {
    await handleSuggestion(messageDefault, masterId);
    elementList.value.get(masterId).push(...questionSampleDefault)
  }
}

const handleSendMessage = async (message: string) => {
  const id = props.master.id;
  elementList.value.set(id, elementList.value.get(id).filter(item => item.type !== SAMPLE_QUESTION));
  elementList.value.get(id).push({type: USER_TYPE, message: message, role: MESSAGE_ROLE.HUMAN})
  const index = masterListMessages.findIndex(item => item.id === id);
  const conversationHistory = elementList.value.get(id).filter(item => item.type !== BOT_GUIDE);
  if (index > -1) {
    masterListMessages[index].messages = elementList.value.get(id);
  }

  messageWaitingIdList.value.push(id);
  await axios
      .post(API_BASE_PATH + "chat-bot/send-message/",
          {
            'history_messages': conversationHistory,
            'masterId': id,
            'model': openai_model_version,
          })
      .then(response => {
        if (response.data) {

          let data = response.data;

          data = data.replace("NO", "")

          elementList.value.get(id).push({
            type: BOT_TYPE,
            role: MESSAGE_ROLE.BOT,
            message: data
          });

        }
      })
      .catch(error => {
        console.log(error)
      })
      .finally(() => {
        messageRendering.value = true
        messageWaitingIdList.value = messageWaitingIdList.value.filter(item => item !== id)
      })
}

watch(scrollHeight, (value, oldValue) => {
  const messagebox = document.getElementById("boxMessage");
  if (messagebox) {
    messagebox.scrollTo(0, value);
  }
}, {
  immediate: true
})

onMounted(() => {
  initMasterConversation(props.master.id)
  const header = document.getElementById("header");
  const boxMessage = document.getElementById("boxMessage");
  const clientHeight = document.documentElement.clientHeight;
  const textMessage = document.getElementById("text-message");
  if (header && boxMessage && textMessage && clientHeight) {
    boxMessage.style.height = 'calc(' + clientHeight + 'px - ' + header.offsetHeight + 'px - ' + textMessage.offsetHeight + 'px)';
  }
})

const finishRender = () => {
  messageRendering.value = false;
}
</script>


<template>
  <div class="box">
    <div class="box_chat text-xs">
      <div id="boxMessage" class="message_box bg-scroll ">
        <div>
          <template v-for="(e, index) in elementList.get(props.master.id)">
            <Transition v-if="e.type === BOT_GUIDE" name="fade" mode="out-in" appear>
              <MessageBot class="bot-guide" :msg="e"/>
            </Transition>
            <Transition v-else-if="e.type === SAMPLE_QUESTION" name="fade" mode="out-in" appear>
              <MessageGuide :msg="e.message" @handleClickSend="handleSendMessage"/>
            </Transition>
            <MessageUser v-else-if="e.type === USER_TYPE" :msg="e.message"/>
            <Transition name="slide-up" mode="out-in" appear>
              <MessageBot @finish-render="finishRender" class="chat-bot-message" v-if="e.type === BOT_TYPE" :msg="e"/>
            </Transition>

          </template>
          <MessageLoading v-if="messageWaitingIdList.includes(props.master.id)"/>
        </div>
      </div>
    </div>
    <div id="text-message">
      <TextMessageV2 placeholder="" msg=""
                     :messageWaiting="messageWaitingIdList.includes(props.master.id)
                       || messageGuideWaiting.includes(props.master.id) || messageRendering"
                     @handleClickSend="handleSendMessage"/>
    </div>
  </div>

</template>

<style scoped>

#text-message {
  background: white;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  max-height: 40vh;
  min-height: 5vh;
  z-index: 1;
}

.message_box {
  overflow-y: auto;
  overflow-anchor: auto
}

.box {
  height: 100%;
}

.box_chat {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin: auto;
  border-radius: 10px;
}

.message_box::-webkit-scrollbar-track {
  display: none;
}

.message_box::-webkit-scrollbar {
  display: none;
}

.message_box::-webkit-scrollbar-thumb {
  display: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.7s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.chat-bot-message {
  overflow-y: hidden;
}

.slide-up-enter-active {
  max-height: 10rem;
  transition: max-height 0.5s linear;
}

.slide-up-enter-from,
.slide-up-leave-to {
  max-height: 2rem;
}
</style>