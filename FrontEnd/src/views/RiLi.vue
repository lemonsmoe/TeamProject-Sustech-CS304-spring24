<template>
  <div>
    <el-container>
      <el-aside :width="asideWidth">
        <div style="height: 60px; line-height: 60px; font-size: 20px; display: flex; align-items: center; justify-content: center">
          <img src="@/assets/nkd.jpg" style="width: 30px;" alt="">
          <span class="logo-title" v-show="!isCollapse">学术助手</span>
        </div>
        <el-menu router :collapse="isCollapse" :collapse-transition="false" background-color="#001529"
                 active-text-color="#fff" text-color="rgba(255, 255, 255, 0.65)" :default-active="$route.path"
                 style="border: none">
          <el-menu-item index="/">
            <i class="el-icon-s-home"></i>
            <span slot="title">系统首页</span>
          </el-menu-item>
          <el-menu-item index="/login">
            <i class="el-icon-s-custom"></i>
            <span slot="title">登录</span>
          </el-menu-item>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i><span>学生应用</span></template>
            <el-menu-item index="/xuanke">选课系统</el-menu-item>
            <el-menu-item index="/luntan">学习论坛</el-menu-item>
            <el-menu-item index="/fudao">预约辅导</el-menu-item>
            <el-menu-item index="/rili">学习日历</el-menu-item>
            <el-menu-item index="/pingjiao">评教系统</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header style="height: 60px; line-height: 60px; display: flex; align-items: center; box-shadow: 2px 0 6px rgba(0, 21, 41, .35);">
          <i :class="collapseIcon" @click="handleCollapse" style="font-size: 26px"></i>
          <!--          <el-breadcrumb separator="/" style="margin-left: 20px">-->
          <!--            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>-->
          <!--            <el-breadcrumb-item :to="{ path: '/' }">课程管理</el-breadcrumb-item>-->
          <!--          </el-breadcrumb>-->

          <div style="flex: 1; display: flex; justify-content: flex-end; align-items: center">
            <i class="el-icon-quanping" @click="handleFullScreen" style="font-size: 25px"></i>
            <el-dropdown placement="bottom">
              <div style="display: flex; align-items: center; cursor: pointer">
                <img src="@/assets/nkd.jpg" alt="" style="width: 40px; height: 40px; margin: 0 5px">
                <span>用户中心</span>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>个人信息</el-dropdown-item>
                <el-dropdown-item>修改密码</el-dropdown-item>
                <el-dropdown-item>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </el-header>

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
      </el-container>
    </el-container>
    
    <!-- 查看某一天的日程安排表 -->
    <el-dialog :visible.sync="detail">
      <el-message>
        <p>{{ date }} 日程安排</p>
      </el-message>

      <el-table
        :data="tableData"
        stripe
        style="width: 100%; margin-bottom: 10px">
        <el-table-column
          prop="number"
          label="序号"
          width="150"
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
          width="150"
          :align="'center'">
        </el-table-column>
        
        <el-table-column
          label="操作"
          width="150"
          :align="'center'">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row)" type="text" size="small">编辑</el-button>
            <el-button @click="handleDelete(scope.$index, scope.row)" type="text" size="small">删除</el-button>
          </template>
        </el-table-column>
        
      </el-table>
      <el-button type="primary" @click="addList">添加新日程</el-button>
      <el-button type="info" @click="quitDetail">完成</el-button>
    
    </el-dialog>

    
    <!-- 添加新日程 -->
    <el-dialog :visible.sync="getmessage" width="600px">
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

      <el-button type="primary" @click="onSubmit" :align="'center'">立即创建</el-button>
      <el-button type="info" @click="onCancel" :align="'center'">取消</el-button>

    </el-dialog>

    <!-- 编辑日程 -->
    <el-dialog :visible.sync="editmessage" width="600px">
      <el-form ref="editForm" :model="form" label-width="80px">
        <el-form-item label="开始时间1">
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
      <el-button type="info" @click="onCancelEdit" :align="'center'">取消</el-button>

    </el-dialog>


  </div>
</template>

<script>

export default {
  name: 'RiLi',
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
      getmessage:false,
      editmessage:false,
      detail:false,
      date:'',
      row: {},
      tableData: [{
        number: '1',
        time: '15:00',
        name: '上课',
        content: '简介',
        
      }],
    }
  },
  mounted() {

  },
  methods: {
    handleFullScreen() {
      document.documentElement.requestFullscreen()
    },
    handleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideWidth = this.isCollapse ? '64px' : '200px'
      this.collapseIcon = this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
    },
    chooseDay(date) {
      this.$message({
        message: '选择的日期是: ' + date.day,
        type: 'success'
      })
      this.getdetail()
      this.date = date.day
    },
    getdetail(){
        this.detail = true
    }, 
    addList(){
        this.getmessage = true
    },
    quitDetail(){
        this.detail = false
    },
    
    handleEdit(row){
      // 编辑日程

      this.editmessage = true
      this.editForm.time = row.time
      this.editForm.name = row.name
      this.editForm.content = row.content
      this.row = row

    },
    handleDelete(index, row) {
      // 删除日程
      this.tableData.splice(index, 1)
      // 重新排序
      this.tableData.forEach((item, index) => {
        item.number = index + 1
      })
    }, 
    confirmEdit(){
      // 确认编辑

      this.row.time = this.editForm.time
      this.row.name = this.editForm.name
      this.row.content = this.editForm.content
      this.editmessage = false
    },
    onSubmit(){
      // 将新填写的数据添加到表格中
      var list = {
        number: this.tableData.length + 1,
        time: this.form.time,
        name: this.form.name,
        content: this.form.content,
        }
      this.tableData.push(list)
      this.getmessage = false
    },
    onCancel(){
      this.getmessage = false
    },
    onCancelEdit(){
      this.editmessage = false
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