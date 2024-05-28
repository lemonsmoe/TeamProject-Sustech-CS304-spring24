<!-- Home.vue -->
<template>
    <Layout>

        <el-main>
            <el-card style=" margin-bottom: 10px" >
              <div slot="header" class="clearfix">
                <span>学生选课推荐系统</span>
              </div>
              <div style="margin: 10px">
                <el-form :inline="true" :model="formInline" class="demo-form-inline">
                  <el-form-item label="开课学期">
                    <el-select v-model="formInline.xueqi" placeholder="请选择开课学期">
                      <el-option label="2024春" value="shanghai"></el-option>
                      <el-option label="2023秋" value="beijing"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="课程名称">
                    <el-input v-model="formInline.mingcheng" placeholder="课程名称"></el-input>
                  </el-form-item>
                  <el-form-item label="开课院系">
                    <el-select v-model="formInline.yuanxi" placeholder="开课院系">
                      <el-option label="体育中心" value="shanghai"></el-option>
                      <el-option label="艺术中心" value="beijing"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="onSubmit">查询</el-button>
                  </el-form-item>
                </el-form>
              </div>
              <div style="margin: 10px">
                <el-table
                    :data="tableData"
                    border
                    style="width: 100%"
                    :align="'center'">
                  <el-table-column
                      prop="0"
                      label=" "
                      :align="'center'">
                  </el-table-column>
                  <el-table-column
                      prop="1"
                      label="周一"
                      :align="'center'">
                  </el-table-column>
                  <el-table-column
                      prop="2"
                      label="周二"
                      :align="'center'">
                  </el-table-column>
                  <el-table-column
                      prop="3"
                      label="周三"
                      :align="'center'">
                  </el-table-column>
                  <el-table-column
                      prop="4"
                      label="周四"
                      :align="'center'">
                  </el-table-column>
                  <el-table-column
                      prop="5"
                      label="周五"
                      :align="'center'">
                  </el-table-column>
                  <el-table-column
                      prop="6"
                      label="周六"
                      :align="'center'">
                  </el-table-column>
                  <el-table-column
                      prop="7"
                      label="周日"
                      :align="'center'">
                  </el-table-column>
                </el-table>
  
                <div style="margin: 20px">
                  <el-row>
                    <el-button type="primary" @click="previous">上一页</el-button>
                    <el-button type="primary" @click="next">下一页</el-button>
                  </el-row>
                </div>
              </div>
            </el-card>
  
          </el-main>
    </Layout>
  </template>

<script>
import Layout from '@/components/Layout.vue'
export default {
    name: 'thomastest',
    components: {
        Layout
    },
    data() {
    return {

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
        xueqi: '',
        mingcheng: '',
        yuanxi: ''
      },
      tableData: [{
        0: '第一节',
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: '',
      }, {
        0: '第二节',
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: '',
      }, {
        0: '第三节',
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: '',
      }, {
        0: '第四节',
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: '',
      }, {
        0: '第五节',
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: '',
      }, {
        0: '第六节',
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: '',
        7: '',
      }],
      index: 0,
      scheme: {},
    }
  },
  mounted() {

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
    onSubmit() {
      let obj = []
      obj = this.formInline.mingcheng.split(' ')
      console.log(obj)
      this.axios.post('http://localhost:1314/submit_data', {
        'password': 'my father is YHT', 'student_name': '', 'keywords': obj, 'badwords': [''], 'excluded_time': {'点': []}
      }).then(res=>{

        this.scheme = res.data.schedule_scheme
        // console.log(this.scheme)
        this.show(this.index)

      })
    },

    show(index) {
      if (index < 0) {
        index += 1
      }
      if (index >= this.scheme.length){
        index -= 1
      }
      let obj = this.scheme[index]
      for (let i = 0; i < obj.length; i++) {

        let date1 = obj[i]['上课时间'][0][1]
        let time1 = obj[i]['上课时间'][0][0]

        let date2 = obj[i]['上课时间'][1][1]
        let time2 = obj[i]['上课时间'][1][0]

        let classname = obj[i]['教学班']

        this.tableData[date1-1][time1] = classname
        this.tableData[date2-1][time2] = classname

        this.index = index
        // 组成 原理
      }
    },
    next() {
      this.clear()
      this.show(this.index+1)
    },
    previous() {
      this.clear()
      this.show(this.index-1)
    },
    clear() {
      for (let i = 0; i <= 5; i++) {
        for (let j = 1; j <= 7; j++) {
          this.tableData[i][j] = ''
        }
      }
    }
  }
}
</script>
