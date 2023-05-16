-- 创建名为 genshin_impact 的库
create database if not exists genshin_impact;

-- 使用库
use genshin_impact;

-- 创建名为 record 的表 用来存取抽卡记录
create table if not exists record
(
    id          int primary key AUTO_INCREMENT comment 'ID',
    uid         int comment '账号uid',
    grab_time   timestamp comment '抽卡时间',
    goods_name  varchar(30) comment '物品名字',
    item_type   varchar(10) comment '物品类型',
    rank_type   int comment '物品等级',
    pool_type   int comment '卡池类型',
    upload_time timestamp default CURRENT_TIMESTAMP comment '上传时间'

);

-- 创建名为 user 的表 用于存取用户信息
create table if not exists user
(
    id          int unique key auto_increment comment 'ID编号',
    user_uid    int primary key comment '用户UID',
    create_time timestamp default CURRENT_TIMESTAMP comment '创建时间'
);

-- 给 record 表添加外键约束 外键约束是用于关联两个表的键 user为父表 record为子表
-- 当设置为外键约束的键插入数据的时候他会查询父表中的主键是否有这个数据如果没有会报错
ALTER TABLE record
    ADD CONSTRAINT userUID
        FOREIGN KEY (uid) REFERENCES user (user_uid);


