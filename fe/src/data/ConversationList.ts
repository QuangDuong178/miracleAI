import {ref} from "vue";
import {BOT_GUIDE, BOT_TYPE, SAMPLE_QUESTION} from "@/constant/MessageType";


export const messageDefault = [
    {
        type: BOT_TYPE,
        message: '初めまして\n！' +
            '私は伊藤塾の塾長を務めている伊藤真です。'
    },
    {
        type: BOT_TYPE,
        message: '「精神面」や「勉強法」など、お困りごとにお答えし、あなたの試験ライフをサポートします。'
    },
    {
        type: BOT_TYPE,
        message: '早速、困っている事や聞いてみたい事はありますか？'
    }
]

export const questionSampleDefault = [
    {

        type: SAMPLE_QUESTION,
        message: '勉強のモチベーションを維持したい'
    },
    {

        type: SAMPLE_QUESTION,
        message: '本当に不安の時は何をしたらよい？'
    },
    {

        type: SAMPLE_QUESTION,
        message: "長期休暇で気をつけた方が良い事は\n" + "ありますか？"
    }
]

export const masterListMessages = [];