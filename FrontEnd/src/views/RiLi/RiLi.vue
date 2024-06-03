<template>
  <Layout>
    <el-main>
      <el-card style=" margin-bottom: 10px" >
        <div slot="header" class="clearfix">
            <span>学生日历</span>
        </div>
        <el-tabs v-model="activeTab" >
          <el-tab-pane label="日历查看" name="calender" class="classtype"></el-tab-pane>
          <el-tab-pane label="订阅管理" name="course" class="classtype"></el-tab-pane>
          <el-tab-pane label="我的订阅" name="mycourse" class="classtype"></el-tab-pane>
        
        </el-tabs>

        <div v-if="activeTab === 'calender'">
          <div>
            <el-calendar v-model="value"> 
              <div
                  slot="dateCell"
                  slot-scope="{ data }"
                  @click="chooseDay(data)"
                  v-popover:popover
                  class="date-cell">
                <p class="day_num">
                {{ data.day.split("-").slice(2).join() }}
                </p>
                
                <div v-if="memos[data.day]" class="memos">
                  <p v-for="memo in memos[data.day]['display'].slice(0, 3)" 
                  :key="memo[0]"
                  :class="memo[1] === '完成' ? 'completed' : 'incompleted'">
                  {{ '['+memo[0]+']' }}
                  </p>
                </div>

                <p class="meta">
                {{ memos[data.day] ? memos[data.day]['meta'] : ''}}
                </p>
              </div>
                
            </el-calendar>
          </div>
        </div>

        <div v-if="activeTab === 'course'">
          <Course></Course>
        </div>

        <div v-if="activeTab === 'mycourse'">
          <MyCourse></MyCourse>
        </div>
        
      </el-card>
    </el-main>

    <!-- 查看某一天的日程安排表 -->
    <el-dialog :visible.sync="detail" :width="'60%'" @close="getAllDetail()">
      <el-message style="font-size: 20px;">
        <p>{{ date }} 日程安排</p>
      </el-message>

      <el-table
        :data="tableData"
        stripe
        style="width: 100%; margin-bottom: 10px; justify-content: center;">
        <el-table-column
        type="index"
          label="序号"
          width="100"
          :align="'center'">
          
        </el-table-column>
        <el-table-column
          prop="ddl_type"
          label="类型"
          width="100"
          :align="'center'">
          
        </el-table-column>
        <el-table-column
          prop="ddl_time"
          label="开始时间"
          width="100"
          :align="'center'">
        </el-table-column>
        <el-table-column
          prop="ddl_title"
          label="事件名称"
          width="200"
          :align="'center'">
        </el-table-column>
        
        <el-table-column
          prop="ddl_content"
          label="内容简介"
          width="200"
          :align="'center'">
        </el-table-column>
        <el-table-column
          prop="ddl_status"
          label="完成状态"
          width="120"
          :align="'center'">
          <template slot-scope="scope">
            <el-button
              size="mini"
              :type="scope.row.ddl_status === '完成' ? 'success' : 'warning'"
              @click="toggleStatus(scope.row)">
              {{ scope.row.ddl_status }}
            </el-button>
          </template>
        </el-table-column>
        
        <el-table-column
          label="操作"
          width="100"
          :align="'center'">
          <template slot-scope="scope">
            <!-- <el-button @click="handleEdit(scope.row)" type="text" size="small">编辑</el-button> -->
            <el-button @click="handleDelete(scope.row)" type="text" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-button type="primary" @click="handleAdd">添加新日程</el-button>
      <el-button type="info" @click="quitDetail">完成</el-button>
    
    </el-dialog>

    <!-- 添加新日程 -->
    <el-dialog :visible.sync="addmessage" width="600px">
      <el-form ref="form" :model="form" label-width="80px">
        <!-- <el-form-item label="开始时间">
          <el-input v-model="form.time"></el-input>
        </el-form-item> -->
        <el-form-item label="开始时间">
          <el-time-picker
            v-model="form.time"
            placeholder="选择时间"
            format="HH:mm:ss"
            value-format="HH:mm:ss"
          ></el-time-picker>
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
    <!-- 已删除 -->


  </Layout>

</template>

