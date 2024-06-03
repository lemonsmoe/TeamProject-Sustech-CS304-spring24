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

        <el-table :data="myCourseData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe style="width: 100%; margin-bottom: 10px">
          <el-table-column type="index" label="序号" width = 100px :align="'center'"></el-table-column>
          <el-table-column prop="course_id" label="课程编号" :align="'center'"></el-table-column>
          <el-table-column prop="course_name" label="课程名称" :align="'center'"></el-table-column>

          
          <el-table-column label="操作" :align="'center'">
            <template slot-scope="scope">
              
              <el-button @click="handleDeleteCourse(scope.$index, scope.row)" type="text" size="small">取消订阅</el-button>
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
          :total="myCourseData.length"
        ></el-pagination>
      </div>
  
      
    </div>
  </template>
  <script>
    import request from "@/utils/request";
    
    export default {
      name: 'MyCourse',
      components: {
      },
      data() {
        return {
          pageSize: 5,
          currentPage: 1,
          
          courseData:[],
          myCourseData:[],
          query: {
        
            course_id: '',
            course_name: '',
            course_teacher: '',

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
        
        handleQuery() {
          // 筛选课程信息
          console.log(this.query)
          request.post('/calender/course/get',this.query).then(res=>{
            console.log(res);
            if (res.status == 200) {
              this.courseData = res.data;
              console.log("all course");
              console.log(res.data);

              this.getMyCourse() 

              
            }
            else{
            }
          })
          
        },
        getMyCourse() {
          request.get('/calender/subscribe/get').then(res=>{
            console.log(res);
            if (res.status == 200) {
              console.log("my course");
              console.log(res.data);
              let courses = res.data
              // this.myCourseData = courses

              for (let i = 0; i < courses.length; i++) {
                for (let j = 0; j < this.courseData.length; j++) {
                  if (courses[i] == this.courseData[j].course_id) {
                    this.myCourseData.push(this.courseData[j])
                  }
                }
              
              }
              console.log(this.myCourseData)
            }
            else{
            }
          })
        },
        handleDeleteCourse(index,row) {
          const list = {
            course_id: row.course_id,
          }
          request.post('/calender/subscribe/delete', list).then(res=>{
            // console.log("交互成功")
            console.log("fetchDataDone")
            console.log(res)
            if (res.status === 200) {
              this.$message.success('取消成功')
              this.myCourseData.splice(index, 1)
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
    
    