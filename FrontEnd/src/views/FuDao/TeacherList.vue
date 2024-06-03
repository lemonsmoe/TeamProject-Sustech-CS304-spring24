<template>
<div>

        <!-- <el-main> -->
          <el-card style=" margin-bottom: 10px" >
            <div slot="header" class="clearfix">
              <span>预约辅导系统</span>
            </div>
              <!-- <div slot="header" class="clearfix">
                  <span>预约辅导</span>
              </div> -->
              <!-- <el-form :inline="true" :model="query" class="demo-form-inline">
                  
                  <el-form-item> -->
                      <!-- <el-button type="danger" @click="toMenu">返回</el-button> -->
                      <!-- <el-button type="primary" @click="toAppointmentList">我的预约</el-button> -->
                  <!-- </el-form-item>
              </el-form> -->

              <el-tabs v-model="activeTab" @tab-click="handleTabClick">
                <el-tab-pane label="一对一辅导" name="teacher" class="classtype"></el-tab-pane>
                <el-tab-pane label="习题课" name="class" class="classtype"></el-tab-pane>
                <el-tab-pane label="我的预约" name="appointment" class="classtype"></el-tab-pane>

              </el-tabs>

              <div v-if="activeTab === 'teacher'">
                <el-row :gutter="20">
                  <el-col :span="8" v-for="(teacher, index) in teacher_list" :key="index">
                    <el-card class="box-card"  @click.native="makeAppointment(teacher)">
                      <!-- <div slot="header" class="clearfix"> -->
                        <span class="teacher_name">{{teacher.name }}</span>
                      <!-- </div>
                      <img src="@/assets/cover.png" alt="">
                      <div> -->
                      
                        <p class="teacher_subject">{{ teacher.subject }}</p>
                        <div class="teacher_gender">{{ teacher.gender }}</div>
                        <div class="teacher_age">{{ teacher.age }}</div>
                      <!-- </div> -->
                      <!-- <el-button @click="makeAppointment(teacher)" type="primary" style="margin-top: 10px;">预约</el-button> -->
                    </el-card>
                  </el-col>
                </el-row>
              </div>

              <div v-if="activeTab === 'class'">
                <el-row :gutter="20">
                  <el-col :span="8" v-for="(workshop, index) in class_list" :key="index">
                    <el-card class="box-card"">
                      <div slot="header" class="clearfix">
                        <span class="teacher_subject">{{ workshop.subject }}</span>
                      <!-- </div>
                      <img src="@/assets/cover.png" alt="">
                      <div> -->
                        <p class="teacher_name">{{ workshop.tutor_name }}</p>
                        <p  class="teacher_content">课程内容: {{ workshop.content }}</p>
                        <p class="teacher_time">{{ workshop.time_start +" - "+ workshop.time_end }}</p>
                        <p>课程地点: {{ workshop.location }}</p>
                      </div>
                      <el-button @click="makeWorkshopAppointment(workshop)" type="primary" style="margin-top: 10px;">预约</el-button>
                    </el-card>
                  </el-col>
                </el-row>
              </div>

              <div v-if="activeTab === 'appointment'">
                <AppointmentList></AppointmentList>
              </div>

          </el-card>

        <!-- </el-main> -->

    <el-dialog :visible.sync="addAppointment" width="600px">
      <el-form ref="form" :model="form" label-width="80px">

        <el-form-item label="老师编号" prop="teacher_id">
          <el-input v-model="appointmentForm.teacher_id"  :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="老师姓名" prop="teacher_name"  >
          <el-input v-model="appointmentForm.teacher_name"  :disabled="true"></el-input>
        </el-form-item>
        <!-- <el-form-item label="学生手机" prop="phone_number">
          <el-input v-model="appointmentForm.phone_number"></el-input>
        </el-form-item> -->

        <el-form-item label="预约日期" prop="appointment_date">
          <el-date-picker
            v-model="appointmentForm.appointment_date"
            type="date"
            placeholder="选择日期"
            :picker-options="pickerOptions"
          ></el-date-picker>
        </el-form-item>

        <el-form-item label="预约时间" prop="appointment_time">
        <el-select v-model="appointmentForm.appointment_time" placeholder="选择时间段">
          <el-option
            v-for="(time, index) in timeSlots"
            :key="index"
            :label="time"
            :value="time"
          ></el-option>
        </el-select>
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
import Layout from '@/components/Layout.vue'
import request from "@/utils/request";
import { formatDate, formatTime } from "@/utils/tool";
import AppointmentList from './AppointmentList.vue';
export default {
  name: 'TeacherList',
  components: {
        Layout,
        AppointmentList
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
        teacher_id: '',
        teacher_name: '',
        phone_number: '',
        appointment_date: '',
        appointment_time: '',
        remark: ''
      },
      timeSlots: ['8:00 - 9:50', '10:20 - 12:10', '14:00 - 15:50', '16:20 - 18:10'],
      
      index: 0,
      scheme: {},
      teacher_list: [
        
      ],
      class_list:[
        
      ],
      activeTab: 'teacher', // 默认激活的选项卡
      pickerOptions: {
        disabledDate(time) {
          const today = new Date();
          return time.getTime() < today.getTime();
        }
      },
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
      // 拿一对一老师信息
      request.get('/tutorial/tutors/get').then(res=>{
        // console.log("交互成功")
        console.log("fetchTutorsDone")
        console.log(res)
        if (res.status === 200) {
          // console.log("收到后端回复200")
          
          // this.$message.success(res.data.msg)
          // console.log(res.data)

        } else {
          this.$message.error(res.data.msg)
        }
        console.log(res.data)
        this.teacher_list = res.data
      })

      // 拿习题课信息
      request.get('/tutorial/workshops/get').then(res=>{
        // console.log("交互成功")
        console.log("fetchWorkshopsDone")
        console.log(res)
        if (res.status === 200) {
          // console.log("收到后端回复200")
          
          // this.$message.success(res.data.msg)
          // console.log(res.data)

        } else {
          this.$message.error(res.data.msg)
        }
        console.log(res.data)
        this.class_list = res.data
        // for (let i = 0; i < this.class_list.length; i++) {
        //   this.class_list[i].time_start = formatDate(this.class_list[i].time_start)
        //   this.class_list[i].time_end = formatTime(this.class_list[i].time_end)
        // }
      })

    },
    toMenu() {
      this.$router.push('/fudao')
    },
    toAppointmentList() {
      this.$router.push('/fudao/appointmentlist')
    },
    makeAppointment(teacher) {
      this.addAppointment = true
      // this.appointmentForm.student_id = this.current_student_id

      this.appointmentForm.teacher_id = teacher.tutor_id
      this.appointmentForm.teacher_name = teacher.name
      this.appointmentForm.appointment_date = ''
      this.appointmentForm.appointment_time = ''
      this.appointmentForm.remark = ''
      

    },
    makeWorkshopAppointment(workshop) {
      let list = {
        'workshop_id': workshop.workshop_id
      }
      request.post('/tutorial/appointments/addworkshop', list).then(res=>{
        console.log(res)
        if (res.status === 200) {
          console.log(res.data.msg)
          // this.$router.push('/login')
          this.$message.success('预约成功')
          
        } else {
          console.log(res.data.msg)
          this.$message.error('预约失败')
        }
      })

    },
    confirmAdd() {
      
      let list = {
        // 学生id 老师编号 老师姓名 学生手机 预约时间 备注
        'tutor_id': this.appointmentForm.teacher_id,
        'teacher_name': this.appointmentForm.teacher_name,
        'phone_number': this.appointmentForm.phone_number,
        'appointment_date': this.appointmentForm.appointment_date.toLocaleDateString(),
        'appointment_time': this.appointmentForm.appointment_time,
        'help_needed': this.appointmentForm.remark
      }

      request.post('/tutorial/appointments/add', list).then(res=>{
        console.log(res)
        if (res.status === 200) {
          console.log(res.data.msg)
          // this.$router.push('/login')
          this.$message.success('创建成功')
          this.addAppointment = false
        } else {
          console.log(res.data.msg)
          this.$message.error(res.data.msg)
        }
      })

      // AppointmentList.tableData.push(list)

      // this.$message({
      //   message: '创建成功',
      //   type: 'success'
      // })
      
    },
    cancelAdd() {
      this.addAppointment = false
    },
    disabledDate(time) {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return time.getTime() < today.getTime();
    },
    handleTabClick(tab) {
      console.log(`当前激活的选项卡: ${tab.name}`);
    },
    
  }
}
</script>

<style>
  .teacher_subject {
    font-size: 60px;
    color: #265b38c6;
    margin: 10px;
  }
  .teacher_name {
    font-size: 20px;
    color: #0000009b;
  }
  .teacher_content {
    font-size: 30px;
    color: #0a9aed;
  }
  .teacher_time {
    font-size: 20px;
    color: #ed0a0a;
  }
  .teacher_gender {
    font-size: 30px;
    color: #0c4edc;
  }
  .teacher_age {
    font-size: 20px;
    color: #ed0a0a;
  }
  .box-card {
    /* 颜色 */
    background-color: #d3fed3c2;
    /* 透明度 */
    opacity: 0.9;
    margin: 10px 2px;
    /* 圆角 */
    border-radius: 40px;
    /* 阴影 */
    box-shadow: 0 0 10px rgb(114, 163, 117);
    /* 过渡效果 */
    transition: all 0.3s;
    /* 定位 */
    position: relative;
    /* 边框 */
    border: 2px solid #0d500dd2;
  }
  /* 鼠标移入卡片时，卡片的样式 透明度变化 */
  .box-card:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transform: scale(1.05);
  }

  .el-dialog {
    border-radius: 10px; /* 调整为你需要的圆角大小 */
  }

</style>