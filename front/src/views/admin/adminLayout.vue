<template>
    <div class="w-full h-full">
        <el-container class="w-full h-full">
            <el-header class="flex place-content-center justify-around bg-slate-400 dark:bg-black ">
                <div class="mt-2 flex-1">
                    <img class=" dark:text-white text-white" src="../../assets/arnaya_logo.png" width="200">
                </div>
                <div
                    class="flex justify-evenly content-center place-content-center space-x-4 items-center place-items-center">
                    <el-icon class=" cursor-pointer" @click="switchMode" v-if="mode == 'dark'">
                        <Moon />
                    </el-icon>
                    <el-icon class=" cursor-pointer" @click="switchMode" v-else>
                        <Sunny />
                    </el-icon>
                    <el-icon class=" cursor-pointer" @click="gotoIndexPage">
                        <Menu />
                    </el-icon>
                </div>
            </el-header>
            <el-container class="w-full h-full">
                <el-aside class="dark:bg-black bg-slate-400" width="200px">
                    <el-menu class="w-full h-full dark:bg-black bg-slate-400" :default-active="defaultActivate"
                        active-text-color="#ffd04b" router>
                        <el-menu-item v-if="admin" index="1" :route="{ name: 'usermanagement' }">
                            <el-icon>
                                <location />
                            </el-icon>
                            人员管理
                        </el-menu-item>
                        <el-menu-item v-if="admin" index="2" :route="{ name: 'roommanagement' }">
                            <el-icon>
                                <location />
                            </el-icon>
                            景点管理
                        </el-menu-item>
                        <el-menu-item index="3" v-if="admin" :route="{ name: 'reservationmanagement' }">
                            <el-icon>
                                <location />
                            </el-icon>
                            预约管理
                        </el-menu-item>
                        <el-menu-item index="4" :route="{ name: 'personmanagement' }">
                            <el-icon>
                                <location />
                            </el-icon>
                            个人信息管理
                        </el-menu-item>
                        <el-menu-item v-if="!admin" index="5" :route="{ name: 'commentmanagement' }">
                            <el-icon>
                                <location />
                            </el-icon>
                            评论发表
                        </el-menu-item>
                        <el-menu-item v-if="!admin" index="6" :route="{ name: 'bookmarkmanagement' }">
                            <el-icon>
                                <location />
                            </el-icon>
                            收藏管理
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-container class=" bg-slate-100 dark:bg-zinc-900">
                    <el-main>
                        <RouterView />
                    </el-main>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../../boot/api';

//强制刷新一次
const refresh = () => {
    window.location.reload()
    console.log('刷新')
}
onMounted(() => {
    isAdmin()

})
onUnmounted(() => {
    sessionStorage.removeItem('refres')
    localStorage.removeItem('info')
    localStorage.removeItem('token')
    // 删除cookie


})
let gotoIndexPage = () => {
    window.location.href = 'http://127.0.0.1:8000/anaya/home'
}

let mode = ref('light')
if (sessionStorage.getItem('mode')) {
    mode.value = sessionStorage.getItem('mode')
}
if (mode.value === 'dark') {
    document.querySelector('html').classList.add('dark')
}
const switchMode = () => {
    if (mode.value === 'light') {
        mode.value = 'dark'
        document.querySelector('html').classList.add('dark')
        sessionStorage.setItem('mode', 'dark')
    } else {
        mode.value = 'light'
        document.querySelector('html').classList.remove('dark')
        sessionStorage.setItem('mode', 'light')
    }
}
let defaultActivate = ref('1')
let routeMapping = [
    { url: 'usermanagement', index: '1' },
    { url: 'roommanagement', index: '2' },
    { url: 'reservationmanagement', index: '3' },
    { url: 'personmanagement', index: '4' },
    { url: 'commentmanagement', index: '5' },
    { url: 'bookmarkmanagement', index: '6' }
]
const route = useRoute()
let admin = ref('')
routeMapping.forEach(item => {
    console.log(item.url, route.name)
    if (item.url.toString() === route.name) {
        defaultActivate.value = item.index
    }
})

// 把cookie转换成对象
function cookieToObject(cookie) {
    let obj = {}
    cookie.split(';').forEach(item => {
        let [key, value] = item.split('=')
        obj[key.trim()] = value
    })
    return obj
}
let cookies = document.cookie
console.log(cookies)
let cookieObj = cookieToObject(cookies)
let uid = cookieObj.uid
const isAdmin = () => {
    let info = JSON.parse(localStorage.getItem('info'))
    if (info.role === 'admin') {
        admin.value = true
    } else {
        admin.value = false
    }

}
api.get('/user/get/' + uid).then(res => {
    let info = res.data.data
    let preInfo = JSON.parse(localStorage.getItem('info'))
    if (preInfo) {
        info.refresh = preInfo.refresh
    }
    localStorage.setItem('info', JSON.stringify(info))

}).then(() => {
    let info = JSON.parse(localStorage.getItem('info'))
    if (info.refresh === '0' || info.refresh === undefined) {
        info.refresh = '1'
        localStorage.setItem('info', JSON.stringify(info))
        refresh()
    }
    isAdmin()

})


</script> 
 
<style scoped></style>