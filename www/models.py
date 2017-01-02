# !/usr/bin/python
# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from utils import utc_time


# 用户表
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)  # 自增ID
    name = Column(String(40), unique=True)  # 用户昵称
    email = Column(String(100), unique=True)  # 邮箱
    password = Column(String(200))  # 密码
    mobile = Column(String(20), nullable=True)  # 手机号
    created_date = Column(DateTime, default=utc_time())  # 创建日期
    level = Column(Integer, default=0)   # 用户等级
    wexin = Column(String(40), nullable=True)  # 微信号
    qq = Column(String(20), nullable=True)  # QQ号
    weibo = Column(String(100), nullable=True)  # 微博地址
    site = Column(String(100), nullable=True)  # 个人网址
    score = Column(Integer, default=0)  # 用户积分
    status = Column(Boolean, default=False)  # 是否验证
    desc = Column(String(200), default='')  # 用户签名

    # 用户文章
    posts = relationship('Post', back_populates='user_posts')

    def __repr__(self):
        return '<%s (%r, %r)>' % (self.__class__.__name__, self.name, self.email)


# 用户元数据表
class UserMeta(Base):
    __tablename__ = 'users_meta'

    user_meta_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.user_id))
    k = Column(String(20), nullable=False)
    v = Column(String(50), nullable=False)

    def __repr__(self):
        return '<%s  %r>' % (self.__class__.__name__, self.user_id)


# 文章表
class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True, autoincrement=True)  # 自增ID
    author = Column(String(40), default='网友')  # 作者
    source = Column(String(40), default='网络')  # 来源站点
    source_url = Column(String(200), default='http://minzhulou.com')  # 原文链接
    publish_time = Column(DateTime, default=utc_time())  # 发布时间
    title = Column(String(200), nullable=False)  # 标题
    summary = Column(String(300), nullable=True)  # 摘要
    content_md = Column(Text, nullable=False)  # 正文md格式
    content_html = Column(Text, nullable=True)  # 正文html格式
    read_count = Column(Integer, default=0)  # 阅读次数
    up_vote = Column(Integer, default=0)  # 顶的次数
    down_vote = Column(Integer, default=0)  # 踩的次数
    collect_count = Column(Integer, default=0)  # 收藏次数
    feature_url = Column(String(200), nullable=True)  # 文章特色图片url

    # 一篇文章对应多个分类
    taxonomies = relationship('PostTaxRelationship', back_populates='post_taxonomies')
    # 一篇文章对应多个评论
    comments = relationship('Comment', back_populates='post_comments')

    def __repr__(self):
        return '<%s (%r, %r)>' % (self.__class__.__name__, self.author, self.title)


# 文章元数据表
class PostMeta(Base):
    __tablename__ = 'posts_meta'

    post_meta_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey(Post.post_id))
    k = Column(String(20), nullable=False)
    v = Column(String(50), nullable=False)

    def __repr__(self):
        return '<%s  %r>' % (self.__class__.__name__, self.post_id)


# 评论表
class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey(Post.post_id))  # 评论所属的文章id
    user_id = Column(Integer, ForeignKey(User.user_id))  # 评论用户id
    ip = Column(Integer)  # 用户ip地址
    comment_time = Column(DateTime, default=utc_time())  # 评论时间
    parent_id = Column(Integer, default=0)  # 评论的父评论
    content = Column(String(1024), nullable=False)  # 评论内容
    up_vote = Column(Integer, default=0)  # 顶
    down_vote = Column(Integer, default=0)  # 踩
    approved = Column(Boolean, default=True)   # 是否通过

    def __repr__(self):
        return '<%s  (%r, %r)>' % (self.__class__.__name__, self.comment_id, self.post_id)


# 分类表
class Taxonomy(Base):
    __tablename__ = 'taxonomy'

    taxonomy_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)  # 分类名,如:科技
    slug = Column(String(30), unique=True)  # 分类别名,如:tech
    description = Column(String(100), default='')  # 分类描述
    parent_id = Column(Integer, default=-1)  # 父ID,-1表示为一级分类
    count = Column(Integer, default=0)  # 属于该分类的文章数
    taxonomy_type = Column(Integer, default=0)  # 0：分类, 1:标签, 2: 其他

    # 一个分类对应多个文章
    posts = relationship('PostTaxRelationship', back_populates='taxonomy_posts')

    def __repr__(self):
        return '<%s  (%r, %r)>' % (self.__class__.__name__, self.taxonomy_id, self.name)


# 文章-分类关联表(将文章跟分类关联起来)
class PostTaxRelationship(Base):
    __tablename__ = 'post_tax_relationship'

    relationship_id = Column(Integer, primary_key=True, autoincrement=True)
    ref_object_id = Column(Integer, ForeignKey('posts.post_id'))
    ref_taxonomy_id = Column(Integer, ForeignKey('taxonomy.taxonomy_id'))
    term_order = Column(Integer, default=0)

    def __repr__(self):
        return '<%s  (%r, %r)>' % (self.__class__.__name__, self.ref_object_id, self.ref_taxonomy_id)

