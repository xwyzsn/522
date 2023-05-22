<template>
    <div class="w-full h-full">
        <div>
            <el-button type="primary" @click="addModal = true">添加</el-button>
        </div>
        <el-table class="w-full h-full" :data="rooms">
            <el-table-column prop="room_name" label="名字"></el-table-column>
            <el-table-column prop="room_desc" label="描述"></el-table-column>
            <el-table-column label="类型">
                <template #default="scope">
                    <el-tag v-for="item in scope.row.room_type.split(',')" :key="item" class="m-1">{{ item }}</el-tag>
                </template>

            </el-table-column>
            <el-table-column prop="room_cover_pic" label="封面">
                <template #default="scope">
                    <img :src="scope.row.room_cover_pic" class="w-40 h-40" />
                </template>
            </el-table-column>
            <el-table-column prop="room_innner_pic" label="图片">
                <template #default="scope">
                    <img :src="scope.row.room_inner_pic" class="w-40 h-40" />
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button type="primary" size="mini" @click="handleUpdate(scope.row)">修改</el-button>
                    <el-button type="danger" size="mini" @click="handleRemove(scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog v-model="editModal">
            <el-form label-width="100px">
                <el-form-item label="房间名">
                    <el-input v-model="editData.room_name" placeholder="房间名"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input v-model="editData.room_desc" type="textarea" placeholder="房间描述"></el-input>
                </el-form-item>
                <el-form-item label="类型">
                    <el-input v-model="editData.room_type" placeholder="标签用,分割"></el-input>
                </el-form-item>
                <el-form-item label="预约">
                    <el-radio-group v-model="editData.need_reservation" size="small">
                        <el-radio label="1">需要续约</el-radio>
                        <el-radio label="0">无需预约</el-radio>

                    </el-radio-group>
                    {{ editData.need_reservation }}
                </el-form-item>
                <el-form-item label="封面">
                    <el-upload class="avatar-uploader" action="none" :on-preview="handleOnPreview" :auto-upload="false"
                        :file-list="fileList" :on-change="onChange" :limit="1" :accept="'image/*'" :on-remove="onRemove">
                        <img v-if="editData.room_cover_pic" :src="editData.room_cover_pic" class="avatar" />
                        <el-icon v-else class="avatar-uploader-icon">
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
                <el-form-item label="图片">
                    <el-upload class="avatar-uploader" action="none" :on-preview="handleOnPreview" :auto-upload="false"
                        :file-list="innerFileList" :on-change="onChangeInner" :limit="1" :accept="'image/*'"
                        :on-remove="onRemoveInner">
                        <img v-if="editData.room_inner_pic" :src="editData.room_inner_pic" class="avatar" />
                        <el-icon v-else class="avatar-uploader-icon">
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button type="primary" @click="handleConfirm">提交</el-button>
            </template>
        </el-dialog>
        <el-dialog v-model="addModal">
            <el-form label-width="100px">
                <el-form-item label="房间名">
                    <el-input v-model="editData.room_name" placeholder="房间名"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input v-model="editData.room_desc" type="textarea" placeholder="房间描述"></el-input>
                </el-form-item>
                <el-form-item label="类型">
                    <el-input v-model="editData.room_type" placeholder="标签用,分割"></el-input>
                </el-form-item>
                <el-form-item label="预约">
                    <el-radio-group v-model="editData.need_reservation" size="small">
                        <el-radio label="1">需要续约</el-radio>
                        <el-radio label="0">无需预约</el-radio>

                    </el-radio-group>
                    {{ editData.need_reservation }}
                </el-form-item>
                <el-form-item label="封面">
                    <el-upload class="avatar-uploader" action="none" :on-preview="handleOnPreview" :auto-upload="false"
                        :file-list="fileList" :on-change="onChange" :limit="1" :accept="'image/*'" :on-remove="onRemove">
                        <img v-if="editData.room_cover_pic" :src="editData.room_cover_pic" class="avatar" />
                        <el-icon v-else class="avatar-uploader-icon">
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
                <el-form-item label="图片">
                    <el-upload class="avatar-uploader" action="none" :on-preview="handleOnPreview" :auto-upload="false"
                        :file-list="innerFileList" :on-change="onChangeInner" :limit="1" :accept="'image/*'"
                        :on-remove="onRemoveInner">
                        <img v-if="editData.room_inner_pic" :src="editData.room_inner_pic" class="avatar" />
                        <el-icon v-else class="avatar-uploader-icon">
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button type="primary" @click="handleAdd">提交</el-button>
            </template>
        </el-dialog>
    </div>
</template>
 
<script setup>
import { ref } from 'vue'
import { api } from '../../boot/api';
import { ElMessage } from 'element-plus';
let editModal = ref(false)
let editData = ref({})
let fileList = ref([])
let innerFileList = ref([])
let rooms = ref([])
let addModal = ref(false)
api.get('/room/get_all').then(res => {
    rooms.value = res.data.data
})
const handleUpdate = (row) => {
    editModal.value = true
    editData.value = row
}
let onChange = (file) => {
    fileList.value.push(file)
    editData.value.room_cover_pic = URL.createObjectURL(file.raw)
}
let onRemove = (file) => {
    console.log('file', file)
    fileList.value = []
    editData.value.room_cover_pic = ''
}
let onChangeInner = (file) => {
    innerFileList.value.push(file)
    editData.value.room_inner_pic = URL.createObjectURL(file.raw)
}
let onRemoveInner = (file) => {
    console.log('file', file)
    innerFileList.value = []
    editData.value.room_inner_pic = ''
}
let handleConfirm = () => {
    let formData = new FormData()
    formData.append('rid', editData.value.rid)
    formData.append('room_name', editData.value.room_name)
    formData.append('room_desc', editData.value.room_desc)
    formData.append('room_type', editData.value.room_type)
    if (fileList.value.length !== 0) {
        formData.append('room_cover_pic', fileList.value[0].raw)
    }
    if (innerFileList.value.length !== 0) {
        formData.append('room_inner_pic', innerFileList.value[0].raw)
    }
    api({
        url: '/room/update',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then(res => {
        let response = res.data
        console.log('response', response)
        if (response.code === 200) {
            ElMessage.success('修改成功')
            editModal.value = false
            editData.value = {}
        }
    })
}
let handleAdd = () => {
    let formData = new FormData()
    // formData.append('rid', editData.value.rid)
    formData.append('room_name', editData.value.room_name)
    formData.append('room_desc', editData.value.room_desc)
    formData.append('room_type', editData.value.room_type)
    if (fileList.value.length !== 0) {
        formData.append('room_cover_pic', fileList.value[0].raw)
    }
    if (innerFileList.value.length !== 0) {
        formData.append('room_inner_pic', innerFileList.value[0].raw)
    }
    api({
        url: '/room/add',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then(res => {
        let response = res.data
        console.log('response', response)
        if (response.code === 200) {
            ElMessage.success('添加成功')
            addModal.value = false
            editData.value = {}
            api.get('/room/get_all').then(res => {
                rooms.value = res.data.data
            })
        }
    })
}
let handleRemove = (row) => {
    let row_id = row.rid.toString()
    api({
        url: '/room/delete/' + row_id,
        method: 'delete'
    }).then(res => {
        let response = res.data
        if (response.code === 200) {
            ElMessage.success('删除成功')
            api.get('/room/get_all').then(res => {
                rooms.value = res.data.data
            })
        }
    })

}
</script> 
<style scoped>
.avatar-uploader .avatar {
    width: 178px;
    height: 178px;
    display: block;
}
</style>


<style>
.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}
</style>