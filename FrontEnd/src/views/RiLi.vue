<template>
  <Layout>
    <el-main>
      <el-card style=" margin-bottom: 10px" >
        <div slot="header" class="clearfix">
            <span>学生日历</span>
        </div>
        <div>
          <el-calendar v-model="value"> 
            <div
                slot="dateCell"
                slot-scope="{ data }"
                @click="chooseDay(data)"
                v-popover:popover
            >
              <p>
              {{ data.day.split("-").slice(2).join() }}
              </p>
            </div>

            <!-- <el-date-picker
                v-model="value"
                type="date"
                placeholder="选择日期"
                v-on:change="onSubmit(date)">
            </el-date-picker> -->
            <!-- <template
                slot="dateCell"
                slot-scope="{date, data}">
                <p :class="data.isSelected ? 'is-selected' : ''" >
                {{ data.day.split('-').slice(1).join('-') }} {{ data.isSelected ? '✔️' : ''}}
                </p>
            </template> -->
              
          </el-calendar>
        </div>
      </el-card>
    </el-main>

    <!-- 查看某一天的日程安排表 -->
    <el-dialog :visible.sync="detail">
      <el-message style="font-size: 20px;">
        <p>{{ date }} 日程安排</p>
      </el-message>

      <el-table
        :data="tableData"
        stripe
        style="width: 100%; margin-bottom: 10px">
        <el-table-column
          prop="number"
          label="序号"
          width="100"
          :align="'center'">
          
        </el-table-column>
        <el-table-column
          prop="time"
          label="开始时间"
          width="150"
          :align="'center'">
        </el-table-column>
        <el-table-column
          prop="name"
          label="事件名称"
          width="150"
          :align="'center'">
        </el-table-column>
        <el-table-column
          prop="content"
          label="内容简介"
          width="200"
          :align="'center'">
        </el-table-column>
        
        <el-table-column
          label="操作"
          width="168"
          :align="'center'">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row)" type="text" size="small">编辑</el-button>
            <el-button @click="handleDelete(scope.$index, scope.row)" type="text" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-button type="primary" @click="handleAdd">添加新日程</el-button>
      <el-button type="info" @click="quitDetail">完成</el-button>
    
    </el-dialog>

    <!-- 添加新日程 -->
    <el-dialog :visible.sync="addmessage" width="600px">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="开始时间">
          <el-input v-model="form.time"></el-input>
        </el-form-item>
        <el-form-item label="活动名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="内容简介">
          <el-input v-model="form.content"></el-input>
        </el-form-item>
      </el-form>

      <el-button type="primary" @click="confirmAdd" :align="'center'">立即创建</el-button>
      <el-button type="info" @click="cancelAdd" :align="'center'">取消</el-button>
    </el-dialog>

    <!-- 编辑日程 -->
    <el-dialog :visible.sync="editmessage" width="600px">
      <el-form ref="editForm" :model="form" label-width="80px">
        <el-form-item label="开始时间">
          <el-input v-model="editForm.time"></el-input>
        </el-form-item>
        <el-form-item label="活动名称">
          <el-input v-model="editForm.name"></el-input>
        </el-form-item>
        <el-form-item label="内容简介">
          <el-input v-model="editForm.content"></el-input>
        </el-form-item>
      </el-form>

      <el-button type="primary" @click="confirmEdit" :align="'center'">修改</el-button>
      <el-button type="info" @click="cancelEdit" :align="'center'">取消</el-button>
    </el-dialog>

  </Layout>

</template>

<script>
import Layout from '@/components/Layout.vue'
import request from "@/utils/request";
export default {
  name: 'RiLi',
  components: {
      Layout
  },
  data() {
    return {
      form: {
        time: '',
        name: '',
        content: '',
      },
      editForm: {
        time: '',
        name: '',
        content: '',
      },
      isCollapse: false,
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold',
      value: new Date(),
      addmessage:false,
      editmessage:false,
      detail:false,
      date:'',
      row: {},
      tableData: [],
    }
  },
  mounted() {

  },
  created() {
  // 在组件创建后立即发送请求
    this.getUser();
  },
  methods: {
    getUser() {
      // 获取当前用户信息
      request.get('/general/current_student').then(res=>{
        console.log(res)
      })
    },
    handleLogout() {
      // 在这里添加退出登录的逻辑
      console.log('正在退出登录...');
      // 清除用户信息
      // localStorage.removeItem('user');
      request.get('/general/logout').then(res=>{
        console.log(res)
      })
      // 跳转到登录页面
      this.$router.push('/login');
    },
    handleFullScreen() {
      document.documentElement.requestFullscreen()
    },
    handleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideWidth = this.isCollapse ? '64px' : '200px'
      this.collapseIcon = this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
    },
    chooseDay(date) {
      // 查看详情
      this.$message({
        message: '选择的日期是: ' + date.day,
        type: 'success'
      })
      this.detail = true
      this.date = date.day
    },
    quitDetail(){
      // 退出详情
      this.detail = false
    },

    handleAdd(){
      // 添加日程
      this.addmessage = true
      this.form.time = ''
      this.form.name = ''
      this.form.content = ''
    },
    confirmAdd(){
      // 确认添加（更新表格）
      var list = {
        number: this.tableData.length + 1,
        time: this.form.time,
        name: this.form.name,
        content: this.form.content,
        }
      this.tableData.push(list)
      this.addmessage = false
    },
    cancelAdd(){
      // 取消添加
      this.addmessage = false
    },
    
    
    handleEdit(row){
      // 编辑日程
      this.editmessage = true
      this.editForm.time = row.time
      this.editForm.name = row.name
      this.editForm.content = row.content
      this.row = row

    },
    confirmEdit(){
      // 确认编辑（更新表格）
      this.row.time = this.editForm.time
      this.row.name = this.editForm.name
      this.row.content = this.editForm.content
      this.editmessage = false
    },
    cancelEdit(){
      // 取消编辑
      this.editmessage = false
    },

    handleDelete(index, row) {
      // 删除日程
      this.tableData.splice(index, 1)
      // 重新排序
      this.tableData.forEach((item, index) => {
        item.number = index + 1
      })
    }, 
    
  }
}
</script>

<style>
.el-menu--inline, .el-menu-item {
  background-color: #000c17 !important;
}

.el-submenu__title {
  height: 40px !important;
  line-height: 40px !important;
  padding: 0 25px !important;
  transition: color 0s;
}
.el-menu--collapse .el-submenu__title {
  padding: 0 20px !important;
}
.el-submenu__title>i:nth-child(1) {
  margin-top: 2px;
}
.el-submenu__title>i.el-submenu__icon-arrow {
  margin-top: -5px;
}
.el-menu-item {
  min-width: 0 !important;
  width: calc(100% - 10px);
  margin: 5px;
  height: 40px !important;
  line-height: 40px !important;
  border-radius: 5px;
}
.el-menu--inline>.el-menu-item {
  padding-left: 50px !important;
}
.el-menu-item.is-active {
  background-color: dodgerblue !important;
}

.el-menu-item:hover {
  color: #fff !important;
}

.el-submenu__title:hover *, .el-submenu__title:hover {
  color: #fff !important;
}

.el-aside {
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
  background-color: #001529;
  color: #fff;
  min-height: 100vh;
  transition: width .3s;
}
.el-menu--collapse .el-tooltip {
  padding: 0 15px !important;
}
.logo-title {
  margin-left: 5px;
  transition: all .3s;
}
.el-menu {
  transition: all .3s;
}
</style>