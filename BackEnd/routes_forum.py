from flask import jsonify, request, session, Blueprint
from datetime import datetime
from models_wholeProject import app, db, fk_command, Post, Reply, PostContent, CourseReview
from sqlalchemy import inspect

app_forum = Blueprint('app_forum', __name__, url_prefix='/forum')

@app_forum.route('/post/get', methods = ['GET'])
def get_all_post():
    """
获取所有帖子信息
---
tags:
  - Forum
responses:
  200:
    description: 成功获取所有帖子信息
    schema:
      type: array
      items:
        type: object
        properties:
          post_id:
            type: integer
            description: 帖子ID
          title:
            type: string
            description: 帖子标题
          content:
            type: string
            description: 帖子内容
          created_time:
            type: string
            description: 帖子创建时间（格式：YYYY-MM-DD HH:MM:SS）
          last_updated_time:
            type: string
            description: 帖子最后更新时间（格式：YYYY-MM-DD HH:MM:SS）
          view_count:
            type: integer
            description: 帖子浏览数
          reply_count:
            type: integer
            description: 帖子回复数
          ReplyAndViewCount:
            type: string
            description: 回复数/浏览数
  404:
    description: 未找到帖子信息
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 未找到帖子信息
"""

    posts = Post.query.filter_by(used=True).all()
    data = [dict((c, getattr(post, c)) for c in inspect(post).mapper.column_attrs.keys()) for post in posts]
    # 查询reply_count
    data = [dict(post, reply_count=len(Reply.query.filter_by(post_id=post["post_id"]).all())) for post in data]
    # 修改时间格式
    for post in data:
        post["created_time"] = post["created_time"].strftime("%Y-%m-%d %H:%M:%S")
        post["last_updated_time"] = post["last_updated_time"].strftime("%Y-%m-%d %H:%M:%S")
        post['ReplyAndViewCount'] = f"{post['reply_count']}/{post['view_count']}"
    return jsonify(data)

@app_forum.route('/post/getcontent', methods = ['POST'])
def get_post_content():
    """
获取帖子内容
---
tags:
  - Forum
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        post_id:
          type: integer
          description: 帖子ID
responses:
  200:
    description: 成功获取帖子内容
    schema:
      type: object
      properties:
        title:
          type: string
          description: 帖子标题
        content:
          type: string
          description: 帖子内容
        board:
          type: string
          description: 论坛板块
        topic:
          type: string
          description: 帖子主题
        created_time:
          type: string
          description: 帖子创建时间（格式：YYYY-MM-DD HH:MM:SS）
        last_updated_time:
          type: string
          description: 帖子最后更新时间（格式：YYYY-MM-DD HH:MM:SS）
        author:
          type: string
          description: 帖子作者ID
  404:
    description: 帖子不存在或内容不存在
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 帖子不存在或内容不存在
"""

    req_data = request.get_json()
    post = Post.query.filter_by(post_id=req_data["post_id"], used=True).first()
    if post is None:
        return jsonify(msg="帖子不存在"), 404

    post_content = PostContent.query.filter_by(post_id=req_data["post_id"]).first()
    if post_content is None:
        return jsonify(msg="帖子内容不存在"), 404

    data = {
        "title": post.title,
        "content": post_content.content,
        "board": post.board,
        "topic": post.topic,
        "created_time": post.created_time.strftime("%Y-%m-%d %H:%M:%S"),
        "last_updated_time": post.last_updated_time.strftime("%Y-%m-%d %H:%M:%S"),
        "author": post.student_id
    }
    return jsonify(data), 200


@app_forum.route('/post/put', methods = ['POST'])
def put_post():
    """
发布帖子
---
tags:
  - Forum
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        title:
          type: string
          description: 帖子标题
        content:
          type: string
          description: 帖子内容
        topic:
          type: string
          description: 帖子主题
        board:
          type: string
          description: 论坛板块
responses:
  200:
    description: 帖子发布成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 发布成功
  202:
    description: 帖子发布失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 发布失败
"""

    req_data = request.get_json()
    req_data["student_id"] = session.get("student_id", 'admin')
    req_data["created_time"] = datetime.now()
    req_data["last_updated_time"] = datetime.now()
    # 单独抽离content
    content = req_data.pop("content")
    
    post = Post(**req_data)
    try:
        db.session.execute(fk_command)
        db.session.add(post)
        db.session.commit()
        
        post_content = PostContent(post_id=post.post_id, content=content)
        db.session.add(post_content)
        db.session.commit()
        return jsonify(msg="发布成功")
    except Exception as e:
        return jsonify(msg="发布失败", error=str(e)), 202

