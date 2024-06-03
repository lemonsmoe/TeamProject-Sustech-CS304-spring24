<template>
  <div>

        <!-- <el-main> -->
          <el-card style=" margin-bottom: 10px" >
              <!-- <div slot="header" class="clearfix">
                  <span>我的预约</span>
              </div> -->

              <el-form :inline="true" :model="query" class="demo-form-inline" @keydown.enter.native="handleQuery">
                  
                  <el-form-item label="老师姓名">
                      <el-input v-model="query.tutor_name" placeholder="请输入老师姓名"></el-input>
                  </el-form-item>
                  <el-form-item label="预约日期" prop="appointment_date">
                    <el-date-picker
                      v-model="query.appointment_date"
                      type="date"
                      placeholder="选择日期"
                      
                    ></el-date-picker>
                  </el-form-item>
                  
                  <el-form-item>
                      <el-button type="primary" @click="handleQuery">查询</el-button>
                  </el-form-item>
                  
              </el-form>

              <el-table :data="tableData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe style="width: 100%; margin-bottom: 10px">
                <el-table-column
                  type="index"
                  label="序号"
                  width="100"
                  :align="'center'">
                </el-table-column>

                <el-table-column
                  prop="type"
                  label="课程类型"
                  :align="'center'">
                </el-table-column>

                <el-table-column
                  prop="help_needed"
                  label="课程主题"
                  :align="'center'">
                </el-table-column>

                <el-table-column
                  prop="tutor_name"
                  label="老师姓名"
                  :align="'center'">
                </el-table-column>

                <el-table-column
                  prop="appointment_time_start"
                  label="开始时间"
                  width="200"
                  :align="'center'">
                </el-table-column>

                <el-table-column
                  prop="appointment_time_end"
                  label="结束时间"
                  width="200"
                  :align="'center'">
                </el-table-column>
                
                <el-table-column
                  label="操作"
                  
                  :align="'center'">
                  <template slot-scope="scope">
                    <el-button @click="handleDelete(scope.$index, scope.row)" type="text" size="small">取消预约</el-button>
                  </template>
                </el-table-column>
              </el-table>

              <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-sizes="[5, 10, 20]"
                :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="tableData.length"
              ></el-pagination>

          </el-card> 

        <!-- </el-main> -->
      </div>
</template>

<script>
import Layout from '@/components/Layout.vue'
import request from "@/utils/request";
import { formatDate } from "@/utils/tool.js";
export default {
  name: 'AppointmentList',
  components: {
      Layout
  },
  data() {
    return {
      pageSize: 5,
      currentPage: 1,
      isCollapse: false,
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold',

      query: {
        
        tutor_name: '',
        appointment_date: '',

      },
      
      tableData:[],
      
      index: 0,
      scheme: {},

    }
  },
  mounted() {

  },
  created() {
    // 在组件创建后立即发送请求
    this.fetchData();
  },
  methods: {
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    fetchData() {
      console.log("fetchData111")
      request.post('/tutorial/appointments/get', this.query).then(res=>{
        // console.log("交互成功")
        console.log("fetchDataDone")
        console.log(res)
        if (res.status === 200) {
          // console.log("收到后端回复200")
          
          // this.$message.success(res.data.msg)
          let obj = res.data
          for (let i = 0; i < obj.length; i++) {
            obj[i].appointment_time_start = formatDate(obj[i].appointment_time_start)
            obj[i].appointment_time_end = formatDate(obj[i].appointment_time_end)
          }
          this.tableData = obj
        } else {
          this.$message.error(res.data.msg)
        }
        
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
    // 查询预约
    handleQuery() {
      console.log(this.query)
      request.post('/tutorial/appointments/get', this.query).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.$message.success('查询成功')
          let obj = res.data
          for (let i = 0; i < obj.length; i++) {
            obj[i].appointment_time_start = formatDate(obj[i].appointment_time_start)
            obj[i].appointment_time_end = formatDate(obj[i].appointment_time_end)
          }
          this.tableData = obj
        } else {
          this.$message.error(res.data.msg)
        }
      })
    },
    
    toMenu() {
      this.$router.push('/fudao')
    },
    handleDelete(index, row) {
      // 前端删除
      this.tableData.splice(index, 1)
      
      // 后端删除
      let appointment_id = row.appointment_id
      request.post('/tutorial/appointments/delete', {
        appointment_id: appointment_id
      }).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.$message.success('取消预约成功')
        } else {
          this.$message.error(res.data.msg)
        }
      })
    }, 
    
  }
}
</script>