<script>
import Layout from '@/components/Layout.vue'
import request from "@/utils/request";
import { formatDate, formatTime } from "@/utils/tool.js";
import Course from './Course.vue';
import MyCourse from './MyCourse.vue';
export default {
  name: 'RiLi',
  components: {
      Layout,
      Course,
      MyCourse,
  },
  data() {
    return {
      activeTab: 'calender', // 默认激活的选项卡
      form: {
        time: '',
        name: '',
        content: '',
      },
      isCollapse: false,
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold',
      value: new Date(),
      addmessage:false,

      detail:false,
      date:'',
      row: {},
      tableData: [],
      memos: {
        
      }
    }
  },
  mounted() {
    // this.getAllDetail(); // 初次加载时获取数据
    // setInterval(() => this.getAllDetail(), 3000); // 每3秒执行一次getDetail
  },
  created() {
    // 在组件创建后立即发送请求
    this.getAllDetail()
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
    getAllDetail() {
      // 获取所有日程
      request.get('/calender/getallevent').then(res => {
        console.log(res)
        if (res.status === 200) {
          // this.$message.success('获取成功')
          // console.log(res.data)
          this.memos = res.data
        } else {
          this.$message.error(res.data.msg)
        }
      })
    },

    chooseDay(date) {
      // 查看详情
      this.$message({
        message: '选择的日期是: ' + date.day,
        type: 'success'
      })
      this.detail = true
      this.date = date.day
      // console.log(date)
      console.log(date.day)
      
      this.getDetail()

    },
    getDetail(){
      // 获取日程安排
      let list = {
        'ddl_time': this.date
      }
      request.post('/calender/get_byday', list).then(res=>{
        // console.log("交互成功")
        console.log("fetchDataDone")
        console.log(res)
        if (res.status === 200) {
          // this.$message.success('获取成功')
          console.log(res.data)
          let ddls = res.data
          for (let i = 0; i < ddls.length; i++) {
            ddls[i].ddl_time = formatTime(ddls[i].ddl_time)
          }
          this.tableData = ddls

        } else {
          this.$message.error(res.data.msg)
        }
        
      })
    },
    quitDetail(){
      // 退出详情
      // this.getAllDetail()
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
        
        ddl_time: this.date +" "+ this.form.time,
        ddl_title: this.form.name,
        ddl_content: this.form.content,
      }

      request.post('/calender/student_ddl/add', list).then(res=>{
        // console.log("交互成功")
        console.log("fetchDataDone")
        console.log(res)
        if (res.status === 200) {
          this.$message.success('添加成功')
          this.getDetail()
        } else {
          this.$message.error(res.data.msg)
        }
        
      })
      
      this.addmessage = false
    },
    
    cancelAdd(){
      // 取消添加
      this.addmessage = false
    },
    
    
    // handleEdit(row){
    //   // 编辑日程
    //   this.addmessage = true
    //   this.form.time = row.ddl_time
    //   this.form.name = row.ddl_title
    //   this.form.content = row.ddl_content
    //   this.row = row

    // },
    // confirmEdit(){
    //   // 确认编辑(创建+删除)
    //   this.confirmAdd()
    //   console.log("删除前")
    //   this.handleDelete(this.row)
    //   console.log("删除后")
    //   this.addmessage = false
    // },
    // cancelEdit(){
    //   // 取消编辑
    //   this.addmessage = false
    // },

    handleDelete(row) {
      request.post('/calender/student_ddl/delete', row ).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.$message.success('删除成功')

          this.getDetail()

        } else {
          this.$message.error(res.data.msg)
        }
      })
    }, 

    toggleStatus(row) {
      row.ddl_status = row.ddl_status === '完成' ? '未完成' : '完成';
      request.post('/calender/update', row).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.$message.success('修改成功')
        } else {
          this.$message.error(res.data.msg)
        }
      })
    },
    
    
  },
  
}
</script>

<style>
.date-cell {
  padding: 4px; /* 调整内边距以减少间距 */
  cursor: pointer; /* 鼠标悬停时显示指针 */
  height: 100px; /* 调整高度 */
  display: flex;
  align-items: start;
}

.day_num {
  margin: 2px 10px; /* 调整上下的外边距 */
  /* 调整位置偏左 */
  text-align: left;
}

.meta {
  margin: 2px 10px; /* 调整上下的外边距 */
  /* 调整位置偏左 */
  color: rgb(220, 85, 23);
}


.memos p {
  margin: 2px 0; /* 调整备忘录的上下外边距 */
  font-size: smaller;
  
}

.completed {
  color: green;
  font-weight: bold;
}

.incompleted {
  color: red;
  font-weight: bold;
}

</style>