@app_forum.route('/post/delete', methods = ['POST'])
def delete_post():
    """
删除帖子
---
tags:
  - Forum
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        post_id:
          type: integer
          description: 帖子ID
responses:
  200:
    description: 帖子删除成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 删除成功
  202:
    description: 帖子删除失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 删除失败
"""

    req_data = request.get_json()
    post = Post.query.filter_by(post_id=req_data["post_id"]).first()
    if post is None:
        return jsonify(msg=f"帖子不存在"), 202
    try:
        post.used = False
        db.session.commit()
        return jsonify(msg="删除成功")
    except Exception as e:
        return jsonify(msg="删除失败", error=str(e)), 202

@app_forum.route('/post/addview', methods = ['POST'])
def add_view_count():
    """
增加帖子查看数
---
tags:
  - Forum
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        post_id:
          type: integer
          description: 帖子ID
responses:
  200:
    description: 增加帖子查看数成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 增加查看数成功
  202:
    description: 增加帖子查看数失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 增加查看数失败
"""

    req_data = request.get_json()
    post = Post.query.filter_by(post_id=req_data["post_id"]).first()
    if post is None:
        return jsonify(msg=f"帖子不存在"), 202
    try:
        post.view_count += 1
        db.session.commit()
        return jsonify(msg="增加查看数成功")
    except Exception as e:
        return jsonify(msg="增加查看数失败", error=str(e)), 202

@app_forum.route('/reply/get', methods = ['POST'])
def get_post_reply():
    """
获取帖子回复信息
---
tags:
  - Forum
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        post_id:
          type: integer
          description: 帖子ID
responses:
  200:
    description: 成功获取帖子回复信息
    schema:
      type: array
      items:
        type: object
        properties:
          reply_id:
            type: integer
            description: 回复ID
          content:
            type: string
            description: 回复内容
          created_time:
            type: string
            description: 回复创建时间（格式：YYYY-MM-DD HH:MM:SS）
  404:
    description: 未找到帖子回复信息
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 未找到帖子回复信息
"""

    req_data = request.get_json()
    replies = Reply.query.filter_by(post_id=req_data["post_id"], used=True).all()
    data = [dict((c, getattr(reply, c)) for c in inspect(reply).mapper.column_attrs.keys()) for reply in replies]
    # 修改时间格式
    for reply in data:
        reply["created_time"] = reply["created_time"].strftime("%Y-%m-%d %H:%M:%S")
    print(data)
    return jsonify(data)

@app_forum.route('/reply/put', methods = ['POST'])
def put_reply():
    """
回复帖子
---
tags:
  - Forum
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        post_id:
          type: integer
          description: 帖子ID
        content:
          type: string
          description: 回复内容
responses:
  200:
    description: 回复帖子成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 回复成功
  202:
    description: 回复帖子失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 回复失败
"""

    req_data = request.get_json()
    req_data["student_id"] = session.get("student_id", 'admin')
    req_data["created_time"] = datetime.now()
    
    # 判断post_id是否存在
    post = Post.query.filter_by(post_id=req_data["post_id"]).first()
    if post is None:
        return jsonify(msg=f"回复的帖子不存在"), 202
    
    reply = Reply(**req_data)
    try:
        db.session.execute(fk_command)
        db.session.add(reply)
        post.last_updated_time = datetime.now()
        db.session.commit()
        return jsonify(msg="回复成功")
    except Exception as e:
        return jsonify(msg="回复失败", error=str(e)), 202

@app_forum.route('/reply/delete', methods = ['POST'])
def delete_reply():
    """
删除回复
---
tags:
  - Forum
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        reply_id:
          type: integer
          description: 回复ID
responses:
  200:
    description: 删除回复成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 删除成功
  202:
    description: 删除回复失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 删除失败
"""

    req_data = request.get_json()
    reply = Reply.query.filter_by(reply_id=req_data["reply_id"]).first()
    if reply is None:
        return jsonify(msg=f"回复不存在"), 202
    try:
        reply.used = False
        db.session.commit()
        return jsonify(msg="删除成功")
    except Exception as e:
        return jsonify(msg="删除失败", error=str(e)), 202








