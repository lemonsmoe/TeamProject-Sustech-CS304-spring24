<template>
  <Layout>
    <el-main>
      <el-card style=" margin-bottom: 10px" >
        <!-- <div slot="header" class="clearfix">
          <span>选课推荐系统</span>
        </div> -->
        <el-tabs v-model="activeTab">
          
          <el-tab-pane label="方案管理" name="mystar" class="classtype">
            <keep-alive>
              <Star v-if="activeTab === 'mystar'"></Star>
            </keep-alive>
          </el-tab-pane> 
          <el-tab-pane label="选课规划" name="schedule" class="classtype">
            <keep-alive>
              <XuanKe v-if="activeTab === 'schedule'"></XuanKe>
            </keep-alive>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </el-main>

      
  </Layout>
</template>

<script>
import Layout from '@/components/Layout.vue'
import XuanKe from './XuanKe.vue';
import Star from './Star.vue';
import request from "@/utils/request";

export default {
  name: 'thomas',
  components: {
      Layout,
        XuanKe,
        Star,
  },
  data() {
    return {
      activeTab: 'mystar', // 默认激活的选项卡
    }
  },
  methods: {
  }
}
</script>