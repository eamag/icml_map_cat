import json
import sqlite3


class PaperDatabase:
    def __init__(self, db_name="icml.sqlite"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Check if the table already exists
            cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='papers';
            """)
            table_exists = cursor.fetchone()

            # If the table does not exist, create it
            if not table_exists:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    classification_reasoning TEXT,
                    field TEXT,
                    discipline TEXT,
                    sub_discipline TEXT,
                    area TEXT,
                    topic TEXT,
                    subtopic TEXT,
                    problems_addressed TEXT,
                    follow_up_tasks TEXT,
                    further_research TEXT,
                    outstanding_paper_award_probability REAL,
                    startup_based_on_paper TEXT,
                    alternative_classifications TEXT,
                    pdf_link TEXT
                )
                """)
                conn.commit()

    def insert_paper(self, paper_data):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Convert the nested structures to JSON strings
            problems_addressed_json = json.dumps(paper_data["problems_addressed"])
            follow_up_tasks_json = json.dumps(paper_data["follow_up_tasks"])
            further_research_json = json.dumps(paper_data["further_research"])
            alternative_classifications_json = json.dumps(
                paper_data["alternative_classifications"]
            )
            cursor.execute(
                """
                INSERT INTO papers (
                    id, title, classification_reasoning, field, discipline, sub_discipline, 
                    area, topic, subtopic, problems_addressed, follow_up_tasks, further_research, 
                    outstanding_paper_award_probability, startup_based_on_paper, 
                    alternative_classifications, pdf_link
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    paper_data["id"],
                    paper_data.get("title", ""),
                    paper_data.get("classification_reason_sub_discipline", ""),
                    paper_data["field"],
                    paper_data["discipline"],
                    paper_data["sub_discipline"],
                    paper_data["area"],
                    paper_data["topic"],
                    paper_data["subtopic"],
                    problems_addressed_json,
                    follow_up_tasks_json,
                    further_research_json,
                    paper_data.get("outstanding_paper_award_probability", 0.0),
                    paper_data.get("startup_based_on_paper", ""),
                    alternative_classifications_json,
                    paper_data["pdf_link"],
                ),
            )
            conn.commit()

    def id_exists(self, paper_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM papers WHERE id = ?", (paper_id,))
            existing_id = cursor.fetchone()
            return True if existing_id else False

    def get_unique_topics(self, res):
        sub_discipline = res.get("sub_discipline")
        area = res.get("area")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
            SELECT DISTINCT topic FROM papers
            WHERE sub_discipline = ? AND area = ?
            """,
                (sub_discipline, area),
            )
            unique_topics = [row[0] for row in cursor.fetchall()]
            return unique_topics

    def get_sub_topics(self, res):
        sub_discipline = res.get("sub_discipline")
        area = res.get("area")
        topic = res.get("topic")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
            SELECT DISTINCT subtopic FROM papers
            WHERE sub_discipline = ? AND area = ? AND topic = ?
            """,
                (sub_discipline, area, topic),
            )
            sub_topics = [row[0] for row in cursor.fetchall()]
            return sub_topics
