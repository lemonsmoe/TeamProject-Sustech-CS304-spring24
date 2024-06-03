<template>
  <div>
    <div>
      <el-table :data="workshopData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe style="width: 100%; margin-bottom: 10px">
        <el-table-column type="index" label="序号" width=100px :align="'center'"></el-table-column>
        <el-table-column prop="tutor_name" label="老师姓名" :align="'center'"></el-table-column>
        <el-table-column prop="subject" label="教授课程" :align="'center'"></el-table-column>
        <el-table-column prop="content" label="课程内容" :align="'center'"></el-table-column>
        <el-table-column
          label="时间"
          :align="'center'"
          width=200px 
          :formatter="row => `${row.time_start} - ${row.time_end}`">
        </el-table-column>
        <!-- <el-table-column prop="time_start" label="开始时间" :align="'center'"></el-table-column>
        <el-table-column prop="time_end" label="结束时间" :align="'center'"></el-table-column> -->
        <el-table-column prop="location" label="地点" :align="'center'"></el-table-column>
        <el-table-column label="操作" :align="'center'">
          <template slot-scope="scope">

            <el-button @click="handleDeleteWorkshop(scope.$index, scope.row)" type="text" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 
        AI-generated-content
        tool: Copilot
        version: latest
        usage: 询问如何分页
      -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 10, 20]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="workshopData.length"
      ></el-pagination>
      <el-button type="primary" @click="handleAddWorkshop">添加习题课</el-button>
    </div>

    <div>
      <!-- 添加新习题课 -->
      <el-dialog :visible.sync="addworkshop" width="600px">
        <el-form ref="workshopform" :model="form" label-width="80px">
          
          <el-form-item label="老师姓名">
            <!-- <el-input v-model="workshopform.tutor_id"></el-input> -->
            <el-select v-model="workshopform.tutor_id" placeholder="请选择老师">
              <el-option
                v-for="item in teacherData"
                :key="item.tutor_id"
                :label="item.tutor_id+': '+item.name"
                :value="item.tutor_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="教授课程">
            <el-input v-model="workshopform.subject"></el-input>
          </el-form-item>
          <el-form-item label="课程内容">
            <el-input v-model="workshopform.content"></el-input>
          </el-form-item>

          <el-form-item label="课程日期">
            <el-date-picker
              v-model="workshopform.date"
              type="date"
              placeholder="选择日期"
              
            ></el-date-picker>
          </el-form-item>
          <!-- 
            AI-generated-content
            tool: Copilot
            version: latest
            usage: 询问如何选择时间段
          -->
          <el-form-item label="课程时间">
            <el-select v-model="workshopform.time" placeholder="选择时间段">
              <el-option
                v-for="(time, index) in timeSlots"
                :key="index"
                :label="time"
                :value="time"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="地点">
            <el-input v-model="workshopform.location"></el-input>
          </el-form-item>
        </el-form>

        <el-button type="primary" @click="confirmAddWorkshop" :align="'center'">立即创建</el-button>
        <el-button type="info" @click="cancelAddWorkshop" :align="'center'">取消</el-button>
      </el-dialog>
  
    
    </div>
  </div>
</template>
<script>
  import request from "@/utils/request";
  
  export default {
    name: 'Workshop',
    components: {
    },
    data() {
      return {
        pageSize: 5,
        currentPage: 1,
        teacherData:[],
        workshopData:[],
        addworkshop:false,
        workshopform: {
          tutor_id: '',
          subject: '',
          content: '',
          date: '',
          time: '',
          location: ''
        },
        timeSlots: ['8:00 - 9:50', '10:20 - 12:10', '14:00 - 15:50', '16:20 - 18:10'],

      }
    },
    mounted() {
    
    },
    created() {
      // 在组件创建后立即发送请求
      this.getAllTutor()
      this.getAllWorkshop()

    },
    methods: {
      handleSizeChange(val) {
        this.pageSize = val;
      },
      handleCurrentChange(val) {
        this.currentPage = val;
      },
      getAllTutor() {
        // 获取所有老师信息
        request.get('/tutorial/tutors/get').then(res=>{
          console.log(res);
          if (res.status == 200) {
            this.teacherData = res.data;
            console.log(res.data);
  
          }
          else{
  
          }
          
        })
      },
      getAllWorkshop() {
        // 获取所有习题课信息
        request.get('/tutorial/workshops/get').then(res=>{
          console.log(res);
          console.log("workshopData")
          if (res.status == 200) {
            
            this.workshopData = res.data;
            console.log(res.data);
          }
          else{

          }
          
        })
      },
      handleAddWorkshop() {
        // 添加习题课
        this.addworkshop = true

        this.workshop.tutor_id = ''
        this.workshop.subject = ''
        this.workshop.content = ''
        this.workshop.date = ''
        this.workshop.time = ''
        this.workshop.location = ''
      },
      confirmAddWorkshop(){
        // 确认添加（更新表格）

        //判断是否所有信息都填写了
        if (this.workshopform.tutor_id === '' 
        || this.workshopform.subject === '' 
        || this.workshopform.content === '' 
        || this.workshopform.date === '' 
        || this.workshopform.time === '' 
        || this.workshopform.location === '') {
          this.$message.error('请填写完整信息')
          return
        }

        var list = {
          'tutor_id': this.workshopform.tutor_id,
          'subject': this.workshopform.subject,
          'content': this.workshopform.content,
          'date': this.workshopform.date.toLocaleDateString(),
          'time': this.workshopform.time,
          'location': this.workshopform.location
        }

        request.post('/tutorial/workshops/add', list).then(res=>{
          // console.log("交互成功")
          console.log("fetchDataDone")
          console.log(res)
          if (res.status === 200) {
            this.$message.success('添加成功')
            this.getAllWorkshop()
          } else {
            this.$message.error(res.data.msg)
          }
          
        })
        
        this.addworkshop = false
      },
      
      cancelAddWorkshop(){
        // 取消添加
        this.addworkshop = false
      },

      handleDeleteWorkshop(index, row) {
        // 前端删除
        //this.tableData.splice(index, 1)
        
        // 后端删除
        let workshop_id = row.workshop_id
        request.post('/tutorial/workshops/delete', {
          workshop_id: workshop_id
        }).then(res => {
          console.log(res)
          if (res.status === 200) {
            this.$message.success('删除成功')
          } else {
            this.$message.error(res.data.msg)
          }
        })
      }, 

    },
      
  }
</script>

<style>


</style>
  
  
