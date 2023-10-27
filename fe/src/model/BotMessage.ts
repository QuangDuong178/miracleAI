import type {Ref, UnwrapRef} from "vue";

export interface BotMessage {
    id : number,
    avatar : string,
    name: string,
    messageList: Ref<UnwrapRef<{ type: string, message: string }[]>>
}
