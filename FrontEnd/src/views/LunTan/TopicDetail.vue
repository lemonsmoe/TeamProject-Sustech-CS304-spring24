<template>
  <Layout>
    <el-main>
      <el-card style="margin-bottom: 10px">
        <!-- <div slot="header" class="clearfix"> -->
          <div class="back_button">
            <el-button type="text" @click="goBack">返回</el-button>
          </div>
          <!-- <span>学习论坛</span> -->

        <!-- 标题和正文部分 -->
        <el-card class="topic-detail-card">
          <h1 class="topic-title">{{ topic.title }}</h1>
          <div class="topic-meta">
            <span class="topic-board">{{ topic.board }}</span> | 
            <span class="topic-topic">{{ topic.topic }}</span> | 
            <span class="topic-author">作者: {{ topic.author }}</span> | 
            <span class="topic-time">发表于: {{ topic.created_time }}</span> | 
            <span class="topic-updated">最后更新: {{ topic.last_updated_time }}</span>
          </div>
          <div class="topic-content">{{ topic.content }}</div>
        </el-card>

        <!-- 评论区 -->
        <div class="forum-container">
          <div class="comments-section">
            <el-card v-for="comment in comments" :key="comment.id" class="comment-card">
              <div class="comment-container">
              <div class="comment-content">
                <div class="comment-head">{{ comment.student_id }}</div>
                <div class="comment-body">{{ comment.content }}</div>
              </div>
              <div class="comment-date">{{ comment.created_time }}</div>
            </div>
            </el-card>
          </div>
          
          <el-pagination
            background
            layout="prev, pager, next"
            :total="comments.length"
            :page-size="10"
            class="pagination-with-margin">
          </el-pagination>
          <el-input
            type="textarea"
            placeholder="发表您的评论...按下Ctrl+Enter快速发表"
            v-model="newComment.content"
            class="quick-reply"
            @keydown.enter.ctrl.native="postComment">
          </el-input>
          <el-button type="primary" class="quick-reply" @click="postComment">发表评论</el-button>
        </div>
      </el-card>
    </el-main>
  </Layout>
</template>

<script>
import Layout from '@/components/Layout.vue'
import request from "@/utils/request"; 

export default {
  name: 'TopicDetail',
  components: {
    Layout
  },
  data() {
    return {
      topic: {
        title: '',
        content: '',
        board: '',
        topic: '',
        created_time: '',
        last_updated_time: '',
        author: ''
      },
      comments: [],
      newComment: {
        post_id: this.$route.params.id,
        content: ''
      }
    };
  },
  mounted() {
    this.fetchTopicDetail();
    this.fetchComments(); 
  },
  created() {
    this.addView();
  },
  methods: {
    addView() {
      const topicId = this.$route.params.id;
      request.post('/forum/post/addview', { post_id: topicId }).then(res => {
        if (res.status !== 200) {
          this.$message.error(res.data.msg);
        }
      }).catch(error => {
        console.error("增加浏览量失败:", error);
      });
    },

    // <!-- AI-generated-content tool: chatGPT version: 4.o usage: 要求GPT生成获取话题细节信息的方法，然后我自己修改了相关参数和细节 -->
    fetchTopicDetail() {
      const topicId = this.$route.params.id; // 获取路由参数中的话题ID
      request.post('/forum/post/getcontent', { post_id: topicId }).then(res => {
        if (res.status === 200) {
          this.topic = res.data; // 将获取到的话题详情设置到topic
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(error => {
        console.error("获取话题详情失败:", error);
      });
    },
    
    fetchComments() {
      const topicId = this.$route.params.id;
      request.post('/forum/reply/get', { post_id: topicId }).then(res => {
        if (res.status === 200) {
          this.comments = res.data;
        } else {
          this.$message.error(res.data.msg);
        }
      }).catch(error => {
        console.error("获取评论列表失败:", error);
      });
    },

      // <!-- AI-generated-content tool: chatGPT version: 4.o usage: 要求GPT生成发表评论的方法框架，与发帖逻辑相似故属于重复工作，然后我自己修改了相关参数和细节，如路由信息 -->
    postComment() {
      if (this.newComment.content.trim() !== '') {
        request.post('/forum/reply/put', this.newComment)
          .then(res => {
            if (res.status === 200) {
              this.$message.success('评论已发表');
              // 重置评论输入框
              this.newComment.content = '';
              // 重新获取评论列表
              this.fetchComments();
            } else {
              this.$message.error(res.data.msg);
            }
          })
          .catch(error => {
            console.error("发表评论失败:", error);
          });
      } else {
        this.$message.error('请输入评论内容');
      }
    },
    goBack() {
      this.$router.go(-1); 
    }
  }
};
</script>

<style scoped>
.back_button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.topic-detail-card {
  margin-bottom: 20px;
  padding: 5px;
  border-radius: 20px;
}
.topic-title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
  margin-top: auto;
}
.topic-meta {
  font-size: 14px;
  color: #888;
  margin-bottom: 20px;
}
.topic-content {
  font-size: 16px;
  line-height: 1.5;
}
.forum-container {
  width: 80%;
  margin: auto;
}
.comment-card {
  /* 圆角边框 */
  border-radius: 20px;
  padding: 2px;
  margin-bottom: 3px;
}
.comment-header {
  display: flex;
  align-items: center;
}
.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
.comment-head {
  font-weight: bold;
  margin-right: 10px;
}
.comment-body {
  text-align: left;
}
.comment-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
.quick-reply {
  margin-top: 20px;
}
.pagination-with-margin {
  margin-top: 20px; 
}
.comment-container {
  display: flex;
  justify-content: space-between;
  align-items: start;
}
.comment-content {
  display: flex;
  align-items: start;
}
</style>
