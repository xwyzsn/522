<template>
    <div class="w-full h-full">
        <el-table class="w-full h-full" :data="users">
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="email" label="邮箱"></el-table-column>
            <el-table-column prop="password" label="密码"></el-table-column>
            <el-table-column prop="tel" label="电话"></el-table-column>
            <el-table-column prop="role" label="角色"></el-table-column>
            <el-table-column label="操作">
                <template #default="scope">

                    <el-button type="primary" size="mini" @click="handleUpdate(scope.row)">编辑</el-button>
                    <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog title="编辑用户" v-model="editModal.modal" width="400px">
            <updateInformation :data="editModal.data" url="/user/update"></updateInformation>
        </el-dialog>
    </div>
</template>
 
<script setup>
import { ref, watch } from 'vue'
import { api } from '../../boot/api';
import { ElMessage } from 'element-plus';
import updateInformation from '../../components/information/updateInformation.vue';
let users = ref([])
api.get('/user/fetchall').then((res) => {
    users.value = res.data.data
})
let editModal = ref({
    modal: false,
    data: {}
})
const handleUpdate = (row) => {
    console.log(row)
    editModal.value.modal = true
    editModal.value.data = row
    // Object.entries(row).forEach(([key, value]) => {
    //     editModal.value.data[key] = [va]
    // })
}

const handleDelete = (row) => {
    let postData = {}
    Object.entries(row).forEach(([key, value]) => {
        postData[key] = value
    })
    console.log(postData)
    api({
        url: '/user/delete',
        method: 'delete',
        data: postData
    }).then(res => {
        let response = res.data
        if (response.code === 200) {
            ElMessage.success(response.msg)
            api.get('/user/fetchall').then((res) => {
                users.value = res.data.data
            })
        } else {
            ElMessage.error(response.msg)
        }
    })

}


</script> 
 
<style scoped></style>