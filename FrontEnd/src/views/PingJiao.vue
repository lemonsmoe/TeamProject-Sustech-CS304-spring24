<template>
    <div>
      <el-container>
        <el-aside :width="asideWidth">
          <div style="height: 60px; line-height: 60px; font-size: 20px; display: flex; align-items: center; justify-content: center">
            <img src="@/assets/nkd.jpg" style="width: 30px;" alt="">
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
                  <img src="@/assets/nkd.jpg" alt="" style="width: 40px; height: 40px; margin: 0 5px">
                  <span>用户中心</span>
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
            <el-card style=" margin-bottom: 10px" >
                <div slot="header" class="clearfix">
                    <span>预约辅导</span>
                </div>
            </el-card>
  
          </el-main>
        </el-container>
      </el-container>
  
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'LunTan',
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