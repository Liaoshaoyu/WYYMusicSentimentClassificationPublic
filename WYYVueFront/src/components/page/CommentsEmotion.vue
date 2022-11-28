<template>
    <div>
        <!-- <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item> <i class="el-icon-lx-cascades"></i> 基础表格 </el-breadcrumb-item>
            </el-breadcrumb>
        </div> -->
        <div class="container">
            <div class="handle-box">
                <!-- <el-button type="primary" icon="el-icon-delete" class="handle-del mr10" @click="delAllSelection">批量删除</el-button> -->
                <el-input v-model="query.content" placeholder="评论内容" class="handle-input mr10"></el-input>
                <el-select v-model="query.positive" placeholder="情感类型" clearable class="handle-select mr10">
                    <el-option key="1" label="积极" :value="true"></el-option>
                    <el-option key="2" label="消极" :value="false"></el-option>
                </el-select>

                <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
            </div>
            <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
                <!-- <el-table-column type="selection" width="55" align="center"></el-table-column> -->
                <el-table-column prop="comment_id" label="ID" align="center"></el-table-column>
                <el-table-column prop="content" label="评论内容"></el-table-column>
                <el-table-column label="积极评论" align="center">
                    <template slot-scope="scope">
                        <el-switch
                            v-if="scope.row.positive !== null"
                            v-model="scope.row.positive"
                            @change="switchChangeHandle(scope.row)"
                        ></el-switch>
                        <span v-else>未分类</span>
                    </template>
                </el-table-column>

                <el-table-column prop="time_str" label="评论时间"></el-table-column>
                <el-table-column prop="song_name" label="所属歌曲"></el-table-column>
                <el-table-column prop="classify_by" label="分类"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        <!-- <el-button type="text" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)"
                            >删除</el-button
                        > -->
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    layout="total, sizes, prev, pager, next, jumper"
                    :current-page="query.page"
                    :page-size="query.page_size"
                    :page-sizes="pageSizes"
                    :total="pageTotal"
                    @current-change="handlePageChange"
                    @size-change="handleSizeChange"
                ></el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="45%">
            <el-form ref="form" :model="form" label-width="110px">
                <el-form-item label="评论内容：">
                    <span>{{ form.content }}</span>
                </el-form-item>
                <el-form-item label="情感类型：">
                    <el-radio v-model="form.positive" :label="true">积极</el-radio>
                    <el-radio v-model="form.positive" :label="false">消极</el-radio>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { get_song_comments, update_song_comments } from '@/api';
export default {
    name: 'basetable',
    data() {
        return {
            query: {
                page: 1,
                page_size: 10,
                content: null,
                positive: null
            },
            tableData: [],
            editVisible: false,
            pageTotal: 0,
            form: {
                id: null,
                positive: true
            },
            idx: -1,
            id: -1,
            pageSizes: [10, 20, 50]
        };
    },
    created() {
        this.getData();
    },
    methods: {
        async getData() {
            await get_song_comments(this.query).then((res) => {
                this.tableData = res.data.list;
                this.pageTotal = res.data.total;
            });
        },
        // 触发搜索按钮
        handleSearch() {
            if (this.query.positive === '') {
                this.query.positive = null;
            }
            this.query.page = 1;
            this.getData();
        },
        // 编辑操作
        handleEdit(index, row) {
            this.idx = index;
            this.form = row;
            this.editVisible = true;
        },
        // 保存编辑
        async saveEdit() {
            this.editVisible = false;
            if (this.form.positive === null) {
                return;
            }
            await update_song_comments({
                id: this.form.id,
                positive: this.form.positive,
                classify_by: '手动分类'
            }).then(() => {
                this.$message.success(`修改第 ${this.idx + 1} 行成功`);
                this.$set(this.tableData, this.idx, this.form);
            });
        },
        // 分页导航
        handlePageChange(val) {
            if (val > 9999) {
                this.$message.error('页码不能超过9999页！');
                return;
            }
            this.query.page = val;
            this.getData();
        },
        handleSizeChange(val) {
            this.query.page = 1;
            this.query.page_size = val;
            this.getData();
        },
        async switchChangeHandle(row) {
            if (this.editVisible) {
                return;
            }
            // console.log(row.positive);
            await update_song_comments({
                id: row.id,
                positive: row.positive,
                classify_by: '手动分类'
            });
        }
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
