<template>
  <div>
    <el-container>
      <el-aside :width="asideWidth">
        <div style="height: 60px; line-height: 60px; font-size: 20px; display: flex; align-items: center; justify-content: center">
          <img src="@/assets/logo.png" style="width: 30px;" alt="">
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
<!--          <div style="box-shadow: 0 0 10px rgba(0,0,0,.1); padding: 10px 20px; border-radius: 5px; margin-bottom: 10px">-->
<!--            简介-->
<!--          </div>-->
          <el-card style=" margin-bottom: 10px" >
            <div slot="header" class="clearfix">
              <span>学生选课系统</span>
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
                  style="width: 100%">
                <el-table-column
                    prop="0"
                    label=" ">
                </el-table-column>
                <el-table-column
                    prop="1"
                    label="周一">
                </el-table-column>
                <el-table-column
                    prop="2"
                    label="周二">
                </el-table-column>
                <el-table-column
                    prop="3"
                    label="周三">
                </el-table-column>
                <el-table-column
                    prop="4"
                    label="周四">
                </el-table-column>
                <el-table-column
                    prop="5"
                    label="周五">
                </el-table-column>
                <el-table-column
                    prop="6"
                    label="周六">
                </el-table-column>
                <el-table-column
                    prop="7"
                    label="周日">
                </el-table-column>
              </el-table>
            </div>
            <div style="margin: 20px">
              <el-pagination
                  background
                  layout="prev, pager, next"
                  :total="1000">
              </el-pagination>
            </div>
          </el-card>

<!--          <el-card style="width: 800px">-->

<!--            <div slot="header" class="clearfix">-->
<!--              <span>小标题</span>-->
<!--            </div>-->
<!--            -->
<!--            <div>-->
<!--              <el-form ref="form" :model="form" label-width="80px">-->
<!--                <el-form-item label="活动名称">-->
<!--                  <el-input v-model="form.name"></el-input>-->
<!--                </el-form-item>-->
<!--                <el-form-item label="活动区域">-->
<!--                  <el-select v-model="form.region" placeholder="请选择活动区域">-->
<!--                    <el-option label="区域一" value="shanghai"></el-option>-->
<!--                    <el-option label="区域二" value="beijing"></el-option>-->
<!--                  </el-select>-->
<!--                </el-form-item>-->
<!--                <el-form-item label="活动时间">-->
<!--                  <el-col :span="11">-->
<!--                    <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 100%;"></el-date-picker>-->
<!--                  </el-col>-->
<!--                  <el-col class="line" :span="2">-</el-col>-->
<!--                  <el-col :span="11">-->
<!--                    <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 100%;"></el-time-picker>-->
<!--                  </el-col>-->
<!--                </el-form-item>-->
<!--                <el-form-item label="即时配送">-->
<!--                  <el-switch v-model="form.delivery"></el-switch>-->
<!--                </el-form-item>-->
<!--                <el-form-item label="活动性质">-->
<!--                  <el-checkbox-group v-model="form.type">-->
<!--                    <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>-->
<!--                    <el-checkbox label="地推活动" name="type"></el-checkbox>-->
<!--                    <el-checkbox label="线下主题活动" name="type"></el-checkbox>-->
<!--                    <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>-->
<!--                  </el-checkbox-group>-->
<!--                </el-form-item>-->
<!--                <el-form-item label="特殊资源">-->
<!--                  <el-radio-group v-model="form.resource">-->
<!--                    <el-radio label="线上品牌商赞助"></el-radio>-->
<!--                    <el-radio label="线下场地免费"></el-radio>-->
<!--                  </el-radio-group>-->
<!--                </el-form-item>-->
<!--                <el-form-item label="活动形式">-->
<!--                  <el-input type="textarea" v-model="form.desc"></el-input>-->
<!--                </el-form-item>-->
<!--                <el-form-item>-->
<!--                  <el-button type="primary" @click="onSubmit">立即创建</el-button>-->
<!--                  <el-button>取消</el-button>-->
<!--                </el-form-item>-->
<!--              </el-form>-->
<!--            </div>-->
<!--          </el-card>-->
          <!--          <el-table stripe :header-cell-style="{ backgroundColor: 'aliceblue', fontWeight: 'bold', color: '#333' }">-->
          <!--            <el-table-column label="姓名" align="center"></el-table-column>-->
          <!--            <el-table-column label="电话" align="center"></el-table-column>-->
          <!--            <el-table-column label="邮箱" align="center"></el-table-column>-->
          <!--            <el-table-column label="地址" align="center"></el-table-column>-->
          <!--          </el-table>-->
        </el-main>
      </el-container>
    </el-container>

  </div>
