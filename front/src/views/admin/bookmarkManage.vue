<template>
    <div class="w-full h-full">
        <div class="grid grid-cols-3 gap-4">
            <div v-for="room in room_info" :key="room.room_id">
                <el-card :body-style="{ padding: '0px' }">
                    <img class=" h-44 w-full" :src="room.room_cover_pic" />
                    <div style="padding: 14px" class="flex">
                        <div class="flex-1 space-y-2">
                            <div><span class=" text-2xl">{{ room.room_name }}</span></div>
                            <div><span class=" text-sm dark:text-white">{{ room.room_desc }}</span></div>
                        </div>
                        <div class="mt-2">
                            <el-button text type="primary " @click="cancel(room)">取消收藏</el-button>
                        </div>
                    </div>
                </el-card>
            </div>
        </div>
    </div>
</template>
 
<script setup>
import { ref } from 'vue'
import { api, axios } from '../../boot/api';
import { ElMessage } from 'element-plus'
let data = ref([])
let room_ids = ref([])
let info = JSON.parse(localStorage.getItem('info'))
let room_info = ref([])
api.get('/bookmark/get_bookmark_by_uid/' + info.uid).then(res => {
    let response = res.data;
    if (response.code == 200) {
        data.value = response.data;
        data.value.forEach(item => {
            room_ids.value.push(item.room_id)
        })
        if (room_ids.value.length == 0) {
            return
        }
        // concat room_ids 
        let s = room_ids.value.join(',')
        api.get('/room/get_by_roomid_list?rid_list=' + s).then(res => {
            let response = res.data
            if (response.code == 200) {
                room_info.value = response.data
            }
        })
    }
})
const cancel = (room) => {
    let payload = {
        uid: info.uid,
        room_id: room.rid,
        bid: null
    }
    api.post('/bookmark/delete_bookmark', payload).then(res => {
        let response = res.data
        if (response.code == 200) {
            ElMessage.success('取消收藏成功')
            room_info.value = room_info.value.filter(item => item.rid != room.rid)
        } else {
            ElMessage.error('取消收藏失败')
        }
    })
}
</script> 
 
<style scoped></style>