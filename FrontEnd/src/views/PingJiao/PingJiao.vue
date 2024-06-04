<template>
  <Layout>
    <el-main>
      <el-card style="margin-bottom: 10px">
        <div slot="header" class="clearfix">
          <span>评教系统</span>
        </div>
        <el-form :inline="true" :model="form" class="demo-form-inline">
          <el-form-item label="课程类别">
            <el-select v-model="form.category" placeholder="请选择课程类别" @change="fetchCourseBriefs">
              <el-option label="全部" value=""></el-option>
              <el-option label="培养环节" value="培养环节"></el-option>
              <el-option label="通识必修课" value="通识必修课"></el-option>
              <el-option label="专业基础课" value="专业基础课"></el-option>
              <el-option label="专业核心课" value="专业核心课"></el-option>
              <el-option label="专业选修课" value="专业选修课"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="排序方式">
            <el-select v-model="form.sort" placeholder="请选择排序方式" @change="fetchCourseBriefs">
              <el-option label="评分高低" value="rating"></el-option>
              <el-option label="评价人数多少" value="reviews"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="搜索课程">
            <el-input v-model="form.searchQuery" placeholder="请输入课程名称" @input="fetchCourseBriefs"></el-input>
          </el-form-item>
        </el-form>
      </el-card>

      <el-table :data="filteredCourses.slice((currentPage - 1) * pageSize, currentPage * pageSize)" border style="width: 100%">
  <el-table-column prop="course_name" label="课程名"></el-table-column>
  <el-table-column prop="course_id" label="课程ID"></el-table-column>
  <el-table-column prop="course_type" label="授课类型"></el-table-column>
  <el-table-column prop="credit" label="学时"></el-table-column>
  <el-table-column prop="college" label="开课单位"></el-table-column>
  <el-table-column prop="avg_rating" label="平均评分"></el-table-column>
  <el-table-column prop="review_count" label="评价人数"></el-table-column>
  <el-table-column
    label="操作"
    width="180">
    <template slot-scope="scope">
      <router-link :to="{ name: 'coursedetail', params: { id: scope.row.course_id } }">
        <el-button type="text">查看详情</el-button>
      </router-link>
    </template>
  </el-table-column>
</el-table>

<el-pagination
  @current-change="handleCurrentChange"
  :current-page="currentPage"
  :page-size="pageSize"
  layout="total, prev, pager, next"
  :total="totalCourses">
</el-pagination>
    </el-main>
  </Layout>
</template>

<script>
import Layout from '@/components/Layout.vue'
import request from "@/utils/request";

export default {
  components: {
    Layout
  },
  data() {
    return {
      pagedCourses: [],
      isCollapse: false,
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold',
      form: {
        category: '',
        sort: '',
        searchQuery: ''
      },
      courses: [],
      currentPage: 1,
      pageSize: 5,
      totalCourses: 0
    };
  },
  computed: {
    filteredCourses() {
      let filtered = this.courses;

      if (this.form.category) {
        filtered = filtered.filter(course => course.course_type === this.form.category);
      }

      if (this.form.searchQuery) {
        filtered = filtered.filter(course => course.course_name.includes(this.form.searchQuery));
      }

      if (this.form.sort === 'rating') {
        filtered = filtered.sort((a, b) => b.avg_rating - a.avg_rating);
      } else if (this.form.sort === 'reviews') {
        filtered = filtered.sort((a, b) => b.review_count - a.review_count);
      }
      this.totalCourses = filtered.length;

      return filtered;
    }
  },
  mounted() {
    this.fetchCourseBriefs();
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
    handleCurrentChange(newPage) {
    this.currentPage = newPage;
    this.pagedCourses = this.filteredCourses.slice((newPage - 1) * this.pageSize, newPage * this.pageSize);
  },

       // <!-- AI-generated-content tool: chatGPT version: 4.o usage: 要求GPT生成获取课程细节信息的方法，因为涉及到多个方法api的利用，然后我自己调整细节 -->
    async fetchCourseBriefs() {
      try {
        const coursesResponse = await request.get('/evaluation/courses/brief');
        const reviewsResponse = await request.get('/evaluation/review/getbrief');
        
        if (coursesResponse.status === 200 && reviewsResponse.status === 200) {
          const courses = coursesResponse.data;
          const reviews = reviewsResponse.data;
          const reviewDict = {};
          
          reviews.forEach(review => {
            reviewDict[review.course_id] = review;
          });

          courses.forEach(course => {
            if (reviewDict[course.course_id]) {
              course.avg_rating = reviewDict[course.course_id].avg_rating;
              course.review_count = reviewDict[course.course_id].review_count;
            } else {
              course.avg_rating = 0;
              course.review_count = 0;
            }
          });

          this.courses = courses;
          this.totalCourses = courses.length;
          console.log(this.courses);
        } else {
          this.$message.error("获取课程信息或评价信息失败");
        }
      } catch (error) {
        console.error("获取课程信息或评价信息失败:", error);
      }
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
