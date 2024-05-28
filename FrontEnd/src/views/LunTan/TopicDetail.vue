<template>
  <div>
    <el-container>
      <el-header style="height: 60px; line-height: 60px; display: flex; align-items: center; box-shadow: 2px 0 6px rgba(0, 21, 41, .35);">
        <el-button @click="goBack" icon="el-icon-arrow-left">返回</el-button>
        <i :class="collapseIcon" @click="handleCollapse" style="font-size: 26px"></i>
        <div style="flex: 1; display: flex; justify-content: flex-end; align-items: center">
          <i class="el-icon-quanping" @click="handleFullScreen" style="font-size: 25px"></i>
          <el-dropdown placement="bottom">
            <div style="display: flex; align-items: center; cursor: pointer">
              <img src="@/assets/logo.png" alt="" style="width: 40px; height: 40px; margin: 0 5px">
              <span>管理员</span>
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
          <h1>{{ topic.title }}</h1>
          <div class="forum-container">
            <div class="topic-content">{{ topic.content }}</div>
            <div class="comments-section">
              <el-card v-for="comment in comments" :key="comment.id" class="comment-card">
                <div class="comment-header">
                  <img :src="comment.userAvatar" alt="User Avatar" class="user-avatar">
                  <span>{{ comment.userName }}</span>
                </div>
                <div class="comment-body">{{ comment.text }}</div>
                <div class="comment-footer">
                  <el-button size="mini">评论</el-button>
                  <el-button size="mini">回复</el-button>
                </div>
              </el-card>
            </div>
            <el-pagination
              background
              layout="prev, pager, next"
              :total="comments.length"
              :page-size="10">
            </el-pagination>
            <el-input
              type="textarea"
              placeholder="发表您的评论..."
              v-model="newComment"
              class="quick-reply">
            </el-input>
            <el-button type="primary" @click="postComment">发表评论</el-button>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'TopicDetail',
  data() {
    return {
      topic: {
        title: 'Example Topic',
        content: 'This is an example topic content.'
      },
      comments: [
        { id: 1, userName: '用户1', userAvatar: 'path/to/avatar1.jpg', text: '非常好的帖子！' },
        { id: 2, userName: '用户2', userAvatar: 'path/to/avatar2.jpg', text: '非常有用的信息，谢谢分享。' }
      ],
      newComment: ''
    };
  },
  methods: {
    handleCollapse() {
      console.log('Toggle sidebar');
    },
    handleFullScreen() {
      console.log('Toggle full screen');
    },
    postComment() {
      if (this.newComment.trim() !== '') {
        const newId = this.comments.length + 1;
        this.comments.push({
          id: newId,
          userName: '新用户',
          userAvatar: 'path/to/defaultAvatar.jpg',
          text: this.newComment
        });
        this.newComment = ''; // Reset the input after posting
        alert('评论已发表！');
      } else {
        alert('请输入评论内容！');
      }
    },
    goBack() {
    this.$router.go(-1);  // 返回前一个页面
  }
  }
};
</script>

<style scoped>
.forum-container {
  width: 80%;
  margin: auto;
}
.topic-content {
  font-size: 16px;
  margin-top: 20px;
}
.comment-card {
  margin-top: 20px;
}
.comment-header {
  display: flex;
  align-items: center;
}
.user-avatar {
  width: 40px;
  height: 40px;
  borderRadius: 50%;
  marginRight: 10px;
}
.comment-body {
  margin-top: 10px;
}
.comment-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
.quick-reply {
  margin-top: 20px;
}
</style>
