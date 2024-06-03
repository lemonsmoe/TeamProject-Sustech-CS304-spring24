<template>
  <div class="flex h-screen bg-gray-200 dark:bg-black">
    <div class="m-auto w-full max-w-sm">
      <el-card class="shadow-xl">
        <div slot="header" class="text-center">南科大学术助手</div>
        <div class="el-card__body">
          <form class="space-y-6">
            <div>
              <div class="flex items-center border-b border-gray-300 pb-2">
                <i class="el-icon-user ml-2"></i>
                <el-input class="ml-2 flex-1 border-none bg-transparent px-4 py-2 focus:ring-0"
                          placeholder="用户名"></el-input>
              </div>
            </div>
            <div>
              <div class="flex items-center border-b border-gray-300 pb-2">
                <i class="el-icon-lock ml-2"></i>
                <el-input class="ml-2 flex-1 border-none bg-transparent px-4 py-2 focus:ring-0"
                          type="password" placeholder="密码"></el-input>
              </div>
            </div>
            <el-button class="w-full py-3">登录</el-button>
          </form>
        </div>
        <div class="flex justify-between px-6 pt-4 pb-6 text-sm text-gray-600">
          <a href="#" class="hover:text-blue-600 dark:text-gray-400 dark:hover:text-white">忘记密码？</a>
          <a href="#" class="hover:text-blue-600 dark:text-gray-400 dark:hover:text-white">注册新用户</a>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  components: {
    'el-card': require('element-ui/lib/card').default,
    'el-input': require('element-ui/lib/input').default,
    'el-button': require('element-ui/lib/button').default
  }
}
</script>
