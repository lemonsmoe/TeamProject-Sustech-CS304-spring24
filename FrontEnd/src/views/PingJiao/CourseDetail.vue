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
              <span>课程详细信息</span>
            </div>
            <div>
              <h2>{{ course.title }}</h2>
              <p>选课类别：{{ course.category }}</p>
              <p>授课类型：{{ course.type }}</p>
              <p>授课方式：{{ course.method }}</p>
              <p>开课单位：{{ course.unit }}</p>
              <p>学分：{{ course.credit }}</p>
            </div>
          </el-card>
  
          <el-card style="margin-bottom: 10px">
            <div slot="header" class="clearfix">
              <span>点评信息</span>
            </div>
            <div>
              <el-form :inline="true" :model="form" class="demo-form-inline">
                <el-form-item label="排序方式">
                  <el-select v-model="form.sort" placeholder="请选择排序方式">
                    <el-option label="评分高低" value="rating"></el-option>
                    <el-option label="获赞数量" value="likes"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="学期">
                  <el-select v-model="form.semester" placeholder="请选择学期">
                    <el-option label="2023春" value="2023spring"></el-option>
                    <el-option label="2023秋" value="2023fall"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="评分">
                  <el-input v-model="form.rating" placeholder="评分"></el-input>
                </el-form-item>
              </el-form>
            </div>
            <div class="comments-section">
              <el-card v-for="comment in filteredComments" :key="comment.id" class="comment-card">
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
              <el-pagination
                style="margin-top: 20px;"
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-size="pageSize"
                layout="total, prev, pager, next"
                :total="totalComments">
              </el-pagination>
            </div>
          </el-card>
  
          <el-card style="margin-bottom: 10px">
            <div slot="header" class="clearfix">
              <span>快速点评</span>
            </div>
            <div class="quick-reply-section">
              <el-input
                type="textarea"
                placeholder="发表您的评论..."
                v-model="newComment"
                class="quick-reply">
              </el-input>
              <el-button type="primary" @click="postComment" style="margin-top: 20px;">发表评论</el-button>
            </div>
          </el-card>
        </el-main>
      </el-container>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        course: {
          title: '马克思主义基本原理',
          category: '计划',
          type: '理论课',
          method: '本科计划内课程',
          unit: '马克思主义学院',
          credit: 2.5
        },
        form: {
          sort: '',
          semester: '',
          rating: ''
        },
        comments: [
          { id: 1, userName: '用户1', userAvatar: 'path/to/avatar1.jpg', text: '非常好的课程！', rating: 4.5, semester: '2023spring', likes: 10 },
          { id: 2, userName: '用户2', userAvatar: 'path/to/avatar2.jpg', text: '课程内容很丰富，受益匪浅。', rating: 4.0, semester: '2023fall', likes: 20 },
          { id: 3, userName: '用户3', userAvatar: 'path/to/avatar3.jpg', text: '讲解详细，推荐。', rating: 5.0, semester: '2023spring', likes: 15 }
        ],
        newComment: '',
        currentPage: 1,
        pageSize: 10,
        totalComments: 3
      };
    },
    computed: {
      filteredComments() {
        let result = this.comments;
        if (this.form.semester) {
          result = result.filter(comment => comment.semester === this.form.semester);
        }
        if (this.form.rating) {
          result = result.filter(comment => comment.rating >= parseFloat(this.form.rating));
        }
        if (this.form.sort === 'rating') {
          result = result.sort((a, b) => b.rating - a.rating);
        } else if (this.form.sort === 'likes') {
          result = result.sort((a, b) => b.likes - a.likes);
        }
        return result;
      }
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
            text: this.newComment,
            rating: 5.0,
            semester: '2023spring',
            likes: 0
          });
          this.newComment = ''; // Reset the input after posting
          alert('评论已发表！');
        } else {
          alert('请输入评论内容！');
        }
      },
      goBack() {
        this.$router.go(-1);  // 返回前一个页面
      },
      handleCurrentChange(page) {
        this.currentPage = page;
        // Fetch new page data
      }
    }
  };
  </script>
  
  <style scoped>
  .forum-container {
    width: 80%;
    margin: auto;
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
    border-radius: 50%;
    margin-right: 10px;
  }
  .comment-body {
    margin-top: 10px;
  }
  .comment-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 10px;
  }
  .quick-reply-section {
    margin-top: 20px;
  }
  </style>
  