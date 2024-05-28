<template>
<Layout>
  <el-main>
    <el-card style=" margin-bottom: 10px" >
      <div slot="header" class="clearfix">
          <span>预约辅导</span>
      </div>
      <el-row>
        <el-col :span="8">
            <el-card>
                <img src="@/assets/logo.png" alt="">
                <div></div>
                <el-button type="primary" @click="toAppointmentList">我的预约</el-button>
            </el-card>
        </el-col>
        <el-col :span="8">
            <el-card>
                <img src="@/assets/logo.png" alt="">
                <div></div>
                <el-button type="primary" @click="toTeacherList">我要预约</el-button>
            </el-card>
        </el-col>
        <el-col :span="8">
            <el-card>
                <img src="@/assets/logo.png" alt="">
                <div></div>
                <el-button type="primary">活动查询</el-button>
            </el-card>
        </el-col>
          
      </el-row>
        
    </el-card>
    <!-- 三个按钮 第一个跳转到选择辅导师的列表 第二个跳转到预约信息 第三个跳转到心理咨询活动-->
    
    <!-- 选择辅导师的列表 -->
    
    <!-- 点击按钮跳转到辅导师列表页面 -->
    <!-- 辅导师列表页面显示所有辅导师的信息 -->
    


    

  </el-main>
</Layout>
  </template>
  
  <script>
  import Layout from '@/components/Layout.vue'
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
  