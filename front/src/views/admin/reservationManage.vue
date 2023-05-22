<template>
    <div class="w-full h-full">
        <el-table v-if="tableData" :data="tableData">
            <el-table-column prop="rid" label="预约ID"></el-table-column>
            <el-table-column prop="room_name" label="预约景点"></el-table-column>
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="tel" label="联系方式"></el-table-column>

            <el-table-column prop="start_datetime" label="开始时间"></el-table-column>
            <el-table-column prop="end_datetime" label="结束时间"></el-table-column>
            <el-table-column prop="status" label="状态"></el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <div class="flex">
                        <el-button type="primary" size="mini" @click="handleConfirm(scope.row)">通过</el-button>
                        <el-button type="danger" size="mini" @click="handleReject(scope.row)">拒绝</el-button>
                    </div>
                </template>
            </el-table-column>

        </el-table>

    </div>
</template>
 
<script setup>
import { ref } from 'vue'
import { api } from '../../boot/api';
import { ElMessage } from 'element-plus';
import dayjs from 'dayjs'
let tableData = ref([])
const fetchAll = () => {
    api.get('/reservation/get_all').then(res => {
        let response = res.data
        if (response.code === 200) {
            tableData.value = response.data
            console.log(tableData.value)
            tableData.value.forEach(item => {
                item.start_datetime = dayjs(item.start_datetime).format('YYYY-MM-DD HH:mm:ss')
                item.end_datetime = dayjs(item.end_datetime).format('YYYY-MM-DD HH:mm:ss')
            })
        }
    })
}
fetchAll()

let handleConfirm = (row) => {
    api.post('/reservation/update', {
        rid: row.rid,
        uid: row.uid,
        username: row.username,
        tel: row.tel,
        start_datetime: row.start_datetime,
        end_datetime: row.end_datetime,
        room_id: row.room_id,
        room_name: row.room_name,
        status: '已通过'

    }).then(res => {
        let response = res.data
        if (response.code === 200) {
            ElMessage.success(response.msg)
        } else {
            ElMessage.error(response.msg)
        }
        fetchAll()

    })
}
let handleReject = (row) => {
    api.post('/reservation/update', {
        rid: row.rid,
        uid: row.uid,
        username: row.username,
        tel: row.tel,
        start_datetime: row.start_datetime,
        end_datetime: row.end_datetime,
        room_id: row.room_id,
        room_name: row.room_name,
        status: '已拒绝'

    }).then(res => {
        let response = res.data
        if (response.code === 200) {
            ElMessage.success(response.msg)
        } else {
            ElMessage.error(response.msg)
        }
        fetchAll()

    })
}

</script> 
 
<style scoped></style>