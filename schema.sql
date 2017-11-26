-- 用户表
create table if not exists user  (
    id           integer primary key autoincrement not null, -- id, 唯一标识符
    user_id     integer, -- 用户 id
    username        text, -- 用户名
    timestamp date -- 时间戳
);

-- wechat message
create table if not exists message (
    id integer primary key autoincrement not null, -- id,唯一标识符
    from_user_name text, -- 发送方 ID
    to_user_name text, --接收方 ID
    content text, -- 消息内容
    msg_type integer, -- 消息类型
    file_name text, -- 文件名
    status integer, -- 状态
    url text, -- url
    recommend_info text, -- 名片推荐信息
    timestamp date -- 时间戳
);
