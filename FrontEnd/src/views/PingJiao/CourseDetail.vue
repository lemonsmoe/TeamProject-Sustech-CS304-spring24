<template>
  <Layout>
    <div class="back_button">
      <el-button type="text" @click="goBack">返回</el-button>
    </div>
    <el-main>
        <el-card class="box-card-evaluation">
  <div slot="header" class="clearfix">
    <span style="font-size: 40px; font-weight: bold"
    >  {{ course.course_name }}</span>
  </div>
  <el-row :gutter="20">
    <el-col :span="12">
      <p>授课类型：{{ course.course_type }}</p>
      <p>开课单位：{{ course.college }}</p>
      
    </el-col>
    <el-col :span="12">
      <p>学分：{{ course.credit }}</p>
      <p>平均评分：{{ avgRating }}</p>
      <p>评价人数：{{ reviewCount }}</p>
    </el-col>
  </el-row>
</el-card>

      <el-card style="margin-bottom: 10px">
        <!-- <div slot="header" class="clearfix">
          <span>课程评价统计</span>
        </div> -->
        <el-row gutter="20">
  <el-col :span="6">
    <div class="stat-item">
      <h3>难度</h3>
      <div class="stat-details">
        简单: {{ courseStats.difficulty.简单 }}<span></span>
        普通: {{ courseStats.difficulty.普通 }}<span></span>
        较难: {{ courseStats.difficulty.较难 }}
      </div>
    </div>
  </el-col>
  <el-col :span="6">
    <div class="stat-item">
      <h3>作业</h3>
      <div class="stat-details">
       少: {{ courseStats.homework.少 }}<span></span>
       适中: {{ courseStats.homework.适中 }}<span></span>
       多: {{ courseStats.homework.多 }}
      </div>
    </div>
  </el-col>
  <el-col :span="6">
    <div class="stat-item">
      <h3>给分</h3>
      <div class="stat-details">
       低: {{ courseStats.grading.低 }}<span></span>
       中: {{ courseStats.grading.中 }}<span></span>
       高: {{ courseStats.grading.高 }}
      </div>
    </div>
  </el-col>
  <el-col :span="6">
    <div class="stat-item">
      <h3>收获</h3>
      <div class="stat-details">
        少: {{ courseStats.harvest.少 }}<span></span>
        中: {{ courseStats.harvest.中 }}<span></span>
        多: {{ courseStats.harvest.多 }}
      </div>
    </div>
  </el-col>
