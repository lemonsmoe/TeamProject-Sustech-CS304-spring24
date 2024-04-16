# CS304 软件工程 项目中期报告

小组成员：彭彦兮、杨浩庭、彭子燊、胡清畅



## 第一部分：架构及UI设计

#### 架构设计

##### 设计图

<img src="markdown_img/report.assets/d2fabae91135d8e574044aa41a8bc6c.png" alt="d2fabae91135d8e574044aa41a8bc6c" style="zoom:60%;" />

<img src="markdown_img/report.assets/7809e70e200b47bebe44d4c8594f241.png" alt="7809e70e200b47bebe44d4c8594f241" style="zoom:60%;" />

<img src="markdown_img/report.assets/0c214166a548ea4545a5ddd84f969dd.png" alt="0c214166a548ea4545a5ddd84f969dd" style="zoom:60%;" />

<img src="markdown_img/report.assets/3c00b033108d60690c091189f8ee87c.png" alt="3c00b033108d60690c091189f8ee87c" style="zoom:60%;" />

<img src="markdown_img/report.assets/f6fa9f1cbc28a864f496024009a4382.png" alt="f6fa9f1cbc28a864f496024009a4382" style="zoom:60%;" />

##### 解释说明

​	采用了Data-Centered Architecture 以数据为中心的架构，因为我们设计的功能本质上都是数据的查看和修改，都是基于数据库上的改动。其中多个数据库信息为了展示方便，将其按照五个不同的功能进行了划分。

​	中间的组件为central data，负责提供各组件和功能之间互相交换修改信息的数据存储库；周围的组件为data accessor，可以是个体（比如用户），也可以是独立组件的集合（抽象成一个功能）。

​	双向箭头表示对数据库既有存储又有读取操作，由数据库指向data accessor表示外部组件只对数据库有读取操作，而不修改数据库内容。

​	

#### UI设计

###### 主页面设计：

![New Wireframe 1](markdown_img/report.assets/New%20Wireframe%201.png)

###### 个人信息页面：

![New Wireframe 2](markdown_img/report.assets/New%20Wireframe%202.png)

###### 选课助手主界面：

###### ![image-20240416021514820](markdown_img/report.assets/image-20240416021514820.png)



###### 学习论坛主页面：

![New Wireframe 1 (1)](markdown_img/report.assets/New%20Wireframe%201%20(1).png)

###### 学习论坛帖子详细内容：

![New Wireframe 1 (2)](markdown_img/report.assets/New%20Wireframe%201%20(2).png)

###### 辅导咨询主页面+预约界面：

![New Wireframe 1 (3)](markdown_img/report.assets/New%20Wireframe%201%20(3).png)

###### 辅导咨询信息填写界面：

![New Wireframe 1 (4)](markdown_img/report.assets/New%20Wireframe%201%20(4).png)

###### 学习日历/日历设置：

![New Wireframe 1 (5)](markdown_img/report.assets/New%20Wireframe%201%20(5).png)

###### 学习日历/学术信息活动：

![New Wireframe 1 (6)](markdown_img/report.assets/New%20Wireframe%201%20(6).png)

###### 课程反馈/课程详细信息：

![New Wireframe 1 (7)](markdown_img/report.assets/New%20Wireframe%201%20(7).png)

###### 课程反馈/学生点评信息：

![New Wireframe 1 (8)](markdown_img/report.assets/New%20Wireframe%201%20(8).png)