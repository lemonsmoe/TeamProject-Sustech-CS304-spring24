<template>
  <div style="height: 100vh; display: flex; align-items: center; justify-content: center; background-color: #0f9876">
    <div style="display: flex; background-color: white; width: 50%; border-radius: 5px; overflow: hidden">
      <div style="flex: 1">
        <img src="@/assets/nkd.jpg" alt="" style="width: 100%">
      </div>
      <div style="flex: 1; display: flex; align-items: center; justify-content: center">
        <el-form :model="user" style="width: 80%" :rules="rules" ref="loginRef" @keyup.enter.native="login">
          <div style="font-size: 20px; font-weight: bold; text-align: center; margin-bottom: 20px">欢迎登录使用南科大学术助手</div>
          <el-form-item prop="username">
            <el-input prefix-icon="el-icon-user" size="medium" placeholder="请输入账号" v-model="user.username"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input prefix-icon="el-icon-lock" size="medium" show-password placeholder="请输入密码" v-model="user.password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" style="width: 100%" @click="login">登 录</el-button>
          </el-form-item>
          <div style="display: flex">
            <div style="flex: 1">还没有账号？请 <span style="color: #0f9876; cursor: pointer" @click="$router.push('/register')">注册</span></div>
            <div style="flex: 1; text-align: right"><span style="color: #0f9876; cursor: pointer">忘记密码</span></div>
          </div>
        </el-form>
      </div>
    </div>

  </div>
</template>

<script>
import ValidCode from "@/views/ValidCode";
import axios from "axios";
import request from "@/utils/request";

export default {
  name: "Login",
  components: {
    ValidCode
  },
  data() {
    return {
      user: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
        ],
      }
    }
  },
  created() {

  },
  methods: {
    login() {
      let body = {'student_id': this.user.username, 'password': this.user.password}
      request.post('/general/login', body).then(res=>{
        console.log(res)
        if (res.status === 200) {
          this.$router.push('/')
          this.$message.success(res.data.msg)
        } else {
          this.$message.error(res.data.msg)
        }
      })
    }
  }
}
</script>

<style scoped>

</style>