</el-row>
      </el-card>

      

      <el-card style="margin-bottom: 10px">
        <!-- <div slot="header" class="clearfix">
          <span>提交评价</span>
        </div> -->

            <!-- AI-generated-content tool: chatGPT version: 4.o usage: 要求GPT生成各种课程属性的框架结构，属于重复工作 -->
        <div class="quick-reply-section">
          <el-form :model="newReview" class="review-form">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="评分">
                  <el-rate v-model="newReview.rating" allow-half style="margin-top: 10px;"></el-rate>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="难度">
                  <el-select v-model="newReview.difficulty" placeholder="请选择难度">
                    <el-option label="简单" value="简单"></el-option>
                    <el-option label="普通" value="普通"></el-option>
                    <el-option label="较难" value="较难"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="作业">
                  <el-select v-model="newReview.homework" placeholder="请选择作业量">
                    <el-option label="少" value="少"></el-option>
                    <el-option label="适中" value="适中"></el-option>
                    <el-option label="多" value="多"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="给分">
                  <el-select v-model="newReview.grading" placeholder="请选择给分">
                    <el-option label="低" value="低"></el-option>
                    <el-option label="中" value="中"></el-option>
                    <el-option label="高" value="高"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="收获">
                  <el-select v-model="newReview.harvest" placeholder="请选择收获">
                    <el-option label="少" value="少"></el-option>
                    <el-option label="中" value="中"></el-option>
                    <el-option label="多" value="多"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              
              <el-col :span="15">
                <el-form-item label="评论">
                  <el-input type="textarea" v-model="newReview.comment" placeholder="请输入评论" style="margin-left: 40px;"></el-input>
                </el-form-item>
              </el-col>
            <el-col :span="2">
              <el-form-item class="submit-button" style="margin-left: 100px; margin-top:50px">
                <el-button type="primary" @click="submitReview">提交评价</el-button>
              </el-form-item>
            </el-col>
            </el-row>
            
          </el-form>
        </div>
      </el-card>
      <el-card style="margin-bottom: 10px">
        <div slot="header" class="clearfix">
          <span>其他用户点评信息</span>
        </div>
        <div class="comments-section">
          <el-table :data="pagedReviews" style="width: 100%">
            <el-table-column prop="student_id" label="用户名"></el-table-column>
            <el-table-column prop="rating" label="评分"></el-table-column>
            <el-table-column prop="difficulty" label="难度"></el-table-column>
            <el-table-column prop="homework" label="作业"></el-table-column>
            <el-table-column prop="grading" label="给分"></el-table-column>
            <el-table-column prop="harvest" label="收获"></el-table-column>
            <el-table-column prop="comment" label="评论"></el-table-column>
          </el-table>
          <el-pagination
            style="margin-top: 20px;"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-size="pageSize"
            layout="total, prev, pager, next"
            :total="totalReviews">
          </el-pagination>
        </div>
      </el-card>
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
      course: {
        title: '马克思主义基本原理',
        category: '计划',
        type: '理论课',
        method: '本科计划内课程',
        unit: '马克思主义学院',
        credit: 2.5
      },
      avgRating: 0,
      reviewCount: 0,
      courseStats: [],
      form: {
        sort: '',
        semester: '',
        rating: ''
      },
      reviews: [],
      newReview: {
        course_id: this.$route.params.id,
        rating: null,
        difficulty: '',
        homework: '',
        grading: '',
        harvest: '',
        comment: ''
      },
      currentPage: 1,
      pageSize: 5,
      totalReviews: 0
    };
  },
  computed: {
    pagedReviews() {
      return this.reviews.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize);
    }
  },
  mounted() {
    this.fetchCourseInfo();
    this.fetchCourseStats();
    this.fetchCourseReviews();
  },
  methods: {
    handleCollapse() {
      console.log('Toggle sidebar');
    },
    handleFullScreen() {
      console.log('Toggle full screen');
    },
    goBack() {
      this.$router.go(-1);  // 返回前一个页面
    },
    handleCurrentChange(page) {
      this.currentPage = page;
      // this.fetchCourseReviews(); // Fetch new page data
    },
    fetchCourseInfo() {
      request.get(`/evaluation/course/${this.$route.params.id}`)
        .then(res => {
          if (res.status === 200) {
            this.course = res.data;
            this.fetchCourseReviewBrief(); // 获取课程的平均评分和评价人数
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(error => {
          console.error("获取课程信息失败:", error);
        });
    },
    fetchCourseReviewBrief() {
      request.get(`/evaluation/review/getbrief`)
        .then(res => {
          if (res.status === 200) {
            const review = res.data.find(r => r.course_id === this.$route.params.id);
            if (review) {
              this.avgRating = review.avg_rating;
              this.reviewCount = review.review_count;
            }
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(error => {
          console.error("获取课程评价信息失败:", error);
        });
    },
    fetchCourseReviews() {
      request.get(`/evaluation/review/getall/${this.$route.params.id}`)
        .then(res => {
          if (res.status === 200) {
            console.log(res.data);
            this.reviews = res.data;
            this.totalReviews = res.data.length;
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(error => {
          console.error("获取课程评价失败:", error);
        });
    },

    // <!-- AI-generated-content tool: chatGPT version: 4.o usage: 要求GPT生成各种获取课程评教统计信息 -->
    fetchCourseStats() {
      request.get(`/evaluation/review/stats/${this.$route.params.id}`)
        .then(res => {
          if (res.status === 200) {
            this.courseStats = res.data;
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(error => {
          console.error("获取课程评价统计失败:", error);
        });
    },

    submitReview() {
      if (!this.newReview.rating  || !this.newReview.difficulty || !this.newReview.homework || !this.newReview.grading || !this.newReview.harvest || !this.newReview.comment) {
        this.$message.error('请填写完整信息');
        return;
      }
      request.post('/evaluation/review/put', this.newReview)
        .then(res => {
          if (res.status === 200) {
            this.$message.success('评价发布成功');
            // 清空表单
            this.newReview = {
              course_id: this.$route.params.id,
              rating: null,
              difficulty: '',
              homework: '',
              grading: '',
              harvest: '',
              comment: ''
            };
            this.fetchCourseReviews(); // 刷新评价列表
            this.fetchCourseStats(); // 刷新统计数据
          } else {
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.error("发布评价失败:", error);
        });
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
.review-attribute {
  margin-right: 20px; /* 控制属性之间的间距 */
  flex: 1; /* 让每个属性平分容器宽度 */
}
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
.stat-item {
  margin-bottom: 20px;
}
.stat-details {
  /* display: flex; */
  justify-content: space-between;
}
</style>
