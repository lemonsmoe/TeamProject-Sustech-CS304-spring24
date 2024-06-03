<template>
<Layout>
  <el-main>
    <!-- <el-card style=" margin-bottom: 10px" >
      <div slot="header" class="clearfix">
          <span>预约辅导</span>
      </div>
      <el-row> -->
        <!--
           <el-col :span="10">
            <el-card>
              <img src="@/assets/logo.png" alt="">
                <div></div>
                <el-button type="primary" @click="toAppointmentList">我的预约</el-button>
            </el-card>
        </el-col>
        <el-col :span="4">
            <el-card></el-card>
        </el-col>
        <el-col :span="10">
            <el-card>
                <img src="@/assets/logo.png" alt="">
                <div></div>
                <el-button type="primary" @click="toTeacherList">我要预约</el-button>
            </el-card>
        </el-col> -->
      <!-- </el-row>
      
    </el-card> -->
    <TeacherList></TeacherList>
  </el-main>
</Layout>
</template>

<script>
import Layout from '@/components/Layout.vue'
import TeacherList from './TeacherList.vue';
export default {
  name: 'LunTan',
  components: {
      Layout,
      TeacherList
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
      formInline: {
        xueqi: '',
        mingcheng: '',
        yuanxi: ''
      },
      
      index: 0,
      scheme: {},
      // 老师的信息

      tableData: [


      ],
    }
  },
  mounted() {
  },
  
  methods: {
    toTeacherList() {
      this.$router.push('/fudao/teacherlist')
    },
    toAppointmentList() {
      this.$router.push('/fudao/appointmentlist')
    },

  }
}
</script>
