<template>
    <div class="w-full h-full">
        <UpdateInformation :data="formData" url="/user/update"></UpdateInformation>
    </div>
</template>
 
<script setup>
import { ref } from 'vue'
import UpdateInformation from '../../components/information/updateInformation.vue';
let formData = ref(null)

let info = JSON.parse(localStorage.getItem('info'))
let uid = info.uid
let username = info.username
let tel = info.tel
let email = info.email
let password = info.password
let role = info.role
formData.value = {
    uid: [uid, true, '用户ID'],
    username: [username, false, '用户名'],
    tel: [tel, false, '联系方式'],
    email: [email, false, '邮箱'],
    password: [password, false, '密码'],
    role: [role, true, '角色']
}

</script> 
 
<style scoped></style>