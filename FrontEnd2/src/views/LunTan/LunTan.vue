<template>
  <Layout> 
        <el-main>
          <el-card style="margin-bottom: 10px">
            <div slot="header" class="clearfix">
              <span>学习论坛</span>
            </div>
            <!-- 分类按钮和分类搜索框 -->
          <div class="forum-container">
            <!-- 分类按钮 -->
            <div class="board-buttons">
              <!-- 搜索框 -->
              <el-input
                v-model="searchQuery"
                placeholder="请输入搜索内容"
                clearable
                prefix-icon="el-icon-search"
                class="search-input"
                @keyup.enter.native="handleSearch"
                style="width: 300px; margin-left: auto;">
              </el-input>
            </div>
            
            <!-- 筛选框 -->
            <!-- 筛选框 -->
            <div class="filter-buttons">

              <el-select v-model="selectedBoard" placeholder="选择板块" @change="handleSearch" clearable>
                <el-option label="全部" value=""></el-option>
                <el-option label="学术" value="学术"></el-option>
                <el-option label="生活" value="生活"></el-option>
              </el-select>
              
              <el-select v-model="selectedTopic" placeholder="筛选主题" clearable>
                <el-option label="全部主题" value="全部主题"></el-option>
                <el-option label="课程" value="课程"></el-option>
                <el-option label="建议" value="建议"></el-option>
                <el-option label="求助" value="求助"></el-option>
              </el-select>
              
              <el-select v-model="selectedTime" placeholder="筛选时间" clearable>
                <el-option label="全部时间" value="全部时间"></el-option>
                <el-option label="今天" value="今天"></el-option>
                <el-option label="昨天" value="昨天"></el-option>
                <el-option label="最近一周" value="最近一周"></el-option>
              </el-select>
              
              <el-select v-model="selectedOrder" placeholder="排序" clearable>
                <el-option label="最近时间" value="最近时间"></el-option>
                <el-option label="最多回复数" value="最多回复数"></el-option>
                <el-option label="最多查看数" value="最多查看数"></el-option>
              </el-select>
            </div>


            

              <el-table :data="filteredTopics" style="width: 100%" @row-click="handleRowClick">
              <el-table-column type="index" label="序号"></el-table-column>
              <el-table-column prop="title" label="标题"  width="300"></el-table-column>
              <el-table-column prop="board" label="board"></el-table-column>
              <el-table-column prop="topic" label="topic"></el-table-column>
              <el-table-column prop="student_id" label="作者"></el-table-column>
              <el-table-column
                label="回复/查看数"
                prop="ReplyAndViewCount"
              ></el-table-column>
              <!-- <el-table-column prop="last_updated_time" label="最后发表" width="200"></el-table-column> -->
              <el-table-column prop="created_time" label="创建时间" width="200"></el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[4, 6, 8, 10]"
              :page-size="pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="totalTopics"
            ></el-pagination>

            <!-- 快速发帖 -->   
              <div class="quick-post">
                <!-- 选择主题分类 (board) -->
                <div style="display: flex; justify-content: center;">
                  <div style="margin-right: 20px;">
                    <el-select v-model="newPost.board" placeholder="选择board">
                      <el-option label="学术" value="学术"></el-option>
                      <el-option label="生活" value="生活"></el-option>
                    </el-select>
                  </div>

                  <div>
                    <el-select v-model="newPost.topic" placeholder="选择topic">
                      <el-option label="课程" value="课程"></el-option>
                      <el-option label="建议" value="建议"></el-option>
                      <el-option label="求助" value="求助"></el-option>
                    </el-select>
                  </div>
                </div>

                <div style="height: 20px;"></div>

                <!-- 话题标题 -->
                <el-input placeholder="话题标题" v-model="newPost.title" class="post-title"></el-input>

                <!-- 话题正文 -->
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
  </Layout>      
</template>

<script>
import ValidCode from "@/views/ValidCode";
import axios from "axios";
import request from "@/utils/request";
import Layout from '@/components/Layout.vue'

