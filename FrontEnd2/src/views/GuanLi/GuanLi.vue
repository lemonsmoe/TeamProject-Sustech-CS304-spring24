<template>
<Layout>
  <el-main>
    <el-card style=" margin-bottom: 10px" >
      <div slot="header" class="clearfix">
        <span>管理员</span>
      </div>
      <el-tabs v-model="activeTab" >
        <el-tab-pane label="辅导老师管理" name="teacher" class="classtype"></el-tab-pane>
        <el-tab-pane label="习题课管理" name="class" class="classtype"></el-tab-pane>
        <el-tab-pane label="课程管理" name="course" class="classtype"></el-tab-pane>
      </el-tabs>

      <div v-if="activeTab === 'teacher'">
        <Teacher></Teacher>
      </div>

      <div v-if="activeTab === 'class'">
        <Workshop></Workshop>
      </div>

      <div v-if="activeTab === 'course'">
        <Course></Course>
      </div>
        

    </el-card>
  </el-main>

</Layout>

</template>
<script>
import Layout from '@/components/Layout.vue'
import request from "@/utils/request";
import Teacher from './Teacher.vue'
import Workshop from './Workshop.vue'
import Course from './Course.vue';

export default {
  name: 'GuanLi',
  components: {
      Layout,
      Teacher,
      Workshop,
      Course
  },
  data() {
    return {
      activeTab: 'teacher', // 默认激活的选项卡
      
    }
  },
  mounted() {
  
  },
  created() {
    // 在组件创建后立即发送请求

  },
  methods: {
    
  },
    
}
</script>

<style>

</style>

