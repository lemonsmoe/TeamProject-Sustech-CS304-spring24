<template>
  <div>
    <el-container>
      <el-aside :width="asideWidth">
        <div style="height: 60px; line-height: 60px; font-size: 20px; display: flex; align-items: center; justify-content: center">
          <img src="@/assets/nkd.jpg" style="width: 30px;" alt="">
          <span class="logo-title" v-show="!isCollapse">学术助手</span>
        </div>
        <el-menu router :collapse="isCollapse" :collapse-transition="false" background-color="#001529"
                 active-text-color="#fff" text-color="rgba(255, 255, 255, 0.65)" :default-active="$route.path"
                 style="border: none">
          <el-menu-item index="/">
            <i class="el-icon-s-home"></i>
            <span slot="title">系统首页</span>
          </el-menu-item>
          <el-menu-item index="/login">
            <i class="el-icon-s-custom"></i>
            <span slot="title">登录</span>
          </el-menu-item>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i><span>学生应用</span></template>
            <el-menu-item index="/xuanke">选课系统</el-menu-item>
            <el-menu-item index="/luntan">学习论坛</el-menu-item>
            <el-menu-item index="/fudao">预约辅导</el-menu-item>
            <el-menu-item index="/rili">学习日历</el-menu-item>
            <el-menu-item index="/pingjiao">评教系统</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header style="height: 60px; line-height: 60px; display: flex; align-items: center; box-shadow: 2px 0 6px rgba(0, 21, 41, .35);">
          <i :class="collapseIcon" @click="handleCollapse" style="font-size: 26px"></i>
          <!--          <el-breadcrumb separator="/" style="margin-left: 20px">-->
          <!--            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>-->
          <!--            <el-breadcrumb-item :to="{ path: '/' }">课程管理</el-breadcrumb-item>-->
          <!--          </el-breadcrumb>-->

          <div style="flex: 1; display: flex; justify-content: flex-end; align-items: center">
            <i class="el-icon-quanping" @click="handleFullScreen" style="font-size: 25px"></i>
            <el-dropdown placement="bottom">
              <div style="display: flex; align-items: center; cursor: pointer">
                <img src="@/assets/nkd.jpg" alt="" style="width: 40px; height: 40px; margin: 0 5px">
                <span>用户中心</span>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>个人信息</el-dropdown-item>
                <el-dropdown-item>修改密码</el-dropdown-item>
                <el-dropdown-item>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </el-header>
        <el-main>
          <el-card style="margin-bottom: 10px">
            <div slot="header" class="clearfix">
              <span>学习论坛</span>
            </div>
            <!-- 分类按钮和分类搜索框 -->
          <div class="forum-container">
            <!-- 分类按钮 -->
            <div class="category-buttons">
              <el-button-group>
                <el-button>全部</el-button>
                <el-button>建议</el-button>
                <el-button>求助</el-button>
              </el-button-group>
              <!-- 搜索框 -->
              <el-input placeholder="search" v-model="searchQuery" class="search-input">
                <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
              </el-input>
            </div>
            
            <!-- 筛选框 -->
            <div class="filter-buttons">
              <el-select v-model="selectedTopic" placeholder="筛选主题">
                <el-option label="全部主题" value="all"></el-option>
                <el-option label="技术" value="tech"></el-option>
                <el-option label="生活" value="life"></el-option>
              </el-select>
              <el-select v-model="selectedTime" placeholder="筛选时间">
                <el-option label="全部时间" value="all"></el-option>
                <el-option label="最近一周" value="week"></el-option>
                <el-option label="最近一月" value="month"></el-option>
              </el-select>
              <el-select v-model="selectedOrder" placeholder="排序">
                <el-option label="最后发表" value="last"></el-option>
                <el-option label="精华" value="highlight"></el-option>
                <el-option label="推荐" value="recommend"></el-option>
                <el-option label="刷新" value="refresh"></el-option>
              </el-select>
            </div>
            
    
            
            <!-- 话题展示 -->
          <div class="topics-header">
            类别
            <span></span>作者
            <span></span>回复/查看数
            <span></span>最后发表
          </div>
          <div class="topics-list">
            <router-link
              class="topic-item"
              v-for="topic in topics"
              :key="topic.id"
              :to="{ name: 'TopicDetail', params: { id: topic.id } }">
              <div class="topic-title">{{ topic.title }}</div>
              <div class="topic-info">
                <span class="category">{{ topic.category }}</span>
                <span class="author">{{ topic.author }}</span>
                <span class="stats">{{ topic.replies }}/{{ topic.views }}</span>
                <span class="last-post">{{ topic.lastPost }}</span>
              </div>
            </router-link>
          </div>

            

            <!-- 分页 -->
            <el-pagination
              background
              layout="prev, pager, next"
              :total="topics.length"
              class="pagination">
            </el-pagination>

            <!-- 快速发帖 -->
            <div class="quick-post">
              <el-input placeholder="学生学号" v-model="newPost.studentId" class="post-student-id"></el-input>
  
              <el-select v-model="newPost.category" placeholder="选择主题分类">
                <el-option label="技术" value="tech"></el-option>
                <el-option label="生活" value="life"></el-option>
              </el-select>

              <div style="height: 20px;"></div>

              <el-input placeholder="话题标题" v-model="newPost.title" class="post-title"></el-input>
              <el-input
                type="textarea"
                placeholder="话题正文"
                v-model="newPost.content"
                class="post-content">
              </el-input>
              <div class="post-actions">
                <el-button type="primary" @click="submitPost">发表帖子</el-button>
              </div>
            </div>
          </div>
          </el-card>
        </el-main>

      </el-container>
    </el-container>
  </div>
