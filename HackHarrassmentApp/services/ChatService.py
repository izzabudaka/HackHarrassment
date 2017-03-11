import sqlite3


class ChatService:
    def add_user(self, name):
        conn = self.get_conn()
        c = conn.cursor()

        exists = self.user_exists(name)

        if exists is None:
            c.execute("INSERT OR IGNORE INTO `chat_users`(`name`) VALUES(?)", (name,))
            rowid = c.lastrowid
            conn.commit()
            conn.close()
        else:
            rowid = exists
        return rowid

    def user_exists(self, name):
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("SELECT `id` FROM `chat_users` WHERE `name` = ?", (name, ))
        result = c.fetchone()
        conn.close()
        return result

    def create_relation_node(self, user1, user2):
        if self.user_exists(user1) is None or self.user_exists(user2) is None:
            return
        if user2 > user1:
            user1, user2 = user2, user1

        if self.relation_node_exists(user1, user2) is not None:
            return

        conn = self.get_conn()
        c = conn.cursor()

        c.execute("INSERT INTO `chat_connections`(`user_id1`, `user_id2`) VALUES(?, ?)", (user1, user2, ))
        conn.commit()
        conn.close()

    def get_all_relations(self):
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("SELECT `user_id1`, `user_id2` FROM `chat_connections`")
        result = c.fetchall()
        conn.close()
        return result

    def get_all_users_after(self, after):
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("SELECT `id`, `name`, `tagged` FROM `chat_users` WHERE `id` > ?", (after, ))
        result = c.fetchall()
        conn.close()
        return result

    def relation_node_exists(self, user1, user2):
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("SELECT `id` FROM `chat_connections` WHERE `user_id1` = ? AND `user_id2` = ?", (user1, user2,))
        result = c.fetchone()
        conn.close()
        return result

    def get_messages_after(self, last_msg_id):
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("SELECT `id`, `sender`, `receiver`, `message` FROM `chat_messages` WHERE `id` > ?", (last_msg_id, ))
        result = c.fetchall()
        conn.close()
        return result

    def insert_message(self, sender, receiver, message):
        if self.user_exists(receiver) is None or self.user_exists(sender) is None:
            return
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("INSERT INTO `chat_messages`(`sender`, `receiver`, `message`) VALUES(?, ?, ?)", (sender, receiver, message, ))
        row_id = c.lastrowid
        conn.commit()
        conn.close()

        self.create_relation_node(sender, receiver)
        return row_id

    def set_user_tagged(self, user_id):
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("UPDATE `chat_users` SET `tagged` = 1 WHERE `id` = ?", (user_id, ))
        conn.commit()
        conn.close()


    def get_conn(self):
        return sqlite3.connect('db.sqlite3')

    def get_last_message_id(self):
        conn = self.get_conn()
        c = conn.cursor()

        c.execute("SELECT `id` FROM `chat_messages` ORDER BY `id` DESC LIMIT 1")
        row_id = c.fetchone()
        if row_id is None:
            row_id = 0
        conn.close()
        return row_id

