<template>
    <div>
      <div>

        <el-form :inline="true" :model="query" class="demo-form-inline" @keydown.enter.native="handleQuery">
                  
            <el-form-item label="课程编码">
                <el-input v-model="query.course_id" placeholder="请输入课程编码"></el-input>
            </el-form-item>
            <el-form-item label="课程名称">
                <el-input v-model="query.course_name" placeholder="请输入课程名称"></el-input>
            </el-form-item>
            <el-form-item label="任课教师">
                <el-input v-model="query.course_teacher" placeholder="请输入任课教师"></el-input>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="handleQuery">查询</el-button>
            </el-form-item>
            <!-- <el-form-item>
                <el-button type="danger" @click="toMenu">返回</el-button>
            </el-form-item> -->
        </el-form>

        <el-table :data="courseData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe style="width: 100%; margin-bottom: 10px">
          <el-table-column type="index" label="序号" width = 100px :align="'center'"></el-table-column>
          <el-table-column prop="course_id" label="课程编号" :align="'center'"></el-table-column>
          <el-table-column prop="course_name" label="课程名称" :align="'center'"></el-table-column>

          
          <el-table-column label="操作" :align="'center'">
            <template slot-scope="scope">
              
              <el-button @click="handleAddDDL(scope.$index, scope.row)" type="text" size="small">布置作业</el-button>
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
          :total="courseData.length"
        ></el-pagination>
      </div>
  
      <div>
  
        <!-- 添加新DDL -->
        <el-dialog :visible.sync="addDDL" width="600px">
          <el-form ref="ddlform" :model="form" label-width="80px">
            
            <el-form-item label="课程编号">
              <el-input v-model="ddlform.course_id"></el-input>
            </el-form-item>
            
            <el-form-item label="ddl时间">
              <el-date-picker
                v-model="ddlform.ddl_time"
                type="datetime"
                placeholder="选择日期和时间"
                format="yyyy-MM-dd HH:mm"
                value-format="yyyy-MM-dd HH:mm">
              </el-date-picker>
            </el-form-item>
            <el-form-item label="ddl标题">
              <el-input v-model="ddlform.ddl_title"></el-input>
            </el-form-item>
            <el-form-item label="ddl内容">
              <el-input v-model="ddlform.ddl_content"></el-input>
            </el-form-item>
            
          </el-form>
      
          <el-button type="primary" @click="confirmAddDDL" :align="'center'">立即添加</el-button>
          <el-button type="info" @click="cancelAddDDL" :align="'center'">取消</el-button>
        </el-dialog>
      
      </div>
    </div>
  </template>
  <script>
    import request from "@/utils/request";
    
    export default {
      name: 'Teacher',
      components: {
      },
      data() {
        return {
          pageSize: 5,
          currentPage: 1,
          
          courseData:[
            // {
            //   course_id: 'CS101',
            //   course_name: '不知道什么课程',
            //   course_teacher: '不知道什么老师',

            // },
            // {
            //   course_id: 'CS102',
            //   course_name: '不知道什么课程2',
            //   course_teacher: '不知道什么老师2',

            // },

          ],
          query: {
        
            course_id: '',
            course_name: '',
            course_teacher: '',

          },
  
          addDDL:false,
  
          ddlform: {
            course_id: '',
            ddl_time: '',
            ddl_title: '',
            ddl_content: '',
          },
  
  

        }
      },
      mounted() {
      
      },
      created() {
        // 在组件创建后立即发送请求
        this.handleQuery()
  
      },
      methods: {
        handleSizeChange(val) {
          this.pageSize = val;
        },
        handleCurrentChange(val) {
          this.currentPage = val;
        },
        getAllCourse() {
          // 获取所有课程信息
          request.post('/calender/course/get', {}).then(res=>{
            console.log(res);
            if (res.status == 200) {
              this.courseData = res.data;
              console.log(res.data);
            }
            else{
            }
          })
        },
        
        handleQuery() {
          // 筛选课程信息
          console.log(this.query)
          request.post('/calender/course/get',this.query).then(res=>{
            console.log(res);
            if (res.status == 200) {
              this.courseData = res.data;
              console.log(res.data);
            }
            else{
            }
          })
        },

        handleAddDDL(index,row) {
          // 前端添加
          this.addDDL = true

          this.ddlform.course_id = row.course_id
          this.ddlform.ddl_time = '' 
          this.ddlform.ddl_title = '' 
          this.ddlform.ddl_content = ''

    
        },
        confirmAddDDL(){
          // 确认添加（更新表格）
  
          //判断是否DDLform所有信息都填写了
          if (this.ddlform.course_id === '' 
          || this.ddlform.ddl_time === '' 
          || this.ddlform.ddl_title === '' 
          || this.ddlform.ddl_content === '') {
            this.$message.error('请填写完整信息')
            return
          }
    
          request.post('/calender/course_ddl/add', this.ddlform).then(res=>{
            // console.log("交互成功")
            console.log("fetchDataDone")
            console.log(res)
            if (res.status === 200) {
              this.$message.success('添加成功')
            } else {
              this.$message.error(res.data.msg)
            } 
          })
          this.addDDL = false
        },
        
        cancelAddDDL(){
          // 取消添加
          this.addDDL = false
        },

      },
        
    }
  </script>
  
  <style>
  
  
  </style>
    
    