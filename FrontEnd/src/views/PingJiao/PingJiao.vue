<template>
  <Layout>
        <el-main>
          <el-card style="margin-bottom: 10px">
            <div slot="header" class="clearfix">
              <span>评教系统</span>
            </div>
            <el-form :inline="true" :model="form" class="demo-form-inline">
              <el-form-item label="课程类别">
                <el-select v-model="form.category" placeholder="请选择课程类别">
                  <el-option label="通识" value="general"></el-option>
                  <el-option label="专业必修" value="major_required"></el-option>
                  <el-option label="体育" value="sports"></el-option>
                  <el-option label="人文社科" value="humanities"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="排序方式">
                <el-select v-model="form.sort" placeholder="请选择排序方式">
                  <el-option label="评分高低" value="rating"></el-option>
                  <el-option label="评价人数多少" value="reviews"></el-option>
                </el-select>
              </el-form-item>
            </el-form>
          </el-card>

          <el-card v-for="(review, index) in reviews" :key="index" style="margin-bottom: 10px">
            <div slot="header" class="clearfix">
              <span>{{ review.course }}</span>
              <router-link :to="{ name: 'coursedetail', params: { id: review.id } }">
                <el-button style="float: right; padding: 3px 0" type="text" >查看详情</el-button>
              </router-link>
            </div>
            <div>
              <p>评分: {{ review.rating }} (评分人数: {{ review.ratingCount }})</p>
              <p>课程难度: {{ review.difficulty }}</p>
              <p>作业多少: {{ review.homework }}</p>
              <p>给分好坏: {{ review.grading }}</p>
              <p>收获大小: {{ review.harvest }}</p>
              <p>{{ review.comment }}</p>
            </div>
          </el-card>

          <el-pagination
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-size="pageSize"
            layout="total, prev, pager, next"
            :total="totalReviews">
          </el-pagination>
        </el-main>
  </Layout>
</template>
  

<script>
import Layout from '@/components/Layout.vue'
export default {
    components: {
        Layout
    },
  data() {
    return {
      isCollapse: false,
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold',
      form: {
        category: '',
        sort: ''
      },
      reviews: [
        // Example data
        {
          id: 1,
          course: '马克思主义基本原理',
          rating: 4.5,
          ratingCount: 43,
          difficulty: '较难',
          homework: '多',
          grading: '好',
          harvest: '多',
          comment: '这门课涵盖了哲学、马克思主义基本原理等内容，教授讲解细致。'
        },
        // More reviews...
      ],
      currentPage: 1,
      pageSize: 10,
      totalReviews: 50 // Example total
    }
  },
  methods: {
  handleFullScreen() {
    document.documentElement.requestFullscreen();
  },
  handleCollapse() {
    this.isCollapse = !this.isCollapse;
    this.asideWidth = this.isCollapse ? '64px' : '200px';
    this.collapseIcon = this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold';
  },
  viewDetails(id) {
    this.$router.push({ name: 'CourseDetail', params: { id } }); // 使用路由名称和参数跳转
  },
  handleCurrentChange(page) {
    this.currentPage = page;
    // Fetch new page data
  },
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