</template>

<script>

export default {
  name: 'xuanke',
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
        3: '高等数学（上）',
        4: '',
        5: 'EAP',
        6: '',
        7: '',
      }, {
        0: '第二节',
        1: '',
        2: '大学物理（上）',
        3: '',
        4: '',
        5: 'EAP',
        6: '',
        7: '',
      }, {
        0: '第三节',
        1: '',
        2: '大学物理（上）',
        3: '高等数学（上）',
        4: '',
        5: '',
        6: '',
        7: '',
      }, {
        0: '第四节',
        1: '',
        2: '大学物理（上）',
        3: '',
        4: '',
        5: 'EAP',
        6: '',
        7: '',
      }, {
        0: '第五节',
        1: '',
        2: '',
        3: '高等数学（上）',
        4: '',
        5: 'EAP',
        6: '',
        7: '',
      }, {
        0: '第六节',
        1: '',
        2: '大学物理（上）',
        3: '高等数学（上）',
        4: '',
        5: 'EAP',
        6: '',
        7: '',
      }, {
        0: '第七节',
        1: '',
        2: '大学物理（上）',
        3: '高等数学（上）',
        4: '',
        5: 'EAP',
        6: '',
        7: '',
      },
      ]
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
        console.log(res)
        console.log(res.data.schedule_scheme[0])
        let obj = res.data.schedule_scheme[0]
        for (let i = 0; i < obj.length; i++) {
          console.log(obj[i])
          console.log(obj[i]['上课时间'])
          console.log(obj[i]['教学班'])
        }
        localStorage.setItem('list',res.data.schedule_scheme)
      })
    },
    change() {

      this.tableData[0][1] = '大学化学'
      this.tableData[0][2] = '大学生物'
      console.log(this.tableData[0])
      console.log(this.tableData[0][1])
      console.log(this.tableData[1][2])

    }
  }
}
</script>

<style>
.el-menu--inline, .el-menu-item {
  background-color: #000c17 !important;
}

.el-submenu__title {
  height: 40px !important;
  line-height: 40px !important;
  padding: 0 25px !important;
  transition: color 0s;
}
.el-menu--collapse .el-submenu__title {
  padding: 0 20px !important;
}
.el-submenu__title>i:nth-child(1) {
  margin-top: 2px;
}
.el-submenu__title>i.el-submenu__icon-arrow {
  margin-top: -5px;
}
.el-menu-item {
  min-width: 0 !important;
  width: calc(100% - 10px);
  margin: 5px;
  height: 40px !important;
  line-height: 40px !important;
  border-radius: 5px;
}
.el-menu--inline>.el-menu-item {
  padding-left: 50px !important;
}
.el-menu-item.is-active {
  background-color: dodgerblue !important;
}

.el-menu-item:hover {
  color: #fff !important;
}

.el-submenu__title:hover *, .el-submenu__title:hover {
  color: #fff !important;
}

.el-aside {
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
  background-color: #001529;
  color: #fff;
  min-height: 100vh;
  transition: width .3s;
}
.el-menu--collapse .el-tooltip {
  padding: 0 15px !important;
}
.logo-title {
  margin-left: 5px;
  transition: all .3s;
}
.el-menu {
  transition: all .3s;
}
</style>