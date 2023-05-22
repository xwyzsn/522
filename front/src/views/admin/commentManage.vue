<template>
    <div class="w-full h-full">
        <el-table :data="orders">
            <el-table-column prop="room_name" label="景点名称"></el-table-column>
            <el-table-column prop="start_datetime" label="开始时间"></el-table-column>
            <el-table-column prop="end_datetime" label="结束时间"></el-table-column>
            <el-table-column prop="status" label="预约状态">
                <template #default="scope">
                    <el-tag v-if="scope.row.status == '预约申请'" type="success">{{ scope.row.status }}</el-tag>
                    <el-tag v-else-if="scope.row.status == '已通过'" type="warning">待评论</el-tag>
                    <el-tag v-else-if="scope.row.status == '已评论'" type="success">已评论</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template #default="scope">

                    <el-button v-if="scope.row.status === '预约申请'" @click="handleClick(scope.row)" type="primary"
                        link>立刻评论</el-button>
                    <el-button v-else type="primary" @click="handleClick(scope.row)" link>立刻评论</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog v-model="showModal">
            <el-form label-width="75px">
                <el-form-item label="评论内容">
                    <el-input v-model="comment" type="textarea" :rows="5" placeholder="请输入评论内容"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button>取 消</el-button>
                <el-button type="primary" @click="handleConfirm">确 定</el-button>
            </template>
        </el-dialog>
    </div>
</template>
 
<script setup>
import { ref } from 'vue'
import { api } from '../../boot/api';
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'
let infoStore = localStorage.getItem('info');
let info = ref(null)
let orders = ref([])
let showModal = ref(false)
let showData = ref(null)
let comment = ref('')
if (info) {
    info.value = JSON.parse(infoStore);
}
api.get('/reservation/get_by_uid/' + info.value.uid).then((res) => {
    let response = res.data;
    if (response.code == 200) {
        orders.value = response.data;
        orders.value.forEach(item => {
            item.start_datetime = dayjs(item.start_datetime).format('YYYY-MM-DD HH:mm:ss')
            item.end_datetime = dayjs(item.end_datetime).format('YYYY-MM-DD HH:mm:ss')
        })
    }
})
let handleClick = (row) => {
    showData.value = row;
    showModal.value = true;
}
let handleConfirm = () => {
    let payload = {
        uid: info.value.uid,
        username: info.value.username,
        comment_time: dayjs().format('YYYY-MM-DD HH:mm:ss'),
        comment: comment.value,
        room_id: showData.value.room_id,
    }
    api.post('/comment/add', payload).then((res) => {
        let response = res.data;
        if (response.code == 200) {
            ElMessage.success('评论成功');
            api.post('/reservation/update', {
                rid: showData.value.rid,
                status: '已评论'
            }).then((res) => {
                let response = res.data;
                if (response.code == 200) {
                    api.get('/reservation/get_by_uid/' + info.value.uid).then((res) => {
                        let response = res.data;
                        if (response.code == 200) {
                            orders.value = response.data;
                            orders.value.forEach(item => {
                                item.start_datetime = dayjs(item.start_datetime).format('YYYY-MM-DD HH:mm:ss')
                                item.end_datetime = dayjs(item.end_datetime).format('YYYY-MM-DD HH:mm:ss')
                            })
                        }
                    })
                }
            }).then(() => {
                showData.value = null;
                showModal.value = false;

            })
        }
    })
}
</script> 
 
<style scoped></style>