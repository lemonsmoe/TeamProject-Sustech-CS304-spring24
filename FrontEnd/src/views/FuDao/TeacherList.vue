<template>
  <Layout>

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


</Layout>
</template>

<script>
import Layout from '@/components/Layout.vue'
import request from "@/utils/request";
export default {
  name: 'LunTan',
  components: {
        Layout
    },
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
