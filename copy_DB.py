import json
import sqlite3


class CopyBase():
    def __init__(self, path_old_base, path_new_base):
        self.old_conn = sqlite3.connect(path_old_base)
        self.new_conn = sqlite3.connect(path_new_base)

    def export(self):
        dict_tables_with_data = {}

        for table in self.old_conn.execute(f"SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            name_table = table[0]
            dict_positions_and_name_field_in_table = {}
            list_data_table = []
            for field in self.old_conn.execute(f"pragma table_info('{name_table}')").fetchall():
                position = field[0]
                name_field = field[1]
                dict_positions_and_name_field_in_table.update({position: name_field})
            for result_table in self.old_conn.execute(f"""SELECT * FROM {name_table}"""):
                temp_dict = {}
                for key, val in dict_positions_and_name_field_in_table.items():
                    values_for_add = result_table[key]
                    if val == 'writers':
                        if len(result_table[key]) is 0:
                            values_for_add = [temp_dict['writer']]
                        else:
                            values_for_add = [i['id'] for i in json.loads(result_table[key])]
                    temp_dict.update({val: values_for_add})
                list_data_table.append(temp_dict)
            dict_tables_with_data.update({name_table: list_data_table})
        return dict_tables_with_data

    def create_recording(self, select, insert, tuple_values, flag=False):
        if bool(self.new_conn.execute(f"""{select}""", (tuple_values)).fetchall()) is flag:
            self.new_conn.execute(f"""{insert}""", (tuple_values))
            self.new_conn.commit()

    def load(self, data):
        for value in data['actors']:
            self.create_recording(select='SELECT * FROM main_actor WHERE id=? AND name=?',
                                  insert="INSERT INTO main_actor (id, name) VALUES (?, ?)",
                                  tuple_values=(value['id'], value['name'],))

        for value in data['writers']:
            self.create_recording(select='SELECT * FROM main_writer WHERE id=? AND name=?',
                                  insert="INSERT INTO main_writer (id, name) VALUES (?, ?)",
                                  tuple_values=(value['id'], value['name'],))

        for value in data['movie_actors']:
            self.create_recording(select=f"SELECT * FROM main_movie_actors WHERE movie_id=? AND actor_id=?",
                                  insert="INSERT INTO main_movie_actors (movie_id, actor_id) VALUES (?, ?)",
                                  tuple_values=(value['movie_id'], value['actor_id']))

        for value in data['movies']:
            for writer in value['writers']:
                self.create_recording(select=f"SELECT * FROM main_movie_writers WHERE movie_id=? AND writer_id=?",
                                      insert="INSERT INTO main_movie_writers (movie_id,writer_id) VALUES (?, ?)",
                                      tuple_values=(value['id'], writer), flag=True)

            if self.new_conn.execute(f"""SELECT * FROM main_movie_writers WHERE id=?""",
                                     ((value['id'],))).fetchall() is not None:
                writers_list = [
                    self.new_conn.execute(f"""SELECT * FROM main_writer WHERE id=?""", ((writer,))).fetchone()[1] for
                    writer in value['writers']]
                writers_names = ','.join(writers_list)

            if self.new_conn.execute(f"""SELECT * FROM main_movie_actors WHERE movie_id=?""",
                                     ((value['id'],))).fetchall() is not None:
                actors_list = [
                    self.new_conn.execute(f"""SELECT * FROM main_actor WHERE id=?""", ((actor[2],))).fetchone()[1] for
                    actor in self.new_conn.execute(f"""SELECT * FROM main_movie_actors WHERE movie_id=? """,
                                                   ((value['id'],))).fetchall()]
                actors_names = ','.join(actors_list)

            if self.new_conn.execute(f"""SELECT * FROM main_movie WHERE id=?""", ((value['id'],))).fetchone() is None:
                self.new_conn.execute(
                    """INSERT INTO main_movie (id, title, genre, description, writers_names, director, actors_names, imdb) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ((value['id'], value['title'], value['genre'], value['plot'], writers_names, value['director'],
                      actors_names, value['imdb_rating'],)))
                self.new_conn.commit()


obj = CopyBase('old.sqlite', 'movies/db.sqlite3')
data_table = obj.export()
obj.load(data_table)
