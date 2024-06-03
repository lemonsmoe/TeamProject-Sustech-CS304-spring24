
<template  >
      <el-card style=" margin-bottom: 10px" >
        <transition name="fade">
          <div v-if="isLoading" class="loading-indicator">彭小僧小姐姐已经用力了 {{ elapsedTime }} 秒...</div>
        </transition>
        
        <div>
          <el-form :inline="true" :model="formInline" class="demo-form-inline"  @keyup.enter.native="onSubmit">
            <el-alert
          title="本功能专注为你排布课程的时间，请先到TIS查找你需要修读的课，再来排课哦。"
          type="info"
          show-icon>
        </el-alert>
            <el-form-item label="开课学期">
              <el-select v-model="formInline.xueqi" placeholder="请选择开课学期">
                <el-option label="2024春" value="shanghai"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="必选课">
              <el-input v-model="formInline.keywords" placeholder="空格分隔关键词"></el-input>
            </el-form-item>
            
            <el-form-item label="必躲课">
              <el-input v-model="formInline.badwords" placeholder="空格分隔关键词"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">查询</el-button>
            </el-form-item>
            <el-form-item>
              <el-button
                size="mini"
                :type="this.allow_modify ? 'success' : 'warning'"
                @click="toggleModifyPermission">
                {{ this.allow_modify ? '允许选择开摆' : '不允许选择开摆' }}
              </el-button>
            </el-form-item>
            
          </el-form>
        </div>
        <div style="margin: 10px; " >
          <el-table
              :data="tableData"
              border
              style="width: 100%;   border-radius: 10px;"
              :align="'center'"
              @cell-click="handleCellClick"
              >

            <el-table-column
              v-for="(column, index) in columns"
              :key="index"
              :prop="column.prop"
              :label="column.label"
              align="center"
            >
            <template v-slot="scope">
               <div :style="{ backgroundColor: getColor(scope.row[column.prop]), display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold'  }"  style="height: 70px; text-align: center;  border-radius: 10px;">
              {{ scope.row[column.prop] }}
               </div>
              </template>
            </el-table-column>
          </el-table>

          <div style="margin: 20px"  >
            <el-row >
              <el-button type="primary" @click="previous">上一页</el-button>
              <!-- /* 显示当前页数 index+1/total */ -->
              <el-button @keydown.left.native="previous" @keydown.right.native="next" tabindex="0">{{ index+1 }}/{{ total }}</el-button>
              
              <el-button type="primary" @click="next">下一页</el-button>
              <el-button type="primary" @click="star">收藏</el-button>
            </el-row>
          </div>
        </div>
      </el-card>

</template>

