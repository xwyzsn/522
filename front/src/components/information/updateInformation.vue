<template>
    <div class="w-full h-full">
        <el-form label-width="100px">
            <el-form-item v-for=" (item, idx) in formData" :key="idx" :label="item.label">
                <el-input v-model="item.value" :disabled="item.diable"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleClick">提交</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
 
<script setup>
import { ref } from 'vue'
import { api } from '../../boot/api';
import { ElMessage } from 'element-plus';
const props = defineProps({
    data: {
        type: Object,
        default: {},
        required: true
    },
    url: {
        type: String
    }
})
// 
let formData = ref([])
let mapping = {
    uid: '用户ID',
    username: '用户名',
    tel: '联系方式',
    email: '邮箱',
    password: '密码',
    role: '角色'
}

Object.entries(props.data).forEach(([key, value]) => {


    // if value is Array, then push each item to formData
    console.log(Array.isArray(value))
    if (Array.isArray(value)) {
        formData.value.push({
            key: key,
            value: value[0],
            diable: value[1],
            label: value[2]
        })
    } else {
        formData.value.push({
            key: key,
            value: value,
            label: mapping[key]
        })
    }
})
const handleClick = () => {
    let postData = {}
    formData.value.forEach(item => {
        postData[item.key] = item.value
    })
    api.post(props.url, postData).then((res) => {
        let response = res.data
        if (response.code === 200) {
            ElMessage.success(response.msg)
        } else {
            ElMessage.error(response.msg)
        }
    })
}

</script> 
 
<style scoped></style>