export default {
  components: {
        Layout
    },
    data() {
  return {
    pageSize: 4,
    currentPage: 1,
    selectedBoard: '',
    selectedTopic: '全部主题',
    isCollapse: false,
    asideWidth: '200px',
    collapseIcon: 'el-icon-s-fold',
    searchQuery: '',
    selectedTime: '',
    selectedOrder: '',
    topics: [
    ],
    newPost: {
      board: '',
      title: '',
      content: '',
      topic: '' 
    },
    newComment: {
      topicId: null,
      content: ''
    }
  }
},
computed: {
  filteredTopics() {
    let filtered = this.topics.filter(topic => {
      const isBoardMatch = this.selectedBoard === '' || topic.board === this.selectedBoard;
      const isTopicMatch = this.selectedTopic === '全部主题' || topic.topic === this.selectedTopic;
      const isTimeMatch = this.filterByTime(topic.created_time);

      return isBoardMatch && isTopicMatch && isTimeMatch &&
             (this.searchQuery.trim() === '' || topic.title.includes(this.searchQuery.trim()));
    });

    // 根据排序条件排序
    if (this.selectedOrder === '最近时间') {
      filtered.sort((a, b) => new Date(b.created_time) - new Date(a.created_time));
    } else if (this.selectedOrder === '最多回复数') {
      filtered.sort((a, b) => b.reply_count - a.reply_count);
    } else if (this.selectedOrder === '最多查看数') {
      filtered.sort((a, b) => b.view_count - a.view_count);
    }

    return filtered.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize);
  },
  totalTopics() {
    return this.topics.filter(topic => {
      const isBoardMatch = this.selectedBoard === '' || topic.board === this.selectedBoard;
      const isTopicMatch = this.selectedTopic === '全部主题' || topic.topic === this.selectedTopic;
      const isTimeMatch = this.filterByTime(topic.last_updated_time);

      return isBoardMatch && isTopicMatch && isTimeMatch &&
             (this.searchQuery.trim() === '' || topic.title.includes(this.searchQuery.trim()));
    }).length;
  }
}


,
mounted(){
  this.fetchTopics();
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
    formatReplyAndViewCount(row) {
      return `${row.reply_count}/${row.view_count}`;
    },
    handleRowClick(row, event) {
    this.$router.push({ name: 'TopicDetail', params: { id: row.post_id } });
  },
  handleSizeChange(val) {
    this.pageSize = val;
  },
  handleCurrentChange(val) {
    this.currentPage = val;
  },
//获取后端话题
    fetchTopics() {
    request.get('/forum/post/get').then(res => {
      if (res.status === 200) {
        this.topics = res.data;  //设置获取到的话题列表
        console.log(this.topics)
      } else {
        this.$message.error(res.msg);
      }
    }).catch(error => {
      console.error("获取话题列表失败:", error);
    });
  },

  submitPost() {
    // 判断是否填写了board、title、content、topic
    if (!this.newPost.board || !this.newPost.title || !this.newPost.content || !this.newPost.topic) {
      this.$message.error('请填写完整信息');
      return;
    }
    request.post('/forum/post/put', this.newPost)
      .then(res => {
        console.log("尝试上传推文");
        console.log(res);
        if (res.status === 200) {
          this.$message.success('上传推文成功');
          // 清空表单
          this.newPost.board = '';
          this.newPost.title = '';
          this.newPost.content = '';
          this.newPost.topic = '';
        } else {
          this.$message.error(res.data.msg);
        }
        this.fetchTopics(); // 上传成功后刷新话题列表
      })
      .catch(error => {
        console.error("上传推文失败:", error);
      });
  },


  //调整日期显示
  formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    return date.toLocaleDateString('en-US', options);
  },
  handleSearch() {
  if (this.searchQuery.trim() !== '') {
    let lowerCaseQuery = this.searchQuery.trim().toLowerCase();
    this.topics = this.topics.filter(topic => topic.title.toLowerCase().includes(lowerCaseQuery));
  } else {
    this.fetchTopics(); // 如果搜索框为空，则重新获取所有话题
  }
},

  filterByTime(createdTime) {
    const now = new Date();
    const createdDate = new Date(createdTime);
    if (this.selectedTime === '全部时间') {
      return true;
    } else if (this.selectedTime === '今天') {
      return createdDate.toDateString() === now.toDateString();
    } else if (this.selectedTime === '昨天') {
      const yesterday = new Date(now);
      yesterday.setDate(now.getDate() - 1);
      return createdDate.toDateString() === yesterday.toDateString();
    } else if (this.selectedTime === '最近一周') {
      const lastWeek = new Date(now);
      lastWeek.setDate(now.getDate() - 7);
      return createdDate >= lastWeek;
    }
    return true;
  },

  }
}
</script>

<style scoped>
.forum-container {
  width: 80%;
  margin: auto;
}
.board-buttons {
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
