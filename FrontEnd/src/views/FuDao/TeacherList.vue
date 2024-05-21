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
                  <span>我要预约</span>
              </div>
              <el-form :inline="true" :model="query" class="demo-form-inline">
                  <el-form-item label="辅导师姓名">
                      <el-input v-model="query.teacher_Name" placeholder="请输入辅导师姓名"></el-input>
                  </el-form-item>
                  <el-form-item label="辅导师工号">
                      <el-input v-model="query.teacher_ID" placeholder="请输入辅导师工号"></el-input>
                  </el-form-item>
                  <el-form-item label="辅导师学科">
                      <el-input v-model="query.teacher_Subject" placeholder="请输入辅导师学科"></el-input>
                  </el-form-item>
                  <el-form-item>
                      <el-button type="primary" @click="onSubmit">查询</el-button>
                  </el-form-item>
                  <el-form-item>
                      <el-button type="danger" @click="toMenu">返回</el-button>
                  </el-form-item>
              </el-form>

              <!-- <el-row>
                  
                  <el-col :span="8">
                      <el-card>
                          <img src="@/assets/logo.png" alt="">
                          

                          <div>姓名：{{teacher_list[0].teacher_name}}</div>
                          <div>职称：{{teacher_list[0].teacher_title}}</div>
                          <div>学科：{{teacher_list[0].teacher_subject}}</div>
                          <el-button type="primary" @click="makeAppointment">预约</el-button>
                      </el-card>
                  </el-col>
                  <el-col :span="8">
                      <el-card>
                          <img src="@/assets/logo.png" alt="">
                          <div>姓名：{{teacher_list[1].teacher_name}}</div>
                          <div>职称：{{teacher_list[1].teacher_title}}</div>
                          <div>学科：{{teacher_list[1].teacher_subject}}</div>
                          <el-button type="primary" @click="makeAppointment">预约</el-button>
                      </el-card>
                  </el-col>
                  <el-col :span="8">
                      <el-card>
                          <img src="@/assets/logo.png" alt="">
                          
                          <div>姓名：{{teacher_list[2].teacher_name}}</div>
                          <div>职称：{{teacher_list[2].teacher_title}}</div>
                          <div>学科：{{teacher_list[2].teacher_subject}}</div>

                          <el-button type="primary" @click="makeAppointment">预约</el-button>
                      </el-card>
                  </el-col>

              </el-row> -->

              <el-row :gutter="20">
                <el-col :span="8" v-for="(teacher, index) in teacher_list" :key="index">
                  <el-card class="box-card">
                    <div slot="header" class="clearfix">
                      <span>{{ teacher.name }}</span>
                    </div>
                    <img src="@/assets/logo.png" alt="">
                    <div>
                    
                      <p>教授科目: {{ teacher.subject }}</p>
                    </div>
                    <el-button @click="makeAppointment(teacher)" type="primary" style="margin-top: 10px;">预约</el-button>
                  </el-card>
                </el-col>
              </el-row>
              
          </el-card>

        </el-main>
      </el-container>
    </el-container>

    <el-dialog :visible.sync="addAppointment" width="600px">
      <el-form ref="form" :model="form" label-width="80px">

        <el-form-item label="学生姓名" prop="student_name">
          <el-input v-model="appointmentForm.student_name"></el-input>
        </el-form-item>
        <el-form-item label="老师编号" prop="teacher_id">
          <el-input v-model="appointmentForm.teacher_id"></el-input>
        </el-form-item>
        <el-form-item label="老师姓名" prop="teacher_name">
          <el-input v-model="appointmentForm.teacher_name"></el-input>
        </el-form-item>
        <el-form-item label="学生手机" prop="phone_number">
          <el-input v-model="appointmentForm.phone_number"></el-input>
        </el-form-item>
        <el-form-item label="预约时间" prop="appointment_time">
          <el-input v-model="appointmentForm.appointment_time"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="appointmentForm.remark"></el-input>
        </el-form-item>
        
      </el-form>

      <el-button type="primary" @click="confirmAdd" :align="'center'">立即创建</el-button>
      <el-button type="info" @click="cancelAdd" :align="'center'">取消</el-button>
    </el-dialog>

  </div>
</template>

<script>
import request from "@/utils/request";
export default {
  name: 'LunTan',
  data() {
    return {

      isCollapse: false,
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold',
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      },
      query: {
        teacher_Name: '',
        teacher_ID: '',
        teacher_Subject: ''
      },
      addAppointment: false,
      appointmentForm: {
        student_name: '',
        teacher_id: '',
        teacher_name: '',
        phone_number: '',
        appointment_time: '',
        remark: ''
      },
      
      index: 0,
      scheme: {},
      teacher_list: [
        // {
        //   teacher_name: '张六',
        //   teacher_title: '教授',
        //   teacher_subject: '数学'
        // },
        // {
        //   teacher_name: '李七',
        //   teacher_title: '副教授',
        //   teacher_subject: '物理'
        // },
        // {
        //   teacher_name: '王八',
        //   teacher_title: '讲师',
        //   teacher_subject: '化学'
        // }
      ],
      

    }
  },
  mounted() {

  },
  created() {
    // 在组件创建后立即发送请求
    this.fetchData();
  },
  methods: {
    fetchData() {
    console.log("fetchData")
    request.get('/tutorial/tutors').then(res=>{
      // console.log("交互成功")
      console.log("fetchDataDone")
      console.log(res)
      if (res.status === 200) {
        // console.log("收到后端回复200")
        
        this.$message.success(res.msg)
        // console.log(res.data)

      } else {
        this.$message.error(res.msg)
      }
      console.log(res.data)
      this.teacher_list = res.data
    })

    },
    handleFullScreen() {
      document.documentElement.requestFullscreen()
    },
    handleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideWidth = this.isCollapse ? '64px' : '200px'
      this.collapseIcon = this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
    },
    onSubmit() {
      let obj = []
      obj = this.formInline.mingcheng.split(' ')
      console.log(obj)
      this.axios.post('http://localhost:1314/submit_data', {
        'password': 'my father is YHT', 'student_name': '', 'keywords': obj, 'badwords': [''], 'excluded_time': {'点': []}
      }).then(res=>{

        this.scheme = res.data.schedule_scheme
        // console.log(this.scheme)
        this.show(this.index)

      })
    },
    toMenu() {
      this.$router.push('/fudao')
    },
    makeAppointment(teacher) {
      this.addAppointment = true
    },
    confirmAdd() {
      
      var list = {
        // 学生姓名 老师编号 老师姓名 学生手机 预约时间 备注
        student_name: this.appointmentForm.student_name,
        teacher_id: this.appointmentForm.teacher_id,
        teacher_name: this.appointmentForm.teacher_name,
        phone_number: this.appointmentForm.phone_number,
        appointment_time: this.appointmentForm.appointment_time,
        remark: this.appointmentForm.remark
      }
      
      AppointmentList.tableData.push(list)

      this.$message({
        message: '创建成功',
        type: 'success'
      })
      this.addAppointment = false
    },
    cancelAdd() {
      this.addAppointment = false
    }
    
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