</template>

<script>
import ValidCode from "@/views/ValidCode";
import axios from "axios";
import request from "@/utils/request";

export default {
  data() {
    return {
      isCollapse: false,
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold',
      searchQuery: '',
      selectedTopic: '',
      selectedTime: '',
      selectedOrder: '',
      topics: [
        { id: 1, title: '话题1', category: '生活', author: 'admin', replies: 10, views: 100, lastPost: '昨天 10:26' },
        { id: 2, title: '话题2', category: '生活', author: 'admin', replies: 10, views: 100, lastPost: '昨天 10:26' },
        // 继续添加更多话题
      ],
      newPost: {
        studentId: '', // 新增字段
        category: '',
        title: '',
        content: ''
      }
    }
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
    handleSearch() {
      console.log('搜索关键词:', this.searchQuery);
      // 处理搜索逻辑
      this.filteredTopics();
    },
    submitPost() {
      console.log('发表帖子:', this.newPost);

      // 获取学生学号
      const studentId = this.newPost.studentId;

      // 校验学号是否为空
      if (!studentId) {
        this.$message.error('请输入学生学号');
        return;
      }
      console.log("sss")
      // 调用后端 API 获取特定学生的日历项
      request.get('/tutorial/tutors').then(res => {
        console.log("交互成功");
        console.log(res);
        console.log(res.data);
        if (res.status === 200) {
          console.log("收到后端回复200");
          this.$message.success('获取DDL数据成功');
          console.log(res.ddl_id);
          console.log(res.ddl_time);
        } else {
          this.$message.error(res.msg);
        }
      }).catch(error => {
        console.error("获取DDL数据失败:", error);
      });

      // 处理发帖逻辑
    }
  },
  computed: {
  filteredTopics() {
    let result = this.topics;
    if (this.selectedTopic !== 'all') {
      result = result.filter(topic => topic.category === this.selectedTopic);
    }
    if (this.searchQuery) {
      result = result.filter(topic => topic.title.includes(this.searchQuery) || topic.content.includes(this.searchQuery));
    }
    // 添加排序逻辑等
    return result;
  }
}

}
</script>

<style scoped>
.forum-container {
  width: 80%;
  margin: auto;
}
.category-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.search-input {
  width: 200px;
}
.filter-buttons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.topics-header, .topic-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px 0;
}
.topics-header {
  font-weight: bold;
  border-bottom: 2px solid #ddd; /* 添加下边框 */
}
.topic-item {
  border-bottom: 1px solid #ddd; /* 添加下边框 */
  padding: 10px 0; /* 添加内边距 */
}
.topic-item {
  text-decoration: none; /* 去除下划线 */
  color: inherit; /* 使用继承的颜色 */
}

.topic-item:hover {
  text-decoration: none; /* 去除下划线 */
}

.topic-title {
  color: black; /* 设置标题颜色为黑色，或根据需要调整 */
}

/*可选：为链接的其他状态设置颜色
.topic-item:visited {
  color: inherit; 使用继承的颜色，防止变成紫色 
}*/


.topics-header {
  display: flex;
  justify-content: flex-end;
  padding-right: 10px; 
  margin-left: auto; 
  font-weight: bold;
  border-bottom: 2px solid #ddd; 
}
.topics-header span {
  margin-left: 10px; 
}

.topic-info span {
  margin-right: 15px; 
}
.quick-post {
  margin-top: 20px;
}
.post-title, .post-content {
  margin-bottom: 10px;
}
.post-actions {
  display: flex;
  justify-content: flex-end;
}
.pagination {
  margin-top: 20px;
}
</style>
