<template>
    <div class="forum-container">
      <!-- 发帖表单 -->
      <div class="post-form">
        <h2>发表新帖子</h2>
        <form>
          <div>
            <label for="post-title">标题:</label>
            <input type="text" id="post-title" name="title">
          </div>
          <div>
            <label for="post-content">内容:</label>
            <textarea id="post-content" name="content"></textarea>
          </div>
          <button type="submit">发布</button>
        </form>
      </div>
  
      <!-- 帖子列表 -->
      <div class="posts-list">
        <h2>帖子列表</h2>
        <!-- <div class="post" v-for="post in posts" :key="post.id">
          <h3>{{ post.title }}</h3>
          <p>{{ post.content }}</p>
        </div> -->
      </div>
    </div>
  </template>
  
  <style scoped>
    .forum-container {
      width: 80%;
      margin: auto;
    }
    .post-form {
      margin-bottom: 20px;
    }
    .post-form form div {
      margin-bottom: 10px;
    }
    .post-form label {
      margin-right: 10px;
    }
    .post-form input[type="text"],
    .post-form textarea {
      width: 100%;
    }
    .posts-list .post {
      background-color: #f4f4f4;
      border: 1px solid #ccc;
      padding: 10px;
      margin-top: 10px;
    }
  </style>
  