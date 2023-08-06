<template>
    <div class="flex card bg-base-100 shadow-xl justify-center">
        <div class="card-body justify-center">
            <h2 class="card-title ">这个角色是: {{ data.role }}</h2>
            <div class="flex justify-center">
                <input v-model="data.name" type="text" placeholder="输入你的名字（选填）你不仅有机会出现在模型发布的致谢名单内，还可以抢先体验模型。" class="input w-full" />
            </div>
            <div class="flex flex-col w-full border-opacity-50">
                <div class="divider">上下文</div>
                <div v-for="v in data.prompt" :class="v.role==='旅行者'?'chat-end':'chat-start'" class="chat scale-in-ver-top">
                  <div class="chat-header">
                    {{ v.role === '旅行者' ? '旅行者' : data.role }}
                  </div>
                  <div class="chat-bubble">
                    {{ v.v }}
                  </div>
                </div>

                <div class="divider">样例回答</div>
                <div class="chat-start">
                  <div class="chat-header">
                    {{ data.role}}
                  </div>
                  <div class="chat-bubble">
                    {{ data.sample }}
                  </div>
                </div>
            </div>
            <div class="card-actions justify-center">
                <button class="btn btn-accent" @click="data.response=data.sample">复制样例回答到输入框</button>
                <button class="btn btn-accent" @click="report()">这段对话有重大问题</button>
                <button class="btn btn-secondary" @click="deny()">拒绝，请求下一条问题</button>
                <button class="btn btn-primary" @click="finish()">完成，请求下一条问题</button>
            </div>
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text">把你的回答写在这里，请务必认真回答，如果不想做这个角色，请点击拒绝，请求下一个问题。</span>
                </label>
                <textarea type="text" placeholder="请输入问题的答案" class="textarea textarea-lg textarea-bordered w-full" v-model="data.response"/>
            </div>
        </div>
    </div>
</template>
<script setup>
import {onMounted, reactive, resolveTransitionHooks} from "vue";
import {getRequest, postRequest} from '../plugin/api.js'

let data = reactive({
    id: "",
    role: "流浪者",
    prompt: [],
    sample: "这是一个样例回答",
    response: "",
    idx: -1,
    name: "",
    })
function getDocument() {
  getRequest('/api/getDocument').then((res) => {
    let document = res.data;
    const keys = Object.keys(document).filter(key => key !== "_id" && key !== "idx");
    data.id = document['_id']
    console.log(data.id)
    // 随机选择一个键
    const role = keys[Math.floor(Math.random() * keys.length)];
    data.role = role
    // 获取随机选择的角色的值
    const roleValue = document[role];
    selectFragment(roleValue, role);
  })
}
getDocument()
function selectFragment(roleValue, role)
{
  if (roleValue['idx'] >= roleValue['ai'].length || roleValue['idx'] >= roleValue['user'].length)
  {
    getDocument();
    return;
  }
  data.idx = roleValue['idx'];
  data.prompt = [];
  for (let i = 0; i < data.idx; ++i)
  {
    data.prompt.push({'role': '旅行者', 'v': roleValue['user'][i].replace(/\n+/g, '\n')});
    data.prompt.push({'role': 'ai', 'v': roleValue['ai'][i].replace(/\n+/g, '\n')});
  }
  data.prompt.push({'role': '旅行者', 'v': roleValue['user'][data.idx].replace(/\n+/g, '\n')});
  data.sample = roleValue['ai'][data.idx].replace(/\n+/g, '\n');
}

function report()
{
  postRequest('/api/report', {'id': data.id, 'role': data.role}).then((res) => {
    console.log(res);
  })
}

function deny() {
  getDocument();
}

function finish() {
  postRequest('/api/updateDatabase', {'id': data.id, 'role': data.role, 'response': data.response, 'name': data.name}).then((res) => {
    console.log(res);
  })
  getDocument();
}
</script>