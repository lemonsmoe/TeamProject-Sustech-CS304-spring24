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
            
            <el-submenu index="2">
              <template slot="title"><i class="el-icon-menu"></i><span>学生应用</span></template>
              <el-menu-item index="/xuanke">选课规划</el-menu-item>
              <el-menu-item index="/luntan">学习论坛</el-menu-item>
              <el-menu-item index="/fudao">预约辅导</el-menu-item>
              <el-menu-item index="/rili">学习日历</el-menu-item>
              <el-menu-item index="/pingjiao">评教系统</el-menu-item>
              <el-menu-item index="/guanli" v-if="isAdmin()">管理员</el-menu-item>
            </el-submenu>
          </el-menu>
        </el-aside>
  
        <el-container>
          <el-header style="height: 60px; line-height: 60px; display: flex; align-items: center; box-shadow: 2px 0 6px rgba(0, 21, 41, .35);">
            <i :class="collapseIcon" @click="handleCollapse" style="font-size: 26px"></i>
            <div style="flex: 1; display: flex; justify-content: flex-end; align-items: center">
              <i class="el-icon-quanping" @click="handleFullScreen" style="font-size: 25px"></i>
              <span>{{'欢迎，' + current_student_id + '   你是：' + current_type}}</span>
              <el-dropdown placement="bottom">
                
                <div style="display: flex; align-items: center; cursor: pointer">
                  
                  <img src="@/assets/nkd.jpg" alt="" style="width: 40px; height: 40px; margin: 0 5px">
                  <span>用户中心</span>
                </div>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item @click.native="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </el-header>
          <!-- <div :style="{ backgroundImage: `url(${require('@/assets/cover.png')})`}"> -->
            <slot>
              <!-- 插槽用于装载不同模块的主要内容 -->
            </slot>
            <!-- <img src="@/assets/cover.png" alt="OpenZS Logo" style="width: 100%; height: auto"> -->
          <!-- </div> -->
        </el-container>
      </el-container>
  
    </div>
  </template>
  
  <script>
  import request from "@/utils/request";
  export default {
    name: 'Layout',
    data() {
      return {
        isCollapse: false,
        asideWidth: '200px',
        collapseIcon: 'el-icon-s-fold',
        current_student_id: '',
        current_type: '',

      }
    },
    mounted() {
  
    },
    async created() {
    // 在组件创建后立即发送请求
      await this.getUser();
    },
    methods: {
      isAdmin() {
        return this.current_student_id === 'admin';
      },
      getUser() {
        // 获取当前用户信息
        request.get('/general/current_student').then(res=>{
          console.log(res);
          if (res.status == 200) {
            this.current_student_id = res.data.student_id;
            if (this.current_student_id === 'admin') {
              this.current_type = '管理员';
            }
            else {
              this.current_type = '学生';
            }
            
          }
          else{
            this.$router.push('/login');
          }
          
        })
      },
      handleLogout() {
        // 在这里添加退出登录的逻辑
        console.log('正在退出登录...');
        // 清除用户信息
        // localStorage.removeItem('user');
        request.get('/general/logout').then(res=>{
          console.log(res)
        })
        // 跳转到登录页面
        this.$router.push('/login');
      },
      handleFullScreen() {
        document.documentElement.requestFullscreen()
      },
      handleCollapse() {
        this.isCollapse = !this.isCollapse
        this.asideWidth = this.isCollapse ? '64px' : '200px'
        this.collapseIcon = this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
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