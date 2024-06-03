<template>
  <div>
    <div>

      <el-table :data="teacherData.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe style="width: 100%; margin-bottom: 10px">
        <el-table-column type="index" label="序号" width = 100px :align="'center'"></el-table-column>
        <el-table-column prop="name" label="老师姓名" :align="'center'"></el-table-column>
        <el-table-column prop="subject" label="教授课程" :align="'center'"></el-table-column>
        <el-table-column prop="gender" label="老师性别" :align="'center'"></el-table-column>
        <el-table-column prop="age" label="老师年龄" :align="'center'"></el-table-column>
        <el-table-column prop="email" label="老师邮箱" width = 350px :align="'center'"></el-table-column>
        <el-table-column label="操作" :align="'center'">
          <template slot-scope="scope">
            
            <el-button @click="handleDeleteTutor(scope.$index, scope.row)" type="text" size="small">删除</el-button>
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
        :total="teacherData.length"
      ></el-pagination>
      <el-button type="primary" @click="handleAddTutor">添加老师</el-button>
    </div>

    <div>

      <!-- 添加新老师 -->
      <el-dialog :visible.sync="addteacher" width="600px">
        <el-form ref="teacherform" :model="form" label-width="80px">
          
          <el-form-item label="老师姓名">
            <el-input v-model="teacherform.name"></el-input>
          </el-form-item>
          <el-form-item label="教授课程">
            <el-input v-model="teacherform.subject"></el-input>
          </el-form-item>
          <el-form-item label="老师性别">
            <el-select v-model="teacherform.gender" placeholder="请选择性别">
              <el-option label="男" value="男"></el-option>
              <el-option label="女" value="女"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="老师年龄">
            <el-select v-model="teacherform.age" placeholder="请选择年龄">
              <el-option v-for="age in ageOptions" :key="age" :label="age" :value="age"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="老师邮箱">
            <el-input v-model="teacherform.email"></el-input>
          </el-form-item>
        </el-form>
    
        <el-button type="primary" @click="confirmAddTutor" :align="'center'">立即创建</el-button>
        <el-button type="info" @click="cancelAddTutor" :align="'center'">取消</el-button>
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
        teacherData:[],

        addteacher:false,

        teacherform: {
          name: '',
          subject: '',
          age: '',
          gender: '',
          email: ''
        },


        ageOptions: Array.from({ length: 100 }, (_, i) => i + 1), // 年龄选项从1到100
      }
    },
    mounted() {
    
    },
    created() {
      // 在组件创建后立即发送请求
      this.getAllTutor();

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
      handleAddTutor() {
        // 添加老师
        this.addteacher = true
  
        this.teacherform.name = ''
        this.teacherform.subject = ''
        this.teacherform.age = ''
        this.teacherform.gender = ''
        this.teacherform.email = ''
  
      },
      confirmAddTutor(){
        // 确认添加（更新表格）
  
        //判断是否teacherform所有信息都填写了
        if (this.teacherform.name === ''
        || this.teacherform.subject === ''
        || this.teacherform.gender === ''
        || this.teacherform.age === ''
        || this.teacherform.email === '') {
          this.$message.error('请填写完整信息')
          return
        }
        // 判断邮箱格式是否正确
        const emailRegex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        if (!emailRegex.test(this.teacherform.email)) {
          this.$message.error('请输入正确的邮箱地址');
          return;
        }
  
        const list = {
          'name': this.teacherform.name,
          'subject': this.teacherform.subject,
          'gender': this.teacherform.gender,
          'age': this.teacherform.age,
          'email': this.teacherform.email
        }
  
        request.post('/tutorial/tutors/add', list).then(res=>{
          // console.log("交互成功")
          console.log("fetchDataDone")
          console.log(res)
          if (res.status === 200) {
            this.$message.success('添加成功')
            this.getAllTutor()
          } else {
            this.$message.error(res.data.msg)
          }
          
        })
        
        this.addteacher = false
      },
      
      cancelAddTutor(){
        // 取消添加
        this.addteacher = false
      },

      handleDeleteTutor(index, row) {
        // 前端删除
        //this.tableData.splice(index, 1)
        
        // 后端删除
        let tutor_id = row.tutor_id
        request.post('/tutorial/tutors/delete', {
          tutor_id: tutor_id
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
  
  