<script>
import Layout from '@/components/Layout.vue'
import request from "@/utils/request";
export default {
  name: 'XuanKe',
  components: {
      Layout,
  },
  data() {
  return {
    allow_modify: true,
    noClassTimes: [],
    columns: [
        { prop: '0', label: ' ' },
        { prop: '1', label: '周一' },
        { prop: '2', label: '周二' },
        { prop: '3', label: '周三' },
        { prop: '4', label: '周四' },
        { prop: '5', label: '周五' },
        { prop: '6', label: '周六' },
        { prop: '7', label: '周日' },
      ],

    isCollapse: false,
    asideWidth: '200px',
    collapseIcon: 'el-icon-s-fold',
    form: {
      name: '',
      region: '',
      date1: '',
      date2: '',
      delivery: false,
      type: [],
      resource: '',
      desc: ''
    },
    formInline: {
      xueqi: '2024春',
      keywords: '',
      badwords: '',
      yuanxi: ''
    },

    days: ['', '周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    /**
     * AI-generated-content
     * tool: Copilot
     * version: latest
     * usage: 询问如何以简洁的代码生成表格
    */
    tableData: Array(6).fill().map((_, i) => ({
      0: `第${i + 1}节`,
      1: '',
      2: '',
      3: '',
      4: '',
      5: '',
      6: '',
      7: '',
    })), 
    index: 0,
    total: 0,
    scheme: {},
    noclasslabel: '必须开摆',
    all_color: [
     '#CCFF99', '#CCCCFF', '#FF99CC', '#99CCFF', '#CCFFFF', '#FFFFCC',
    '#f3ad45', '#b5f851', '#49b1f6', '#ef42a8', '#FFE5CC', '#CCE5FF', '#abfd59', '#45f19b'
],
    courseNameMap: {
      },
      isLoading: false,
      loadingStartTime: null,
    elapsedTime: 0,
  }
},
mounted() {
},
beforeDestroy() {
  },
computed:{
},
methods: {
  toggleModifyPermission() {
    this.allow_modify = !this.allow_modify;
  },
  handleCellClick(row, column, cell, event) {
    if (!this.allow_modify) {
      return;
    }
    console.log(row, column, cell, event)
    console.log(row['0'], column.property)
    // 转成int
    let r = parseInt(row['0'].split('第')[1].split('节')[0]) - 1
    let c = parseInt(column.property)
    if (c == 0) {
      return
    }
    if (this.tableData[r][c] == this.noclasslabel) {
      this.tableData[r][c] = ''
      return
    }
    this.tableData[r][c] = this.noclasslabel
  },
  getColor(courseName) {
    if (courseName == this.noclasslabel) {
      return 'rgba(247, 165, 165, 0.84)'
    }
    return this.courseNameMap[courseName] || '#ffffff'; // 默认颜色为白色
  },
  getCellClassName({ row, column, rowIndex, columnIndex }) {
    if (columnIndex === 0) {
      return '';
    }
    console.log(row[column.property])
    console.log(this.courseNameMap[row[column.property]])
    return this.courseNameMap[row[column.property]]
  },
  handleFullScreen() {
    document.documentElement.requestFullscreen()
  },
  handleCollapse() {
    this.isCollapse = !this.isCollapse
    this.asideWidth = this.isCollapse ? '64px' : '200px'
    this.collapseIcon = this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
  },
  onSubmit() {
    const loading = this.$loading({
        lock: true,
        text: '啊啊啊啊啊啊，人家真的在用力获取你的规划了啦...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.1)'
      });
    let obj = {
      'password': 'my father is YHT', 'student_name': '', 'keywords': this.formInline.keywords.split(' '), 'badwords': this.formInline.badwords.split(' '), 'excluded_time': {'点': []}
    }
    //'excluded_time': {'点': [[2, 1], [3, 1], [4, 1]]}, 根据tableData来指定
    for (let i = 0; i <= 5; i++) {
      for (let j = 1; j <= 7; j++) {
        if (this.tableData[i][j] == this.noclasslabel) {
          obj['excluded_time']['点'].push([j, i+1])
        }
      }
    }
    console.log(obj)
    this.isLoading = true;
    this.loadingStartTime = Date.now();
    this.timer = setInterval(() => {
      this.elapsedTime = Math.floor((Date.now() - this.loadingStartTime) / 1000);
    }, 1000);

    request.post('courserc/submit_data', obj).then(res=>{
      this.scheme = res.data.schedule_scheme
      this.total = Object.keys(this.scheme).length;
      // console.log(this.scheme)
      
      // this.$message.success('主人主人，彭小僧已经为你找到了符合你心意的规划啦！');
      this.$message({
        message: '主人主人，彭小僧已经为你找到了符合你心意的规划啦！',
        type: 'success',
        duration: 8000
      });
      this.allow_modify = false;
      this.isLoading = false;
      clearInterval(this.timer);
      loading.close();
      this.index = 0;
      this.show(this.scheme[this.index])
    }).catch(err=>{
      console.log(err)
      this.$message({
        message: '彭小僧真的找不到符合你心意的规划啦，求抱抱，啾咪啾啾咪',
        type: 'error',
        duration: 8000
      });
      this.isLoading = false;
      clearInterval(this.timer);
      loading.close();
    })
  },

  show(obj) {
    this.clear()
    this.courseNameMap = {}
    let credit = 0

    for (let i = 0; i < obj.length; i++) {
      credit += parseFloat(obj[i]['学分'])
      this.courseNameMap[obj[i]['教学班']] = this.all_color[i]

      let date1 = obj[i]['上课时间'][0][1]
      let time1 = obj[i]['上课时间'][0][0]

      let classname = obj[i]['教学班']

      this.tableData[date1-1][time1] = classname

      if (obj[i]['上课时间'].length == 1) {
        continue
      }

      let date2 = obj[i]['上课时间'][1][1]
      let time2 = obj[i]['上课时间'][1][0]

      this.tableData[date2-1][time2] = classname
    }
    this.tableData[5][7] = `总学分: ${credit}`
  },
  next() {
    if (this.index >= this.total - 1) {
      return
    }
    this.index = this.index + 1
    this.show(this.scheme[this.index])
  },
  previous() {
    if (this.index == 0) {
      return
    }
    this.index = this.index - 1
    this.show(this.scheme[this.index])
  },
  star() {
    request.post('courserc/star/put', {
      "schedule": this.scheme[this.index]
    }).then(res=>{
      if (res.status == 200) {
        this.$message({
          message: '主人主人，彭小僧已经为你收藏了这个规划啦！',
          type: 'success',
          duration: 8000
        });
      }
  else {
    this.$message({
      message: '主人主人，已经收藏过啦！别逗彭小僧啦！',
      type: 'error',
      duration: 8000
    });
  }
}).catch(err=>{
  console.log(err)
  this.$message({
    message: '彭小僧被玩坏了啦',
    type: 'error',
    duration: 8000
  });
})
  },
  clear() {
    for (let i = 0; i <= 5; i++) {
      for (let j = 1; j <= 7; j++) {
        if (this.tableData[i][j]==this.noclasslabel)
        {
          continue
        }
        this.tableData[i][j] = ''
      }
    }
  }
}
}
</script>

<style>
.el-table .el-table__row {
  height: 80px !important;
}

.el-table .el-table__body-wrapper {
  overflow: hidden;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

</style>
